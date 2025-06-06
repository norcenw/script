import shutil
import re
import json
import pandas as pd
import os

# Input string with incorrect formatting
json1_str = """
{positive_tolerance_error_signal_1=5.0, post_heating_time=50.0, weld_to_post_heating_time=50.0, positive_tolerance_error_signal_3=5.0, positive_tolerance_error_signal_2=5.0, start_temper_time=0.0, control_mode=2.0, positive_percentage_error_current=2.0, pre_heating_power=0.0, average_force=1976.0, pre_heating_time=50.0, length_temper_time=0.0, control_signal_2=2.0, control_signal_1=1.0, average_stroke=5.02, control_signal_3=3.0, current=10.0, ending_stroke=1.0, pre_heating_to_weld_time=50.0, secondary_voltage=2.68, slope_down_time=0.0, pressure_time=200.0, power=35.2, pre_heating_current=5.0, release_time=0.0, negative_percentage_error_current=2.0, negative_tolerance_error_signal_1=5.0, weld_mode=4.0, negative_tolerance_error_signal_3=5.0, negative_tolerance_error_signal_2=5.0, initial_force=0.0, hold_time=200.0, counter=1.0, slope_up_time=0.0, maximum_percentage_power_change=20.0, post_heating_power=0.0, reference_energy=6.43, post_heating_current=7.0, approaching_time=200.0, blanking_time=0.0, pulses=1.0, interval=0.0, average_resistance=269.0, time=200.0, average_energy=0.0, ending_force=5.0}
"""

# Step 1: Fix the formatting
fixed_json1_str = re.sub(r"(\w+)=([^,{}]+)", r'"\1": \2', json1_str.strip()[1:-1])
fixed_json1_str = "{" + fixed_json1_str + "}"

# Parse JSON
try:
    formatted_json1 = json.loads(fixed_json1_str)
except json.JSONDecodeError as e:
    print("JSON formatting failed:", e)
    print(fixed_json1_str)  # Debug output
    raise

# Second JSON object
json2 = {"weld_mode":"4.0","current":"10.0","time":"200.0","positive_tolerance_error_signal_1":"5.0","post_heating_time":"50.0","weld_to_post_heating_time":"50.0","positive_tolerance_error_signal_3":"5.0","positive_tolerance_error_signal_2":"5.0","start_temper_time":"0.0","control_mode":"2.0","positive_percentage_error_current":"2.0","pre_heating_power":"0.0","average_force":"1976.0","pre_heating_time":"50.0","length_temper_time":"0.0","control_signal_2":"2.0","control_signal_1":"1.0","average_stroke":"5.02","control_signal_3":"3.0","ending_stroke":"1.0","pre_heating_to_weld_time":"50.0","secondary_voltage":"2.68","slope_down_time":"0.0","pressure_time":"200.0","power":"35.2","pre_heating_current":"5.0","release_time":"0.0","negative_percentage_error_current":"2.0","negative_tolerance_error_signal_1":"5.0","negative_tolerance_error_signal_3":"5.0","negative_tolerance_error_signal_2":"5.0","initial_force":"0.0","hold_time":"200.0","counter":"1.0","slope_up_time":"0.0","maximum_percentage_power_change":"20.0","post_heating_power":"0.0","reference_energy":"6.43","post_heating_current":"7.0","approaching_time":"200.0","blanking_time":"0.0","pulses":"1.0","interval":"0.0","average_resistance":"269.0","average_energy":"0.0","ending_force":"5.0","id_ctrl":"1422b83740b89729","id_prog":"1"}
# Compare keys and values
comparison_data = []
for key in sorted(set(formatted_json1.keys()).union(json2.keys())):
    json1_value = formatted_json1.get(key, "MISSING")
    json2_value = json2.get(key, "MISSING")

    # Normalize numerical values for comparison
    try:
        json1_value_normalized = float(json1_value) if isinstance(json1_value, (int, float, str)) and str(json1_value).replace('.', '', 1).isdigit() else json1_value
    except ValueError:
        json1_value_normalized = json1_value

    try:
        json2_value_normalized = float(json2_value) if isinstance(json2_value, (int, float, str)) and str(json2_value).replace('.', '', 1).isdigit() else json2_value
    except ValueError:
        json2_value_normalized = json2_value

    status = (
        "EQUAL" if json1_value_normalized == json2_value_normalized else 
        "DIFFERENT" if key in formatted_json1 and key in json2 else 
        "MISSING"
    )

    comparison_data.append({
        "Key": key,
        "Status": status,
        "JSON1 Value": json1_value,
        "JSON2 Value": json2_value,
    })

# Create a dataframe for comparison
comparison_df = pd.DataFrame(comparison_data)

# Define directory path
directory = "C:/Users/weiye.norcen/Desktop/compare"
os.makedirs(directory, exist_ok=True)  # Ensure directory exists

# Save CSV file
file_path = os.path.join(directory, "json_key_comparison.csv")
comparison_df.to_csv(file_path, index=False, sep=';')

print(f"CSV file 'json_key_comparison.csv' created successfully in '{directory}' directory.")
print(comparison_df)
