# Blue Team Reconnaissance Tool
## Hardware Audit Suite for Remote Reconnaissance Projects

---

## Version 1: Silent Mode (`remote_silent.py`)

### Description
Script that executes **complete audit in background** without any visible output.
- No console output
- Runs silently in background
- Complete collection (9 IDs + Storage + Network + Windows + Peripherals + TPM)
- Automatically exports to TXT, CSV and JSON
- Private file-based logging

### How to Use

**Option 1: Run directly (visible)**
```powershell
python remote_silent.py
```

**Option 2: Run in background (invisible)**
```powershell
# Windows PowerShell
Start-Process python -ArgumentList "remote_silent.py" -WindowStyle Hidden -NoWait

# Or with vbs (completely invisible):
wscript.exe invisible.vbs
```

**Option 3: Schedule Windows Task (Task Scheduler)**
```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\path\remote_silent.py"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "HardwareAudit" -Action $action -Trigger $trigger
```

### Output
- **Location**: `C:\Users\[username]\Desktop\remote_reports\`
- **Formats**: `remote_[timestamp].txt`, `.csv`, `.json`
- **Log**: `C:\Users\[username]\Desktop\remote_[timestamp].log`

### Features
- Silent (no output)
- 10-second timeout per command
- Collection of 20+ different data points
- Automatic export to 3 formats

---

## Version 2: Interactive Menu (`remote_sample.py`)

### Description
Script with **visual menu and interactive options**
- Colorful and user-friendly menu
- 2 modes: Simple (9 IDs) or Complete
- Choose export format
- Real-time visual feedback
- Easy to use for manual audits

### How to Use

**Run script**
```powershell
python remote_sample.py
```

### Main Menu
```
╔══════════════════════════════════════════════════════════════╗
║          BLUE TEAM RECONNAISSANCE TOOL                       ║
║          Hardware Audit Suite v2                             ║
╚══════════════════════════════════════════════════════════════╝

=== AUDIT MODE ===

  1) Simple Audit (9 main hardware IDs)
  2) Complete Audit (9 IDs + Storage + Network + Windows + Peripherals + TPM)
  3) Exit
```

### Export Options
```
=== EXPORT FORMAT ===

  1) TXT (Plain text)
  2) CSV (Spreadsheet)
  3) JSON (Structured)
  4) All formats
  5) Cancel
```

### Output
- **Location**: `C:\Users\[username]\Desktop\audit_reports\`
- **Formats**: TXT, CSV, JSON (as chosen)

### Features
- Colored menu with ANSI colors
- Real-time feedback
- Multiple export formats
- Easy navigation
- Error handling

---

## Collected Data

### Simple Audit (9 IDs)
1. Serial Number
2. CPU ID
3. UUID Motherboard
4. MAC Address
5. BIOS Version
6. SSD Serial
7. Machine GUID
8. Windows Product ID
9. IP Address

### Complete Audit (adds)
- **Storage**: Disk Info, Physical Media, Volume Info
- **Network**: Network Adapters, Routing Table, Active Connections
- **Windows**: OS Info, Installed Software, Running Services
- **Peripherals**: USB Devices, PnP Devices, Display Devices
- **TPM**: TPM/OS Build Info

---

## Requirements

### Python
```powershell
# Check if Python is installed
python --version

# If not, install from official website
# https://www.python.org/downloads/
```

### Permissions
- Scripts require **administrator privileges**
- Some commands (wmic, registry) require Admin

### Dependencies
None! Scripts use only Python standard library:
- `os`, `sys`, `json`, `csv`, `subprocess`, `pathlib`

---

## Use Cases - Blue Team

### 1. Remote Reconnaissance Initial
```powershell
# Use silent version to collect data without alerting
python remote_silent.py
```

### 2. Manual On-Site Audit
```powershell
# Use interactive version with menu
python remote_sample.py
```

### 3. Batch Automation
```powershell
# Script runs in background during startup
# Configure in Task Scheduler
```

### 4. Forensic Analysis
```powershell
# Export to JSON for programmatic analysis
python remote_sample.py
# → Select option 3 (JSON)
```

---

## Security Notes

### Detection
- Script is visible in Task Manager (python.exe)
- Exported files in Desktop (visible)
- Log leaves trace in Desktop

### Evasion
For silent mode with less footprint:
```powershell
# 1. Rename script
ren remote_silent.py svchost.py

# 2. Use scheduled task
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\Windows\Temp\svchost.py"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
Register-ScheduledTask -TaskName "WindowsUpdate" -Action $action -Trigger $trigger

# 3. Redirect output to remote server (modify script)
```

### Possible Improvements
- Obfuscate Python code
- Compile to .exe with PyInstaller
- Redirect data to C2 server
- Auto-delete logs
- Use encoded commands

---

## Output Examples

### TXT
```
╔══════════════════════════════════════════════════════════════════════════════╗
║ HARDWARE AUDIT REPORT - 2024-04-23 15:30:45
╚══════════════════════════════════════════════════════════════════════════════╝

┌─ 9ID_Serial Number ────────────────────────────────────────────────────────
│
│ SerialNumber=ABC123DEF456
│
```

### CSV
```
Field,Value
9ID_Serial Number,"SerialNumber=ABC123DEF456"
9ID_CPU ID,"ProcessorId=BFEBFBFF000906A2"
network_Active Connections,"TCP    127.0.0.1:49152..."
```

### JSON
```json
{
  "timestamp": "20240423_153045",
  "mode": "full",
  "data": {
    "9ID_Serial Number": "SerialNumber=ABC123DEF456",
    "9ID_CPU ID": "ProcessorId=BFEBFBFF000906A2",
    "network_Active Connections": "TCP    127.0.0.1:49152..."
  }
}
```

---

## Troubleshooting

### "python: command not found"
```powershell
# Add Python to PATH or use full path
C:\Python311\python.exe remote_sample.py
```

### "Access Denied"
```powershell
# Run as Administrator
# Right-click → Run as administrator
```

### "No module named..."
```powershell
# Scripts have no external dependencies
# If error, check Python installation
```

### Files not appearing
```powershell
# Check location
cd Desktop\audit_reports
dir
```

---

## License
Script for Blue Team / Local or Authorized Testing Only

---

**Version**: 1.0  
**Date**: April 2026  
**Python**: 3.7+  
**OS**: Windows  

---

## Quick Reference

| Script | Mode | Use Case | Output |
|--------|------|----------|--------|
| `remote_silent.py` | Silent | Remote/Background | Auto 3 formats |
| `remote_sample.py` | Interactive | Manual/On-site | Choose format |

**Remember**: Always get proper authorization before running reconnaissance scripts.
