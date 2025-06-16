import subprocess
import os

scenario_dir = "/Users/aurora0926/my_project/py-mgipsim-main/pymgipsim/Settings/DefaultSettings"


scenario_files = [
    os.path.join(scenario_dir, f)
    for f in os.listdir(scenario_dir)
    if f.startswith("scenario_") and f.endswith(".json") and f != "scenario_default.json"
]

main_script = "manual_script.py"


for f in scenario_files:
    print(" -", f)


for f in scenario_files:
    subprocess.run(["python", main_script, "--settings_file", f])
