import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


folder_path = "pymgipsim/VirtualPatient/Models/T1DM/ExtHovorka/Patients"


save_dir = "/Users/aurora0926/my_project/param_distribution_Histogram/"
os.makedirs(save_dir, exist_ok=True)


patient_data = []


for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        with open(os.path.join(folder_path, filename), 'r') as f:
            data = json.load(f)
            patient_dict = {}
            for group in ["model_parameters", "demographic_info"]:
                for key, value in data.get(group, {}).items():
                    if isinstance(value, (int, float)):
                        patient_dict[f"{group}.{key}"] = value
            patient_data.append(patient_dict)


df = pd.DataFrame(patient_data)


for col in df.columns:

    plt.figure(figsize=(8, 4))
    sns.histplot(df[col], stat="count", bins=6, color='skyblue', edgecolor='black')
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.tight_layout()


    filename = col.replace('.', '_') + "_hist.png"
    plt.savefig(os.path.join(save_dir, filename), dpi=300)
    plt.close()

