import os
import json
from collections import defaultdict

def merge_json_files(input_dirs, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = defaultdict(list)
    for input_dir in input_dirs:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    json_files[file].append(file_path)

    for json_file, paths in json_files.items():
        merged_data = []
        
        if len(paths) == 1:
            with open(paths[0], 'r') as f:
                data = json.load(f)
            merged_data = data if isinstance(data, list) else [data]
        else:
            for file_path in paths:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)

        output_path = os.path.join(output_dir, json_file)
        with open(output_path, 'w') as f:
            json.dump(merged_data, f, indent=4)
        
        print(f"Processed {json_file} into {output_path}")


input_dirs = ["Outputs/Intellipaat", "Outputs/Interviewbit", "Outputs/Javatpoint"]
output_dir = "Combined"


def update_json_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
            role = os.path.splitext(filename)[0]
            
            for entry in data:
                entry['role'] = role
            
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

directory = 'combined'


# merge_json_files(input_dirs, output_dir)
update_json_files(directory)