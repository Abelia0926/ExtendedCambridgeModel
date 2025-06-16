import json, random
from copy import deepcopy

with open("scenario_default.json", "r") as f:
    base = json.load(f)


def generate_one(seed):
    random.seed(seed)
    sc = deepcopy(base)

    breakfast_time = random.randint(420, 540) #7-9 AM
    sc["input_generation"]["breakfast_time_range"] = [breakfast_time, breakfast_time]
    sc["input_generation"]["breakfast_carb_range"] = sorted(random.sample(range(30, 71), 2))

    lunch_time = random.randint(720, 840) #12-2 PM
    sc["input_generation"]["lunch_time_range"] = [lunch_time, lunch_time]
    sc["input_generation"]["lunch_carb_range"] = sorted(random.sample(range(40, 91), 2))

    dinner_time = random.randint(1080, 1200)#6-8 PM
    sc["input_generation"]["dinner_time_range"] = [dinner_time, dinner_time]
    sc["input_generation"]["dinner_carb_range"] = sorted(random.sample(range(50, 101), 2))

    am_snack_time = random.randint(600, 660) #10-11 AM
    sc["input_generation"]["am_snack_time_range"] = [am_snack_time, am_snack_time]
    sc["input_generation"]["am_snack_carb_range"] = sorted(random.sample(range(10, 31), 2))

    pm_snack_time = random.randint(900, 960) # 3-4 PM
    sc["input_generation"]["pm_snack_time_range"] = [pm_snack_time, pm_snack_time]
    sc["input_generation"]["pm_snack_carb_range"] = sorted(random.sample(range(10, 31), 2))

    sc["input_generation"]["meal_duration"] = [30, 60]
    sc["input_generation"]["snack_duration"] = [5, 15]

    sc["input_generation"]["fraction_cho_intake"] = [0.4, 0.6]
    sc["input_generation"]["fraction_cho_as_snack"] = [0.1, 0.2]
    sc["input_generation"]["net_calorie_balance"] = [0]
    sc["input_generation"]["total_carb_range"] = [260, 400]

    sc["input_generation"]["running_start_time"] = ["00:00"]
    sc["input_generation"]["running_duration"] = [0.0]
    sc["input_generation"]["running_speed"] = [0.0]
    sc["input_generation"]["running_incline"] = [0.0]

    sc["input_generation"]["cycling_start_time"] = ["00:00"]
    sc["input_generation"]["cycling_duration"] = [0.0]
    sc["input_generation"]["cycling_power"] = [0.0]

    include_running = random.random() < 0.5
    include_cycling = random.random() < 0.3

    running_hour = None

    if include_running:
        running_hour = random.randint(6, 20)
        sc["input_generation"]["running_start_time"] = [f"{running_hour}:00"]
        sc["input_generation"]["running_duration"] = [random.choice([20.0, 30.0, 40.0])]
        sc["input_generation"]["running_speed"] = [round(random.uniform(5.0, 6.5), 1)]
        sc["input_generation"]["running_incline"] = [random.choice([0.0, 0.5, 1.0])]

    if include_cycling:
        valid_hours = list(range(6, 21))
        if running_hour is not None:
            valid_hours = [h for h in valid_hours if abs(h - running_hour) >= 1]

        if valid_hours:
            cycling_hour = random.choice(valid_hours)
            sc["input_generation"]["cycling_start_time"] = [f"{cycling_hour}:00"]
            sc["input_generation"]["cycling_duration"] = [random.choice([20.0, 30.0, 45.0])]
            sc["input_generation"]["cycling_power"] = [random.randint(80, 150)]


    with open(f"scenario_continuous{seed}.json", "w") as f:
        json.dump(sc, f, indent=4)


for i in range(100):
    generate_one(seed=100 + i)
