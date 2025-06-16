import subprocess
import os

def run_14_day_simulations():
    json_dir = "/Users/aurora0926/my_project/py-mgipsim-main/pymgipsim/Settings/DefaultSettings"
    
    
    main_script = "manual_script.py"
    
    for day_idx in range(1, 15):
        scenario_file = os.path.join(json_dir, f"scenario_day_{day_idx}.json")
        subprocess.run([
            "python", 
            main_script, 
            "--settings_file", scenario_file,
            "--day_idx", str(day_idx)
        ])
        
        

if __name__ == "__main__":
    run_14_day_simulations()
