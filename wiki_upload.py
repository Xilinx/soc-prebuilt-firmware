# python3 wiki_upload.py --help
# python3 wiki_upload.py --type wiki_upload --release-version 2024.1 --build-path /proj/petalinux/2024.1/petalinux-v2024.1_04301119
# python3 wiki_upload.py --type git_upload --release-version 2024.1 --build-path /proj/petalinux/2024.1/petalinux-v2024.1_04301119

import os
import re
import shutil
import json
import argparse
import subprocess
import sys

# Load JSON data
json_data = '''
{
    "keys_values": {
        "vck190-versal":     "xilinx-vck190",
        "vek280-versal":     "xilinx-vek280",
        "vhk158-versal":     "xilinx-vhk158",
        "vmk180-versal":     "xilinx-vmk180",
        "vpk120-versal":     "xilinx-vpk120",
        "vpk180-versal":     "xilinx-vpk180",
        "zc702-zynq":        "xilinx-zc702",
        "zcu102-zynqmp":     "xilinx-zcu102",
        "zcu104-zynqmp":     "xilinx-zcu104",
        "zcu106-zynqmp":     "xilinx-zcu106",
        "zcu216-zynqmp":     "xilinx-zcu216",
        "vck190-xsct-versal":     "xilinx-vck190-xsct",
        "vek280-xsct-versal":     "xilinx-vek280-xsct",
        "vhk158-xsct-versal":     "xilinx-vhk158-xsct",
        "vmk180-xsct-versal":     "xilinx-vmk180-xsct",
        "vpk120-xsct-versal":     "xilinx-vpk120-xsct",
        "vpk180-xsct-versal":     "xilinx-vpk180-xsct",
        "zc702-xsct-zynq":        "xilinx-zc702-xsct",
        "zcu102-xsct-zynqmp":     "xilinx-zcu102-xsct",
        "zcu104-xsct-zynqmp":     "xilinx-zcu104-xsct",
        "zcu106-xsct-zynqmp":     "xilinx-zcu106-xsct",
        "zcu216-xsct-zynqmp":     "xilinx-zcu216-xsct"
    }
}
'''

# Argument parser setup
parser = argparse.ArgumentParser(description='Process BSP files.')
parser.add_argument('--type', help='Type of upload: wiki_upload or git_upload', required=True)
parser.add_argument('--release-version', help='Add the Release version', required=True)
parser.add_argument('--build-path', help='Path of the project', required=True)
args = parser.parse_args()

# Parse JSON data
parsed_json = json.loads(json_data)
key_value_pairs = parsed_json["keys_values"]

release = args.release_version
base_directory = args.build_path
upload_type = args.type

# Function to handle wiki upload
def wiki_upload(base_directory):
    # Check if build-path ends with "/logs/bsps"
    base_directory = os.path.join(base_directory, "logs/bsps")

    # Create a dictionary to hold checksums for all zip files
    all_checksums = {}

    # Iterate over key-value pairs
    for output_directory, bsp in key_value_pairs.items():
        bsp_versioned = f"{bsp}-{release}"
        bsp_versioned = os.path.join(bsp_versioned, "pre-built", "linux", "images")
        full_directory = os.path.join(base_directory, bsp_versioned).replace("\\", "/")

        # Extract relevant part from output_directory dynamically
        relevant_part = '-'.join(output_directory.split('-')[:-1])

        # Create target directory based on the JSON value
        target_directory = os.path.join(os.getcwd(), f"{bsp}-{release}_sdimage")
        os.makedirs(target_directory, exist_ok=True)

        # Copy license.manifest file if it exists
        license_manifest_path = os.path.join(base_directory, f"{bsp}-{release}", "license.manifest")
        license_manifest_missing = False
        if os.path.exists(license_manifest_path):
            shutil.copy(license_manifest_path, target_directory)
            print(f"Copied license.manifest to {target_directory}")
        else:
            print(f"License manifest file not found for {bsp}-{release}")
            license_manifest_missing = True

        # Copy README.md file if it exists
        readme_path = f"/proj/petalinux/{release}/wiki_readme/README.md"
        readme_missing = False
        if os.path.exists(readme_path):
            shutil.copy(readme_path, target_directory)
            print(f"Copied README.md to {target_directory}")
        else:
            print("README.md not found")
            readme_missing = True

        # Check if the full_directory exists before iterating over files
        if os.path.exists(full_directory):
            files_missing = False
            for filename in os.listdir(full_directory):
                if filename.endswith(".wic.xz"):
                    source_file = os.path.join(full_directory, filename)
                    if os.path.exists(source_file):
                        shutil.copy(source_file, target_directory)
                        print(f"Copied {filename} to {target_directory}")
                        subprocess.run(['unxz', os.path.join(target_directory, filename)])
                    else:
                        print(f"File {filename} not found in {full_directory}")
                        files_missing = True

            # Rename the target directory to match the desired zip file name
            new_target_directory = f"xilinx-v{release}_{relevant_part}_sdimage"
            os.rename(target_directory, new_target_directory)

            # Zip the directory if no files are missing
            if not (license_manifest_missing or readme_missing or files_missing):
                zip_file_name = f"xilinx-v{release}_{relevant_part}_sdimage.zip"
                subprocess.run(['zip', '-r', zip_file_name, new_target_directory])

                # Calculate md5sum
                md5_result = subprocess.run(['md5sum', zip_file_name], stdout=subprocess.PIPE, universal_newlines=True)
                checksum = md5_result.stdout.split()[0]
                all_checksums[zip_file_name] = checksum
                print(f"Checksum for {zip_file_name}: {checksum}")
            else:
                print("Skipping zip creation due to missing files.")
        else:
            print(f"Directory {full_directory} does not exist.")

    # Write all checksums and zip file names to a single .md5 file
    with open(f"all_sdimages_{release}.md5", 'w') as f:
        for zip_file, checksum in all_checksums.items():
            f.write(f"{checksum}  {zip_file}\n")
    print(f"Checksums for all sdimage files have been written to all_sdimages_{release}.md5")


# Function to handle git upload
def git_upload(base_directory):
    # Get the path to settings.sh dynamically 
    settings_sh_path = f"{base_directory}/tool/petalinux-v{release}-final/settings.sh" 
    print(f"Info : Petalinux tool path {settings_sh_path}")
    if not os.path.exists(settings_sh_path):
        print(f"ERROR: Petalinux tool path {settings_sh_path} is not accessable")
        sys.exit(1)

    # Check if build-path ends with "/logs/bsps"
    base_directory = os.path.join(base_directory, "logs/bsps")

    # Iterate over key-value pairs
    for output_directory, bsp in key_value_pairs.items():
        bsp_versioned = f"{bsp}-{release}"
        bsp_base_dir = os.path.join(base_directory,bsp_versioned)
        print (f"bsp base dir {bsp_base_dir}")
        #full_directory = os.path.join(base_directory, bsp_versioned).replace("\\", "/")
        full_directory = os.path.join(base_directory, bsp_versioned,"pre-built", "linux", "images")
        print (f"full path {full_directory}")
        if not os.path.exists(full_directory):
            print(f"WARNING Directory {full_directory} does not exist.")
            continue

        files = os.listdir(full_directory)
        output_folder = os.path.join(os.getcwd(), output_directory)
        os.makedirs(output_folder, exist_ok=True)

        if 'bootgen.bif' not in files:
            print(f"WARNING bootgen.bif file not found in the {bsp} directory.")
            continue

        with open(os.path.join(full_directory, 'bootgen.bif'), 'r') as f:
            bif_content = f.read()

        shutil.copy(os.path.join(full_directory, 'bootgen.bif'), output_folder)
        print(f"Copying bootgen.bif to {output_folder}")

        # Extract file paths from bif content based on the structure
        if re.search(r'\[[^\]]*\]', bif_content):
            files_from_bif = re.findall(r'(?:\[[^\]]*\]\s*)?([\w./-]+(?:\.[\w]+)+)', bif_content)
        else:
            # Pattern to match filenames with the specific 'file=' prefix
            files_from_bif = re.findall(r'file=([^\s}]+)', bif_content)
        print (f" Info : Files extraced from bif file {files_from_bif}")
        total_files_copied = 0
        for file in files_from_bif:
            if '/' in file:
                file_path = os.path.join(bsp_base_dir, file)
            else:
                file_path = os.path.join(full_directory, file)
            target_file_name = os.path.basename(file)
            target_file_path = os.path.join(output_folder, target_file_name)
            
            if os.path.exists(file_path):
                shutil.copy(file_path, target_file_path)
                total_files_copied += 1
                print(f"Copying {file_path} to {target_file_path}")
            else:
                for root, dirs, _ in os.walk(base_directory):
                    if target_file_name in dirs or target_file_name in os.listdir(root):
                        possible_path = os.path.join(root, target_file_name)
                        if os.path.exists(possible_path):
                            shutil.copy(possible_path, target_file_path)
                            total_files_copied += 1
                            print(f"Copying {possible_path} to {target_file_path}")
                            break
                else:
                    print(f"File {file_path} not found.")
                    continue

        # Update the bif content with relative paths
        if re.search(r"file=.*?\/([^\/]+)\s*}", bif_content):
            pattern = r"file=.*?\/([^\/]+)$"
            bif_content_updated = re.sub(pattern, r"file=\1", bif_content, flags=re.MULTILINE)
            # print(bif_content_updated)
        else:
            pattern = r"\b\S+\/([^\/\s]+\.\w+)\b"
            bif_content_updated = re.sub(pattern, r"\1", bif_content)
            # print(bif_content_updated)
        
        with open(os.path.join(output_folder, 'bootgen.bif'), 'w') as f:
            f.write(bif_content_updated)
        print(f"Updated bootgen.bif in {output_folder}")

        total_files_listed = len(files_from_bif)
        print(f"Total files listed in bootgen.bif: {total_files_listed}")
        print(f"Total files copied: {total_files_copied}")

        if total_files_copied == total_files_listed:
            print("All files listed in bootgen.bif were successfully copied.")
        else:
            print("Some files listed in bootgen.bif were not copied.")

        # Check for .dtb files in the output folder and convert them to .dts
        dtb_files = [file for file in os.listdir(output_folder) if file.endswith('.dtb')]
        if dtb_files:
            for dtb_file in dtb_files:
                ip=os.path.join(output_folder, dtb_file)
                op=os.path.join(output_folder, "system.dts")
                shell_command = (
                'bash -c "source {settings_sh_path};'
                '$PETALINUX/sysroots/x86_64-petalinux-linux/usr/bin/dtc -I dtb -O dts -o {op} {ip}"'
                ).format(settings_sh_path=settings_sh_path,ip=ip,op=op)
            try:
                # Execute the shell command
                subprocess.check_call(shell_command, shell=True)
            except subprocess.CalledProcessError as e:
                print("Command '%s' returned non-zero exit status %d" % (e.cmd, e.returncode))
                sys.exit(1)
        else:
            print("No .dtb files found in the output folder.")

# Invoke the appropriate function based on the upload type
if upload_type == 'wiki_upload':
    wiki_upload(base_directory)
elif upload_type == 'git_upload':
    git_upload(base_directory)
else:
    print("Invalid upload type. Use 'wiki_upload' or 'git_upload'.")
