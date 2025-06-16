# Extended Cambridge Model – Continuous Simulation

## Key Features / Code Modifications

- **Activity Settings Enhancement**
  - Enabled recording of activity inputs (e.g. running, cycling) in continuous simulations
  - Adjusted input processing for multi-day activity sequences  

- **Visualization Updates**
  - Added running and cycling markers to output plots  

- **New Metric Calculation**
  - Automated calculation of Time in Range (TIR) for blood glucose  

## How to Run

Run the 14-day simulation with:

```bash
python manual_script.py --settings_file pymgipsim/Settings/DefaultSettings/scenario_continuous100.json
