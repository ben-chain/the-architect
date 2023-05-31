import os
import shutil
import json

def load_phase_file(number):
    # Format the integer as a two-digit string
    formatted_number = str(number).zfill(2)

    # Search for files in the '/phases' folder
    folder_path = "./phases"
    files = os.listdir(folder_path)

    # Find the matching file
    matching_files = [file for file in files if file.startswith(formatted_number)]

    if matching_files:
        # Load the first matching file
        file_path = os.path.join(folder_path, matching_files[0])
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    else:
        print(f"No matching file found for number {formatted_number}.")
        return None

def get_run_num():
    runs_folder = "./runs"
    if not os.path.exists(runs_folder):
        os.makedirs(runs_folder)

    run_dirs = [d for d in os.listdir(runs_folder) if os.path.isdir(os.path.join(runs_folder, d))]
    existing_runs = [int(d) for d in run_dirs if d.isdigit()]
    current_run = max(existing_runs) + 1 if existing_runs else 0

    return current_run

def write_phase_output(phase_output_full, phase_output_structured, phase_num, run_num):
    # Format run_num to have three characters
    run_num_formatted = f"{run_num:03d}"

    # Format phase_num to have two characters
    phase_num_formatted = f"{phase_num:02d}"

    # Create the directory path for the run
    run_dir = os.path.join(".", "runs", run_num_formatted)

    # Create the directory if it doesn't exist
    os.makedirs(run_dir, exist_ok=True)

    # Create the file path for the phase output
    file_path_full = os.path.join(run_dir, f"phase_{phase_num_formatted}_full.txt")
    file_path_structured = os.path.join(run_dir, f"phase_{phase_num_formatted}_structured.json")

    # Write the full phase output to the text file
    with open(file_path_full, "w") as file:
        file.write(phase_output_full)

    # Write the structured phase output to the JSON file
    with open(file_path_structured, "w") as file:
        json.dump(phase_output_structured, file)

def get_phase_output(phase_num, run_num):
    # Format run_num to have three characters
    run_num_formatted = f"{run_num:03d}"

    # Format phase_num to have two characters
    phase_num_formatted = f"{phase_num:02d}"

    # Create the directory path for the run
    run_dir = os.path.join(".", "runs", run_num_formatted)

    # Create the file path for the JSON object
    json_file_path = os.path.join(run_dir, f"phase_{phase_num_formatted}_structured.json")

    # Read the content of the JSON file
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    return json_data

def copy_prev_phase_outputs(phase_num, prev_run_num, new_run_num):
    # Format prev_run_num and new_run_num to have three characters
    prev_run_num_formatted = f"{prev_run_num:03d}"
    new_run_num_formatted = f"{new_run_num:03d}"

    # Create the directory paths for the previous and new runs
    prev_run_dir = os.path.join(".", "runs", prev_run_num_formatted)
    new_run_dir = os.path.join(".", "runs", new_run_num_formatted)

    # Create the new run directory if it doesn't exist
    os.makedirs(new_run_dir, exist_ok=True)

    # Copy the phase outputs from the previous run to the new run
    for phase in range(1, phase_num + 1):
        # Format phase number to have two characters
        phase_formatted = f"{phase:02d}"

        # Create the file paths for the phase outputs
        prev_file_path = os.path.join(prev_run_dir, f"phase_{phase_formatted}_structured.json")
        new_file_path = os.path.join(new_run_dir, f"phase_{phase_formatted}_structured.json")

        # Copy the file
        shutil.copy(prev_file_path, new_file_path)

def update_prev_phase_outputs(up_to_phase, prev_phase_outputs, run_num, phases):
    for phase_number in range(1, up_to_phase + 1):
        phase_string, phase_function = phases[phase_number]
        phase_output = get_phase_output(phase_number, run_num)
        prev_phase_outputs[phase_string] = phase_output
    return prev_phase_outputs

def get_phase_num(string, the_phases):
    for number, (name, _) in the_phases.items():
        if name == string:
            return number
    return None  # Return None if the string is not found