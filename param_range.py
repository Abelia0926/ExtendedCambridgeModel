import os, json
from collections import defaultdict


folder_path = "pymgipsim/VirtualPatient/Models/T1DM/ExtHovorka/Patients"


param_ranges = defaultdict(lambda: {"min": float("inf"), "max": float("-inf")})


for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), 'r') as f:
            data = json.load(f)
            for group in ["model_parameters", "demographic_info"]:
                for key, value in data.get(group, {}).items():
                    if isinstance(value, (int, float)):
                        param_ranges[f"{group}.{key}"]["min"] = min(param_ranges[f"{group}.{key}"]["min"], value)
                        param_ranges[f"{group}.{key}"]["max"] = max(param_ranges[f"{group}.{key}"]["max"], value)


for param, val in sorted(param_ranges.items()):
    print(f"{param:}  : min: {val['min']:>8.6f}   max: {val['max']:>8.6f}")
