import os
import json
import pandas as pd

folder_path = "pymgipsim/VirtualPatient/Models/T1DM/ExtHovorka/Patients"


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


corr = df.corr()


import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.figure(figsize=(16, 14))  
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", 
            annot_kws={"size": 6},  
            cbar_kws={'label': 'Correlation Coefficient'}) 
plt.xticks(rotation=90, fontsize=7)  
plt.yticks(rotation=0, fontsize=7)   
plt.title("Correlation Matrix of Patient Parameters", fontsize=14)
plt.tight_layout()
plt.savefig("/Users/aurora0926/my_project/param_correlation_matrix.png", dpi=300)
plt.show()

