from packaging import version

def check_version(target, version_list):
    # Extract version strings from the given list
    extracted_versions = [str(v).split("'")[1] for v in version_list]

    # Convert to Version objects for comparison
    target_version = version.parse(target)
    versions = [version.parse(v) for v in extracted_versions]

    # Check if the target version is in the list
    return target_version in versions

# Your target version string
target_version = "0.1.5"

# Your list of versions
versions_list = ["<Version('0.8.23')>", "<Version('0.6.1')>", "<Version('0.5.0')>", 
                 "<Version('0.4.26')>", "<Version('0.4.24')>", "<Version('0.4.23')>", 
                 "<Version('0.4.22')>", "<Version('0.4.18')>", "<Version('0.4.12')>"]

# Check if the version is in the list
is_in_list = check_version(target_version, versions_list)
print(f"Version {target_version} is in the list: {is_in_list}")
