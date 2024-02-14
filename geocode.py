import csv
import googlemaps
import ujson
from dotenv import dotenv_values

# Load API key from .env file
config = dotenv_values(".env")
gmaps = googlemaps.Client(key=config["GOOGLE_MAPS_API_KEY"])


def geocode_address(address):
    """Geocode a single address."""
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]["geometry"]["location"]
            return location["lat"], location["lng"]
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None, None


def process_csv_and_create_geojson(input_csv_path, output_geojson_path):
    """Process CSV to geocode 'from' column and create a GeoJSON file."""
    features = []
    with open(input_csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lat, lng = geocode_address(row["from"])
            if lat is not None and lng is not None:
                feature = {
                    "type": "Feature",
                    "properties": row,
                    "geometry": {"type": "Point", "coordinates": [lng, lat]},
                }
                features.append(feature)

    geojson = {"type": "FeatureCollection", "features": features}

    with open(output_geojson_path, "w", encoding="utf-8") as f:
        f.write(ujson.dumps(geojson, ensure_ascii=False, indent=4))


# Example usage
input_csv_path = "deaths_IDF - Data.csv"
output_geojson_path = "deaths_IDF_Geocoded.geojson"
process_csv_and_create_geojson(input_csv_path, output_geojson_path)
