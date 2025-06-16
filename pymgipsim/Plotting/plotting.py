import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pymgipsim.Utilities.Scenario import scenario
from pymgipsim.Utilities.units_conversions_constants import UnitConversion
import pymgipsim.VirtualPatient.Models as Models


""" 
#######################################################################################################################
Model States
#######################################################################################################################
"""

def plot_subject_response(loaded_model, scenario:scenario, patientidx, tir_result=None):
    mpl.rcParams["font.size"] = 12
    fig = plt.figure(figsize = (20, 6))
    cho_color = [0.259, 0.125, 0.329]
    insulin_color = [0, 0.639, 0.224]
    snack_color = [0.7, 0.7, 0.7]
    glucose_color = [0.69, 0.235, 0.129]
    sglt2i_color = [0.902, 0.941, 0]
    heart_rate_color = [1, 0.498, 0.545]#[1, 0.325, 0.392]
    time_axis = loaded_model.time.as_unix/60.0
    arrow_width = 0.5
    arrow_height = 5

    
    glucose = np.zeros_like(loaded_model.states.as_array[:, loaded_model.glucose_state, :])

    match loaded_model.name:
        case Models.T1DM.ExtHovorka.Model.name:
            glucose = UnitConversion.glucose.concentration_mmolL_to_mgdL(loaded_model.states.as_array[patientidx, loaded_model.glucose_state, :] / loaded_model.parameters.VG[patientidx])
                
        case Models.T1DM.IVP.Model.name:
            glucose = loaded_model.states.as_array[patientidx, loaded_model.glucose_state, :]

    glucose_unit = "mg/dL"


    try:
        hr_times = scenario.inputs.heart_rate.start_time[patientidx]
        hr_magnitudes = scenario.inputs.heart_rate.magnitude[patientidx]
        hr_times = np.asarray(hr_times) / 60
        hr_magnitudes = np.asarray(hr_magnitudes)
        hr_times = np.append(hr_times, time_axis[-1])
        hr_magnitudes = np.append(hr_magnitudes, hr_magnitudes[-1])
        plt.fill_between(hr_times, hr_magnitudes, color = heart_rate_color, label='Heart rate [BPM]', alpha=0.4)
    except:
        pass

    try:
        if scenario.controller.name == "OpenLoop" or scenario.controller.name == "StochasticOpenLoop":
            label = True
            for magnitude,start_time in zip(scenario.inputs.bolus_insulin.magnitude[patientidx], scenario.inputs.bolus_insulin.start_time[patientidx]):
                if label:
                    label = False
                    plt.arrow(start_time/60.0, 0, 0, magnitude,head_width=arrow_width,head_length=arrow_height, facecolor=insulin_color, edgecolor=insulin_color, label='Bolus [U]')
                else:
                    plt.arrow(start_time/60.0, 0, 0, magnitude, head_width=arrow_width, head_length=arrow_height,facecolor=insulin_color, edgecolor=insulin_color)
        else:
            match loaded_model.name:
                case Models.T1DM.ExtHovorka.Model.name:
                    plt.fill_between(time_axis, UnitConversion.insulin.mUmin_to_Uhr(loaded_model.inputs.as_array[patientidx, 3, :]), color=insulin_color, label='Insulin infusion rate [U/hr]')
                case Models.T1DM.IVP.Model.name:
                    plt.fill_between(time_axis, UnitConversion.insulin.uUmin_to_Uhr(loaded_model.inputs.as_array[patientidx, 1, :]),color=insulin_color, label='Insulin infusion rate [U/hr]')
    except:
        pass
##
##    try:
##        running_starts = scenario.input_generation.running_start_time
##        running_durations = scenario.input_generation.running_duration
##
##        if running_starts and isinstance(running_starts[0], str):
##            def time_str_to_min(tstr):
##                hour, minute = map(int, tstr.split(":"))
##                return hour * 60 + minute
##
##            running_starts = [time_str_to_min(t) for t in running_starts]
##
##        running_label_added = False
##        for start, duration in zip(running_starts, running_durations):
##            if start == 0 and duration == 0:
##                continue
##            start_hour = start / 60
##            end_hour = (start + duration) / 60
##            if not running_label_added:
##                plt.axvspan(start_hour, end_hour, color='orange', alpha=0.2, label='Running')
##                running_label_added = True
##            else:
##                plt.axvspan(start_hour, end_hour, color='orange', alpha=0.2)
##
##        cycling_starts = scenario.input_generation.cycling_start_time
##        cycling_durations = scenario.input_generation.cycling_duration
##
##        if cycling_starts and isinstance(cycling_starts[0], str):
##            def time_str_to_min(tstr):
##                hour, minute = map(int, tstr.split(":"))
##                return hour * 60 + minute
##
##            cycling_starts = [time_str_to_min(t) for t in cycling_starts]
##
##        cycling_label_added = False
##        for start, duration in zip(cycling_starts, cycling_durations):
##            if start == 0 and duration == 0:
##                continue
##            start_hour = start / 60
##            end_hour = (start + duration) / 60
##            if not cycling_label_added:
##                plt.axvspan(start_hour, end_hour, color='green', alpha=0.2, label='Cycling')
##                cycling_label_added = True
##            else:
##                plt.axvspan(start_hour, end_hour, color='green', alpha=0.2)
##
##    except Exception as e:
##        print(f"[Warning] Failed to plot exercise zones: {e}")

    try:
        running_starts = np.array(scenario.input_generation.running_start_time)
        running_durations = np.array(scenario.input_generation.running_duration)
        cycling_starts = np.array(scenario.input_generation.cycling_start_time)
        cycling_durations = np.array(scenario.input_generation.cycling_duration)

        running_label_added = False
        for day_idx in range(running_starts.shape[1]):
            start = running_starts[0, day_idx]
            duration = running_durations[0, day_idx]
            if start == 0 and duration == 0:
                continue
            day_offset = day_idx * 24
            start_hour = (start / 60) + day_offset
            end_hour = (start + duration) / 60 + day_offset
            if not running_label_added:
                plt.axvspan(start_hour, end_hour, color='orange', alpha=0.2, label='Running')
                running_label_added = True
            else:
                plt.axvspan(start_hour, end_hour, color='orange', alpha=0.2)

        cycling_label_added = False
        for day_idx in range(cycling_starts.shape[1]):
            start = cycling_starts[0, day_idx]
            duration = cycling_durations[0, day_idx]
            if start == 0 and duration == 0:
                continue
            day_offset = day_idx * 24
            start_hour = (start / 60) + day_offset
            end_hour = (start + duration) / 60 + day_offset
            if not cycling_label_added:
                plt.axvspan(start_hour, end_hour, color='green', alpha=0.2, label='Cycling')
                cycling_label_added = True
            else:
                plt.axvspan(start_hour, end_hour, color='green', alpha=0.2)

        if running_label_added or cycling_label_added:
            plt.legend()

    except Exception as e:
        print(f"[Warning] Failed to plot exercise zones: {e}")


    try:
        label = True
        for magnitude,start_time in zip(scenario.inputs.meal_carb.magnitude[patientidx], scenario.inputs.meal_carb.start_time[patientidx]):
            if label:
                plt.arrow(start_time/60.0, 0, 0, magnitude,head_width=arrow_width, head_length=arrow_height, facecolor=cho_color, edgecolor=cho_color, label='Meal carb [g]')
                label = False
            else:
                plt.arrow(start_time/60.0, 0, 0, magnitude, head_width=arrow_width, head_length=arrow_height,facecolor=cho_color, edgecolor=cho_color)
    except:
        pass

    try:
        label = True
        for magnitude,start_time in zip(scenario.inputs.snack_carb.magnitude[patientidx], scenario.inputs.snack_carb.start_time[patientidx]):
            if label:
                label = False
                plt.arrow(start_time/60.0, 0, 0, magnitude,head_width=arrow_width,head_length=arrow_height, facecolor=snack_color, edgecolor=snack_color, label='Snack carb [g]')
            else:
                plt.arrow(start_time/60.0, 0, 0, magnitude, head_width=arrow_width,head_length=arrow_height, facecolor=snack_color, edgecolor=snack_color)
    except:
        pass
    try:
        label = True
        for magnitude,start_time in zip(scenario.inputs.sgl2i.magnitude[patientidx], scenario.inputs.sgl2i.start_time[patientidx]):
            if magnitude>0.0:
                if label:
                    label = False
                    plt.arrow(start_time/60.0, 0, 0, magnitude,head_width=arrow_width,head_length=arrow_height, facecolor=sglt2i_color, edgecolor=sglt2i_color, label='SGLT2i [mg]')
                else:
                    plt.arrow(start_time/60.0, 0, 0, magnitude, head_width=arrow_width, head_length=arrow_height,facecolor=sglt2i_color, edgecolor=sglt2i_color)
    except:
        pass

    plt.plot(time_axis, glucose, color=glucose_color, label="Blood glucose [" + glucose_unit + "]")

    plt.axhline(y=70, color='blue', linestyle='--', linewidth=1, label='Lower BG Threshold (70 mg/dL)')
    plt.axhline(y=180, color='purple', linestyle='--', linewidth=1, label='Upper BG Threshold (180 mg/dL)')

    plt.grid()
    plt.xlabel('Time [h]')
    plt.ylabel('Magnitude')
    plt.xlim([0, time_axis[-1]])
    if np.max(glucose) < 250.0:
        plt.ylim([0.0, 250.0])
    else:
        plt.ylim([0.0, np.max(glucose)])

    try:
        plt.title(scenario.patient.model.name + " " + scenario.patient.files[patientidx].replace(".json", ""))
    except:
        pass

    handles, labels = plt.gca().get_legend_handles_labels()
    filtered = [(h, l) for h, l in zip(handles, labels) if l and l.strip() != ""]
    if filtered:
        plt.legend(*zip(*filtered), loc='upper left', bbox_to_anchor=(1.05, 1.0), borderaxespad=0.)

    plt.tight_layout()
    plt.subplots_adjust(right=0.75)

    if tir_result is not None:
        tir_text = f"TIR: {tir_result['Target']}%\n"
        tir_text += f"VL: {tir_result['Very Low']}%  L: {tir_result['Low']}%\n"
        tir_text += f"H: {tir_result['High']}%  VH: {tir_result['Very High']}%"

        plt.text(
            0.97, 0.97, tir_text,
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(facecolor='white', edgecolor='gray', alpha=0.7)
        )
    return fig



def plot_bgc(time, glucose, figsize, figcolor):
    """
    Plot the blood glucose concentration (BGC) over time.

    Parameters:
    - formatted_time: np.ndarray
        Time array for plotting.
    - formatted_glucose: np.ndarray
        2D array containing blood glucose data for different subjects.

    Returns:
    - fig: matplotlib.figure.Figure
        The created matplotlib figure.


    """

    mpl.rcParams["font.size"] = 18
    fig = plt.figure(figsize = figsize)

    glucose_mean = glucose.mean(axis=0)
    glucose_std = glucose.std(axis=0)

    time = time/60.0

    plt.plot(time, glucose_mean, color=figcolor, linewidth=1.8)#[0.961*0.5, 0.867*0.5, 0.208*0.5]
    plt.fill_between(time, glucose_mean - glucose_std, glucose_mean + glucose_std, alpha=0.4, color=figcolor)#[0.961, 0.867, 0.208],label='Without SGL2Ti'

    plt.legend()
    plt.grid()
    plt.title("Blood glucose response")
    plt.xlabel('Time [h]')
    plt.ylabel('Blood glucose [mg/dL]')
    plt.ylim([50.0, 250.0])
    plt.xlim([0.0, time[-1]])

    return fig


def plot_all_states(time, all_states, state_units, state_names, figsize, figcolor):
    """
    Plot all states over time in subplots.

    Parameters:
    - formatted_time: np.ndarray
        Time array for plotting.
    - all_states: np.ndarray
        4D array containing state data for different days and variables.
    - state_names: list
        List of state variable names.
    - state_units: list
        List of units corresponding to state variables.

    Returns:
    - fig: matplotlib.figure.Figure
        The created matplotlib figure.
    """
    mpl.rcParams["font.size"] = 10
    rows = int(np.sqrt(all_states.shape[1]))
    cols = rows

    fig, axes = plt.subplots(rows, cols, figsize=figsize)

    state_num = 0
    for row_num in range(rows):
        for col_num in range(cols):
            mean = all_states[:, state_num, :].mean(axis=0)
            std = all_states[:, state_num, :].std(axis=0)

            axes[row_num, col_num].plot(time, mean, color=figcolor)
            axes[row_num, col_num].fill_between(time, mean - std, mean + std, alpha=0.4, color=figcolor)
            axes[row_num, col_num].set_xlabel('Time (h)')
            axes[row_num, col_num].set_ylabel(state_units[state_num])
            axes[row_num, col_num].set_title(state_names[state_num])

            state_num += 1

    plt.xlabel('Time (h)')

    plt.tight_layout()

    return fig


def plot_bw(time, bw_state, bw_unit, state_name, figsize, figcolor):

    fig = plt.figure(figsize = figsize)

    mean = bw_state.mean(axis = 0)[0]
    std = bw_state.std(axis = 0)[0]

    plt.plot(time, mean, color=figcolor)
    plt.fill_between(time, mean - std, mean + std, alpha=0.4, color=figcolor)

    plt.xlabel('Days')
    plt.ylabel(f'{state_name} ({bw_unit})')
    plt.ylim((0.9 * np.min(mean - std), 1.1 * np.max(mean + std)))

    return fig


""" 
#######################################################################################################################
Inputs
#######################################################################################################################
"""

def plot_input_signals(time, input_array, input_names):

    num_inputs = input_array.shape[1]

    if num_inputs > 1:
        num_rows = np.ceil(np.sqrt(num_inputs)).astype(int)
        num_cols = num_rows.astype(int)

    fig, axes = plt.subplots(num_rows, num_cols)

    input_num = 0
    for row in range(num_rows):
        for col in range(num_cols):

            if input_num < num_inputs:

                mean = input_array[:, input_num, :].mean(axis = 0)
                std = input_array[:, input_num, :].std(axis = 0)

                axes[row, col].plot(time, mean)
                axes[row, col].fill_between(time, mean - std, mean + std, alpha = 0.4)
                axes[row, col].set_xlabel('Time (min)')
                axes[row, col].set_title(f"{input_names[input_num]}")
                axes[row, col].set_ylim([0, 1.1*max(mean + std)])

            input_num += 1

    fig.tight_layout()

    return fig
