import json
import random
from copy import deepcopy


default_scenario = {
    "settings": {
        "save_directory": "/Users/aurora0926/my_project/py-mgipsim-main/SimulationResults",
        "start_time": 0,
        "end_time": 1440,
        "random_seed": 402,
        "random_state": {},
        "sampling_time": 1,
        "solver_name": "RK4",
        "simulator_name": "SingleScaleSolver"
    },
    "input_generation": {
        "fraction_cho_intake": [0.4, 0.6],
        "fraction_cho_as_snack": [0.1, 0.2],
        "net_calorie_balance": [0],
        "meal_duration": [30, 60],
        "snack_duration": [5, 15],
        "breakfast_carb_range": [80, 120],
        "lunch_carb_range": [80, 120],
        "dinner_carb_range": [80, 120],
        "am_snack_carb_range": [10, 20],
        "pm_snack_carb_range": [10, 20],
        "total_carb_range": [260, 400],
        "breakfast_time_range": [360, 480],
        "lunch_time_range": [720, 840],
        "dinner_time_range": [1080, 1200],
        "am_snack_time_range": [540, 660],
        "pm_snack_time_range": [900, 1020],
        "running_start_time": ["00:00"],
        "running_duration": [0.0],
        "running_incline": [0.0],
        "running_speed": [0.0],
        "cycling_start_time": ["00:00"],
        "cycling_duration": [0.0],
        "cycling_power": [0.0],
        "sglt2i_dose_magnitude": 0,
        "sglt2i_dose_time_range": [360, 540]
    },
    "inputs": None,
    "controller": {
        "name": "OpenLoop",
        "parameters": []
    },
    "patient": {
        "demographic_info": {
            "renal_function_category": 1,
            "body_weight_range": [60, 80]
        },
        "number_of_subjects": 20,
        "model": {
            "name": "T1DM.ExtHovorka",
            "parameters": None,
            "initial_conditions": None
        },
        "mscale": {
            "models": ["Multiscale.BodyWeight"]
        }
    }
}

def generate_day_scenario(day_idx, seed):
    random.seed(seed)
    sc = deepcopy(default_scenario)

    
    breakfast_time = random.randint(420, 540)
    lunch_time = random.randint(720, 840)
    dinner_time = random.randint(1080, 1200)

    sc["input_generation"]["breakfast_time_range"] = [breakfast_time, breakfast_time]
    sc["input_generation"]["lunch_time_range"] = [lunch_time, lunch_time]
    sc["input_generation"]["dinner_time_range"] = [dinner_time, dinner_time]

    
    sc["input_generation"]["breakfast_carb_range"] = sorted(random.sample(range(30, 71), 2))
    sc["input_generation"]["lunch_carb_range"] = sorted(random.sample(range(40, 91), 2))
    sc["input_generation"]["dinner_carb_range"] = sorted(random.sample(range(50, 101), 2))

    
    sc["input_generation"]["running_start_time"] = ["00:00"]
    sc["input_generation"]["running_duration"] = [0.0]
    sc["input_generation"]["running_incline"] = [0.0]
    sc["input_generation"]["running_speed"] = [0.0]
    sc["input_generation"]["cycling_start_time"] = ["00:00"]
    sc["input_generation"]["cycling_duration"] = [0.0]
    sc["input_generation"]["cycling_power"] = [0.0]

    
    exercise_type = random.choice(["running", "cycling"])
    meal_hours = [breakfast_time // 60, lunch_time // 60, dinner_time // 60]
    valid_hours = [h for h in range(6, 21) if all(abs(h - mh) >= 1 for mh in meal_hours)]
    hour = random.choice(valid_hours)

    if exercise_type == "running":
        sc["input_generation"]["running_start_time"] = [f"{hour}:00"]
        sc["input_generation"]["running_duration"] = [random.choice([20.0, 30.0, 40.0])]
        sc["input_generation"]["running_speed"] = [round(random.uniform(5.0, 6.5), 1)]
        sc["input_generation"]["running_incline"] = [random.choice([0.0, 0.5, 1.0])]
    else:
        sc["input_generation"]["cycling_start_time"] = [f"{hour}:00"]
        sc["input_generation"]["cycling_duration"] = [random.choice([20.0, 30.0, 45.0])]
        sc["input_generation"]["cycling_power"] = [random.randint(80, 150)]

    
    with open(f"scenario_day_{day_idx}.json", "w") as f:
        json.dump(sc, f, indent=4)

    print(f"Day {day_idx} scenario generated.")


for day in range(1, 15):
    generate_day_scenario(day_idx=day, seed=100 + day)

print("All 14 daily scenario files generated without empty fields.")
