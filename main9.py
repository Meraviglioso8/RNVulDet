import argparse
import logging
import json
import sys
import re
import solcx
import engine
from packaging import version
import time

def check_version(target, version_list):
    # Convert the target version string to a Version object
    target_version = version.Version(target)

    # Check if the target version is in the list
    return target_version in version_list

def find_pragma_line(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("pragma solidity"):
                return line.strip()  # Returns the pragma line without any leading/trailing whitespace
    return None  # Return None if no pragma line is found

def is_version_greater(extracted_version, max_version='0.8.23'):
    # Remove 'v' prefix and compare versions
    return version.parse(extracted_version) > version.parse(max_version)

def increment_version(version, existing_versions):
    major, minor, patch = map(int, version.split('.'))
    # Increment the patch version and check if it exists.
    patch += 1
    new_version = f"{major}.{minor}.{patch}"
    if new_version in existing_versions:
        return new_version
    else:
        # If the incremented patch version does not exist, increment the minor version
        # and reset the patch version to 0.
        return f"{major}.{minor+1}.0"

def decrement_version(version, existing_versions):
    major, minor, patch = map(int, version.split('.'))
    # Increment the patch version and check if it exists.
    patch -= 1
    new_version = f"{major}.{minor}.{patch}"
    if new_version in existing_versions:
        return new_version
    else:
        # If the incremented patch version does not exist, increment the minor version
        # and reset the patch version to 0.
        return f"{major}.{minor-1}.23"

def extract_version(version_string):
    version_string = re.sub(r'^[<>=^]+', '', version_string)
    pattern = re.compile(r'\b\d+\.\d+\.\d+\b')
    match = re.search(pattern, version_string)
    if match:
        return match.group(0)
    else:
        return None
    
def get_solidity_version(first_line):
        match = re.search(r'pragma solidity\s*([^;]+)', first_line)
        if match:
            return match.group(1)
        else:
            return None

def compile_solidity_file(file_path):
    try:
        with open(file_path, 'r') as file:
            source_code = file.read()

        pragma_line = find_pragma_line(file_path)

        if not pragma_line:
            print("Pragma line not found.")
            return None

        with open('./versions.txt', 'r') as file:
            existing_versions=[line.strip() for line in file]

        pragma_version = get_solidity_version(pragma_line)

        if not pragma_version:
            print("Error extracting pragma version.")
            return None
        
        extracted_version =''
        

        if ">" in pragma_version and "<" not in pragma_version: # Only > 
            extracted_version_match = re.search(r'>\s*(\d+\.\d+\.\d+)', pragma_version)
            if extracted_version_match:
                extracted_version = extracted_version_match.group(1)
                extracted_version = increment_version(extracted_version, existing_versions)
            else:
                print("Error with > only")
                return
            
        elif "<" in pragma_version and ">" not in pragma_version: # Only <
            extracted_version_match = re.search(r'<\s*(\d+\.\d+\.\d+)', pragma_version)
            if extracted_version_match:
                extracted_version = extracted_version_match.group(1)
                extracted_version = decrement_version(extracted_version, existing_versions)
            else:
                print("Error with < only")
                return
        
        elif "<" in pragma_version and ">"  in pragma_version: # Also have < and >
            extracted_version = re.search(r'(>=|>|<=|<)\s*(\d+\.\d+\.\d+)\s*(>=|>|<=|<)\s*(\d+\.\d+\.\d+)', pragma_version)
            if extracted_version:
                first_operator, first_version, second_operator, second_version = extracted_version.groups()

                first_version = first_version.replace(first_operator, "").strip()
                second_version = second_version.replace(second_operator, "").strip()

                # Adjust the version based on the operator
                if first_operator in ['>=', '>']:
                    first_version = increment_version(first_version, existing_versions)
                    print("First version:", first_version)
                if second_operator in ['<=', '<']:
                    second_version = decrement_version(second_version, existing_versions)
                    print("Second version:", second_version)

                # Compare the versions
                if is_version_greater(first_version, second_version):
                    print("Error. Invalid Version Range.")
                    return
                else:
                    extracted_version = first_version
        # Continue with your logic using extracted_version

        else:
            print("Using pragma solidity in source code.")
            extracted_version = extract_version(pragma_version)

        if (is_version_greater(extracted_version)):
            print("Invalid compile version")
            return     

        if extracted_version not in solcx.get_installed_solc_versions():
            solcx.install_solc(extracted_version, show_progress=True)

        version = solcx.set_solc_version_pragma(extracted_version)

        print("Running...")

        print("Compile version using:",version)

        compiled_code = solcx.compile_source(
            source_code,
            solc_version=version,
            output_values=["bin-runtime"]
        )
    except Exception as e: 
        print("Error!:", e)
        return
    
    
    return compiled_code[list(compiled_code.keys())[0]]['bin-runtime']


def read_versions_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def main() -> None:
    start_time = time.time()
    logging.disable()
    args = parse_args()
    bytecode=''
    if args.file.endswith('.sol'):  # Check if it's a Solidity file
        hexcode = compile_solidity_file(args.file)

        if hexcode is not None:
            bytecode = bytes.fromhex(hexcode)
    else:
        bytecode = read_bytecode(args.file)

    engine_ = engine.Engine(bytecode)
    report = engine_.run()
    output(args, engine_, report)
    
    # Calculate the total runtime
    end_time = time.time()
    total_time = end_time - start_time
    print(f"The program ran for {total_time} seconds.")

def output(args, engine_: engine.Engine, report: bool) -> None:
    attr_names = (
        "conditions",
        "call_values",
        "to_addresses",
        "todo_keys",
    )

    res = {
        "is_reported": report,
        "steps": engine_.step,
    }
    for attr_name in attr_names:
        attr = getattr(engine_, attr_name)
        res[attr_name] = len(attr)

    if args.output is not None:
        with open(args.output, "w") as f:
            json.dump(res, f, indent=4)
    else:
        json.dump(res, sys.stdout, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(description="None")
    parser.add_argument(
        "file",
        help="file containing hex-encoded bytecode string",
        metavar="BYTECODE_FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output information in json format",
        metavar="OUTPUT_FILE",
    )

    args = parser.parse_args()

    return args


def read_bytecode(filename: str) -> bytes:
    with open(filename) as f:
        hex_code = f.read().strip().replace("0x", "").replace("0X", "")
    assert hex_code
    bytecode = bytes.fromhex(hex_code)
    return bytecode

if __name__ == "__main__":
    main()
