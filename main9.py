import argparse
import logging
import json
import sys
import re
import solcx

import engine

def compile_solidity_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    version = extract_version(get_solidity_version(source_code))
    print(version)
    if version not in solcx.get_installed_solc_versions():
        solcx.install_solc(version, show_progress=True)

    compiled_code = solcx.compile_source(
        source_code,
        solc_version=version,
        output_values=["bin-runtime"]
    )

    return compiled_code[list(compiled_code.keys())[0]]['bin-runtime']

def extract_version(version_string):
    version_string = re.sub(r'^[<>=^]+', '', version_string)
    pattern = re.compile(r'\b\d+\.\d+\.\d+\b')
    match = re.search(pattern, version_string)
    if match:
        return match.group(0)
    else:
        return None

def get_solidity_version(source_code):
    version_regex = r'pragma solidity ([><^]?=?\s?\^?\s?(\d+\.\d+\.\d+))(\s?[<]?=?\s?\^?\s?(\d+\.\d+\.\d+))?'
    match = re.search(version_regex, source_code)
    if match:
        return match.group(1)
    else:
        raise ValueError("Solidity version not specified in the source code.")

def main() -> None:
    logging.disable()
    args = parse_args()
    if args.file.endswith('.sol'):  # Check if it's a Solidity file
        hexcode = compile_solidity_file(args.file)
        bytecode = bytes.fromhex(hexcode)
    else:
        bytecode = read_bytecode(args.file)

    engine_ = engine.Engine(bytecode)
    report = engine_.run()
    output(args, engine_, report)

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
