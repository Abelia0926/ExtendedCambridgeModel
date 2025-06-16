import argparse
import subprocess
import os
from pymgipsim.Utilities.paths import results_path
from pymgipsim.Utilities import simulation_folder

from pymgipsim.Interface.parser import generate_parser_cli
from pymgipsim.InputGeneration.activity_settings import activity_args_to_scenario

from pymgipsim.generate_settings import generate_simulation_settings_main
from pymgipsim.generate_inputs import generate_inputs_main
from pymgipsim.generate_subjects import generate_virtual_subjects_main
from pymgipsim.generate_plots import generate_plots_main
from pymgipsim.generate_results import generate_results_main

from pymgipsim.Utilities.Scenario import load_scenario
from pathlib import Path
import json



if __name__ == '__main__':

     parser = argparse.ArgumentParser()
     parser.add_argument("--settings_file", type=str, required=True, help="Path to scenario JSON")
     args_from_cmd = parser.parse_args()

     settings_file = load_scenario(args_from_cmd.settings_file)


     subprocess.run(['python', 'initialization.py'])


     scenario_base = Path(args_from_cmd.settings_file).stem
     scenario_name = f"{scenario_base}_patient_1"
     results_folder_path = os.path.join(results_path, scenario_name)
     os.makedirs(results_folder_path, exist_ok=True)

     figures_path = os.path.join(results_folder_path, "figures")
     os.makedirs(figures_path, exist_ok=True)


     args = generate_parser_cli().parse_args(args=[])
     args.controller_name = "OpenLoop"
     args.model_name = "T1DM.ExtHovorka"
     args.patient_names = ["Patient_1"]
     args.plot_patient = 0

     args.breakfast_carb_range = settings_file.input_generation.breakfast_carb_range
     args.lunch_carb_range = settings_file.input_generation.lunch_carb_range
     args.dinner_carb_range = settings_file.input_generation.dinner_carb_range
     args.am_snack_carb_range = settings_file.input_generation.am_snack_carb_range
     args.pm_snack_carb_range = settings_file.input_generation.pm_snack_carb_range


     if not args.scenario_name:
         settings_file = generate_simulation_settings_main(scenario_instance=settings_file, args=args, results_folder_path=results_folder_path)
         settings_file = generate_virtual_subjects_main(scenario_instance=settings_file, args=args, results_folder_path=results_folder_path)
         settings_file = generate_inputs_main(scenario_instance=settings_file, args=args, results_folder_path=results_folder_path)

     model, _ = generate_results_main(scenario_instance=settings_file, args=vars(args), results_folder_path=results_folder_path)

     single_model = model.singlescale_model


     glucose_raw = single_model.states.as_array[0, single_model.glucose_state, :]
     VG = single_model.parameters.VG[0]


     glucose_mgdL = (glucose_raw / VG) * 18


     bg_mgdl = glucose_mgdL.tolist()
     output_path = os.path.join(results_folder_path, "bg_output.json")
     with open(output_path, "w") as f:
         json.dump({"bg_mgdl": bg_mgdl}, f)


     figures = generate_plots_main(results_folder_path, args)
