# Remote Audit System

This project provides a complete remote auditing workflow consisting of:

- A PHP backend that receives files from a remote audit client.
- A Python script (convertible to an EXE) that collects system information, uploads it to the server, and removes itself after execution.
- A simple web interface that displays received files in real time.

---

## Overview

The system is designed for environments where a remote machine must execute an audit tool, send the results to a central server, and leave no traces behind. The server stores the received files and displays them through a lightweight interface.

---

## Features

### Server (PHP)
- Receives uploaded files via POST (`files[]`).
- Stores files in `audit_results/`.
- Creates redundant copies in `audit_copies/`.
- Displays received files through an auto‑refreshing iframe.
- Automatically triggers download of the audit executable (`auditor.exe`).

### Client (Python/EXE)
- Collects system information using Windows commands (`wmic`, `reg`, `ipconfig`).
- Generates temporary `.txt` and `.csv` audit files.
- Uploads the files to the server using multipart POST.
- Deletes temporary files after successful upload.
- Deletes itself after execution.

---

## Directory Structure

```
/audit_results      Files received from the client
/audit_copies       Redundant copies of received files
auditor.php         Main interface and upload handler
download.php        Forces download of auditor.exe
list_files.php      Displays files in audit_results and audit_copies
auditor.py          Python audit client (to be compiled into EXE)
auditor.exe         Compiled executable delivered to clients
```

---

## Server Components

### auditor.php
- Handles file uploads.
- Saves files and creates copies.
- Displays the audit interface.
- Refreshes only the file list iframe every 3 seconds.

### download.php
- Sends `auditor.exe` to the browser with correct headers.

### list_files.php
- Lists all files found in `audit_results/` and `audit_copies/`.

---

## Client Component (auditor.py)

### Data Collection
Runs commands to gather:
- Serial Number  
- CPU ID  
- Motherboard UUID  
- MAC Address  
- BIOS Version  
- SSD Serial  
- Machine GUID  
- Windows Product ID  
- IP Address  

Each output is trimmed to avoid oversized files.

### File Generation
Creates temporary files in the system’s temp directory:
- `audit_TIMESTAMP.txt`
- `audit_TIMESTAMP.csv`

### Upload Process
- Sends both files to `auditor.php` using multipart POST.
- Validates file existence and size.
- Checks HTTP response status.

### Cleanup
- Deletes the temporary files and directory.
- Schedules deletion of the executable/script itself.

---

## Requirements

### Server
- PHP 7 or newer
- Write permissions for:
  - `audit_results/`
  - `audit_copies/`

### Client
- Windows operating system
- Python 3.10+ (for development)
- PyInstaller (to build the EXE)

---

## Building the Executable

To generate the EXE from the Python script:

```
pyinstaller --onefile auditor.py
```

Place the resulting `auditor.exe` in the same directory as `download.php`.

---

## Execution Flow

1. User opens `auditor.php`.
2. Browser automatically downloads `auditor.exe`.
3. The executable runs on the client machine.
4. The client collects system data and generates temporary files.
5. Files are uploaded to the server.
6. The server stores the files and displays them in the interface.
7. The client deletes temporary files and removes itself.

