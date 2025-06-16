import os
import json
import numpy as np
import matplotlib.pyplot as plt

def calculate_TIR(bg_values, time_values):
    thresholds = [54, 70, 180, 250]
    categories = ["Very Low", "Low", "Target", "High", "Very High"]
    tir_time = {k: 0.0 for k in categories}

    def get_category(g):
        if g < 54:
            return "Very Low"
        elif g < 70:
            return "Low"
        elif g <= 180:
            return "Target"
        elif g <= 250:
            return "High"
        else:
            return "Very High"

    for i in range(len(bg_values)-1):
        g1, g2 = bg_values[i], bg_values[i+1]
        t1, t2 = time_values[i], time_values[i+1]

        if g1 == g2:
            tir_time[get_category(g1)] += t2 - t1
            continue

        cross_points = []
        for th in thresholds:
            if (g1 - th) * (g2 - th) < 0:
                t_cross = t1 + (th - g1) * (t2 - t1) / (g2 - g1)
                cross_points.append((t_cross, th))

        points = [(t1, g1)] + cross_points + [(t2, g2)]
        points.sort()

        for j in range(len(points)-1):
            t_start, g_start = points[j]
            t_end, g_end = points[j+1]
            g_avg = (g_start + g_end) / 2
            tir_time[get_category(g_avg)] += t_end - t_start

    total = sum(tir_time.values())
    return {k: round((v/total)*100, 2) for k,v in tir_time.items()}

def combine_and_plot_full(results_dir, save_path):
    bg_values_all = []
    time_values_all = []

    plt.figure(figsize=(24, 10))

    for day in range(1, 15):
        folder = f"scenario_day_{day}_patient_3"
        json_bg = os.path.join(results_dir, folder, "bg_output.json")
        json_settings = os.path.join(results_dir, folder, "simulation_settings.json")

        
        with open(json_bg, 'r') as f:
            bg = json.load(f)["bg_mgdl"]
        t = [(day-1)*1440 + i for i in range(len(bg))]
        bg_values_all.extend(bg)
        time_values_all.extend(t)

        
        with open(json_settings, 'r') as f:
            settings = json.load(f)

        # heart_rate
        hr = settings["inputs"].get("heart_rate")
        if hr:
            hr_times = hr["start_time"][0]
            hr_mags = hr["magnitude"][0]
            hr_times = [(day-1)*24 + tt/60 for tt in hr_times]
            plt.fill_between(hr_times, hr_mags, color='pink', alpha=0.3, label="Heart rate [BPM]" if day == 1 else "")

        # bolus
        bolus = settings["inputs"].get("bolus_insulin")
        if bolus:
            for mag, tt in zip(bolus["magnitude"][0], bolus["start_time"][0]):
                global_t = (day-1)*24 + tt/60
                plt.arrow(global_t, 0, 0, mag, head_width=0.5, head_length=5, color='green', label="Bolus [U]" if day == 1 else "")

        # meal carb
        meal = settings["inputs"].get("meal_carb")
        if meal:
            for mag, tt in zip(meal["magnitude"][0], meal["start_time"][0]):
                global_t = (day-1)*24 + tt/60
                plt.arrow(global_t, 0, 0, mag, head_width=0.3, head_length=5, color='purple', label="Meal carb [g]" if day == 1 else "")

        # snack carb
        snack = settings["inputs"].get("snack_carb")
        if snack:
            for mag, tt in zip(snack["magnitude"][0], snack["start_time"][0]):
                global_t = (day-1)*24 + tt/60
                plt.arrow(global_t, 0, 0, mag, head_width=0.3, head_length=5, color='gray', label="Snack carb [g]" if day == 1 else "")

        # running
        run_start = settings["input_generation"]["running_start_time"]
        run_dur = settings["input_generation"]["running_duration"]
        for s, d in zip(run_start, run_dur):
            if s != "00:00":
                h, m = map(int, s.split(":"))
                global_t = (day-1)*24 + h + m/60
                plt.axvspan(global_t, global_t + d/60, color='orange', alpha=0.2, label="Running" if day == 1 else "")

        # cycling
        cycling_label_added = False
        cyc_start = settings["input_generation"]["cycling_start_time"]
        cyc_dur = settings["input_generation"]["cycling_duration"]
        for s, d in zip(cyc_start, cyc_dur):
            if s != "00:00":
                h, m = map(int, s.split(":"))
                global_t = (day - 1) * 24 + h + m / 60
                if not cycling_label_added:
                    plt.axvspan(global_t, global_t + d / 60, color='green', alpha=0.2, label="Cycling")
                    cycling_label_added = True
                else:
                    plt.axvspan(global_t, global_t + d / 60, color='green', alpha=0.2)

    
    time_h = np.array(time_values_all) / 60
    bg_arr = np.array(bg_values_all)
    plt.plot(time_h, bg_arr, color=[0.69, 0.235, 0.129], linewidth=1.5)

    # TIR
    tir = calculate_TIR(bg_arr, time_h*60)
    tir_text = "\n".join([f"{k}: {v}%" for k, v in tir.items()])
    plt.text(0.99, 0.99, tir_text, transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7))

    plt.axhline(70, linestyle='--', color='blue', label="70 mg/dL")
    plt.axhline(180, linestyle='--', color='purple', label="180 mg/dL")
    plt.xlabel("Time [h]")
    plt.ylabel("Magnitude")
    plt.title("14-Day Simulation for patient 3", fontsize=16, pad=20)
    plt.xlim([0, 14*24])
    plt.xticks(np.arange(0, 337, 24))
    plt.ylim([0, 250])
    plt.yticks(np.arange(0, 251, 50))
    plt.grid()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()

if __name__ == "__main__":
    results_dir = "/Users/aurora0926/my_project/py-mgipsim-main/SimulationResults"
    save_path = os.path.join(results_dir, "combined_14day_fullsignals.png")
    combine_and_plot_full(results_dir, save_path)
