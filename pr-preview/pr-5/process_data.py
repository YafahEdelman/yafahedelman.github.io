import os
import zipfile
import csv
import json
import glob
import math

def read_csv(filepath):
    data = []
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean up values
            clean_row = {}
            for k, v in row.items():
                if k is None: continue
                # Try to convert to number if possible, but keep original if needed?
                # Actually, JSON usually expects numbers as numbers.
                # Let's try to convert simple numbers.
                val = v
                if v == "":
                    val = None
                else:
                    try:
                        f_val = float(v)
                        if math.isnan(f_val) or math.isinf(f_val):
                             val = None # JSON null
                        else:
                             # check if it's an integer
                             if f_val.is_integer():
                                 val = int(f_val)
                             else:
                                 val = f_val
                    except ValueError:
                        val = v # Keep as string

                clean_row[k] = val
            data.append(clean_row)
    return data

datasets = {}

# Ensure directories exist
base_dir = "temp_downloads"

# Define mappings: Zip Name -> { Dataset Name: CSV Filename }
# Note: zip files are already downloaded in base_dir.
# We will unzip them into subdirectories.

zip_maps = {
    "ai_models.zip": {
        "AI Models (All)": "all_ai_models.csv",
        "AI Models (Notable)": "notable_ai_models.csv"
    },
    "benchmark_data.zip": {
        "Epoch Capabilities Index": "epoch_capabilities_index.csv",
        "MMLU Benchmark": "mmlu_external.csv",
        "MATH Benchmark": "math_level_5.csv",
        "HumanEval Benchmark": "human_eval_external.csv" # check if exists
    },
    "data_centers.zip": {
        "Data Centers": "data_centers.csv"
    },
    "ml_hardware.zip": {
        "ML Hardware": "ml_hardware.csv"
    },
    "ai_companies.zip": {
        "AI Companies": "ai_companies.csv",
        "AI Company Revenue": "ai_companies_revenue_reports.csv",
        "AI Company Funding": "ai_companies_funding_rounds.csv"
    },
    "gpu_clusters.zip": {
        "GPU Clusters": "gpu_clusters.csv"
    },
    "ai_chip_sales.zip": {
        "AI Chip Sales": "timelines_by_chip.csv"
    }
}

# Unzip and load
for zip_name, data_map in zip_maps.items():
    zip_path = os.path.join(base_dir, zip_name)
    if os.path.exists(zip_path):
        extract_path = os.path.join(base_dir, zip_name.replace('.zip', ''))
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        for ds_name, csv_name in data_map.items():
            # Find the file in extracted path (it might be in root or subfolder)
            # We do a recursive search
            found_files = glob.glob(os.path.join(extract_path, "**", csv_name), recursive=True)
            if found_files:
                print(f"Loading {ds_name} from {found_files[0]}...")
                datasets[ds_name] = read_csv(found_files[0])
            else:
                print(f"Warning: {csv_name} not found in {zip_name}")

# Handle standalone CSVs
standalone_csvs = {
    "polling_on_ai_usage_dec_2025.csv": "Public Opinion on AI"
}

for filename, ds_name in standalone_csvs.items():
    path = os.path.join(base_dir, filename)
    if os.path.exists(path):
        print(f"Loading {ds_name} from {path}...")
        datasets[ds_name] = read_csv(path)

# Verify we have data
print("Datasets loaded:")
for k, v in datasets.items():
    print(f"  {k}: {len(v)} records")

# Write to JS file
output_file = "datasets.js"
print(f"Writing to {output_file}...")

# We write it as a JS assignment.
# To avoid huge memory issues during json.dumps of everything at once if it's massive,
# we can write key by key.

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("window.EPOCH_DATASETS = {};\n")
    for k, v in datasets.items():
        json_str = json.dumps(v, ensure_ascii=False)
        # Escape single quotes if necessary? json.dumps produces double quotes, so we are fine wrapping in nothing or just assignment.
        f.write(f"window.EPOCH_DATASETS['{k}'] = {json_str};\n")

# Create a summary object for the AI
summary = {}
for k, v in datasets.items():
    if len(v) > 0:
        summary[k] = list(v[0].keys())

with open("datasets_schema.js", 'w', encoding='utf-8') as f:
    f.write("window.DATASET_SCHEMAS = " + json.dumps(summary, indent=2) + ";\n")

print("Done.")
