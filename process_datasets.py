import requests
import zipfile
import io
import csv
import json
import os

DATASETS = {
    "AI Models": "https://epoch.ai/data/ai_models.zip",
    "ML Hardware": "https://epoch.ai/data/ml_hardware.zip"
}

OUTPUT_FILE = "datasets.js"

def download_and_extract(url):
    print(f"Downloading {url}...")
    try:
        r = requests.get(url)
        r.raise_for_status()
        z = zipfile.ZipFile(io.BytesIO(r.content))

        # Find the first CSV file
        csv_filename = None
        for name in z.namelist():
            if name.endswith('.csv') and not name.startswith('__macosx'):
                csv_filename = name
                break

        if not csv_filename:
            print(f"No CSV found in {url}")
            return None

        print(f"Processing {csv_filename}...")
        with z.open(csv_filename) as f:
            # Read CSV
            content = f.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(content))
            rows = list(csv_reader)
            return rows

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def main():
    final_data = {}
    schemas = {}

    for name, url in DATASETS.items():
        data = download_and_extract(url)
        if data:
            final_data[name] = data
            # Infer schema from the first row keys
            if len(data) > 0:
                schemas[name] = list(data[0].keys())
            else:
                schemas[name] = []

    # Write to JS file
    js_content = f"window.EPOCH_DATASETS = {json.dumps(final_data, indent=2)};\n"
    js_content += f"window.DATASET_SCHEMAS = {json.dumps(schemas, indent=2)};\n"

    with open(OUTPUT_FILE, "w") as f:
        f.write(js_content)

    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
