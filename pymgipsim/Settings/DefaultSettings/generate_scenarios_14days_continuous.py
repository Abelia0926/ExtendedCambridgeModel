import json
import random
from copy import deepcopy

with open("scenario_default.json", "r") as f:
    base = json.load(f)

def generate_one(seed):
    random.seed(seed)
    sc = deepcopy(base)
    breakfast_range = sc["input_generation"]["breakfast_time_range"]
    lunch_range = sc["input_generation"]["lunch_time_range"]
    dinner_range = sc["input_generation"]["dinner_time_range"]
    
    num_days = 14

    def avoid_meal_time():
        
        valid = False
        while not valid:
            t = random.randint(360, 1260)  
            valid = True
            for meal_range in [breakfast_range, lunch_range, dinner_range]:
                meal_t = sum(meal_range) / 2  
                if abs(t - meal_t) < 30:
                    valid = False
                    break
        return t

    
    running_start = [[0.0 for _ in range(num_days)]]
    running_duration = [[0.0 for _ in range(num_days)]]
    running_speed = [[0.0 for _ in range(num_days)]]
    running_incline = [[0.0 for _ in range(num_days)]]

    cycling_start = [[0.0 for _ in range(num_days)]]
    cycling_duration = [[0.0 for _ in range(num_days)]]
    cycling_power = [[0.0 for _ in range(num_days)]]

    for day in range(num_days):
        if random.random() < 0.5:
            # Running
            t = avoid_meal_time()
            running_start[0][day] = float(t)
            running_duration[0][day] = random.choice([20.0, 30.0, 40.0])
            running_speed[0][day] = round(random.uniform(5.0, 6.5), 1)
            running_incline[0][day] = random.choice([0.0, 0.5, 1.0])
        else:
            # Cycling
            t = avoid_meal_time()
            cycling_start[0][day] = float(t)
            cycling_duration[0][day] = random.choice([20.0, 30.0, 45.0])
            cycling_power[0][day] = float(random.randint(80, 150))

    
    sc["input_generation"]["running_start_time"] = running_start
    sc["input_generation"]["running_duration"] = running_duration
    sc["input_generation"]["running_speed"] = running_speed
    sc["input_generation"]["running_incline"] = running_incline

    sc["input_generation"]["cycling_start_time"] = cycling_start
    sc["input_generation"]["cycling_duration"] = cycling_duration
    sc["input_generation"]["cycling_power"] = cycling_power

    
    with open(f"scenario_continuous{seed}.json", "w") as f:
        json.dump(sc, f, indent=4)


generate_one(seed=100)
