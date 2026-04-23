#!/usr/bin/env python3
"""
Blue Team Reconnaissance - Silent Mode
Executes complete hardware audit in background without visible output
Automatically exports reports to Desktop/audit_reports/
"""

import os
import sys
import json
import csv
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Configure silent logging (file only)
log_file = Path.home() / 'Desktop' / f'remote_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(str(log_file))]
)

logger = logging.getLogger(__name__)

class SilentAuditor:
    def __init__(self):
        self.data = {}
        self.results_dir = Path.home() / 'Desktop' / 'audit_reports'
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run_command(self, cmd, description=""):
        """Execute command without output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            logger.info(f"Executed: {description}")
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Failed: {description} - {str(e)}")
            return ""
    
    def collect_nine_ids(self):
        """Collect the 9 main hardware IDs"""
        logger.info("Starting 9-ID collection")
        
        nine_ids = {
            "Serial Number": 'wmic bios get serialnumber /value',
            "CPU ID": 'wmic cpu get processorid /value',
            "UUID Motherboard": 'wmic csproduct get uuid /value',
            "MAC Address": 'ipconfig /all',
            "BIOS Version": 'wmic bios get smbiosbiosversion /value',
            "SSD Serial": 'wmic logicaldisk get serialnumber /value',
            "Machine GUID": 'reg query "HKLM\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid',
            "Windows Product ID": 'wmic os get serialnumber /value',
            "IP Address": 'ipconfig'
        }
        
        for key, cmd in nine_ids.items():
            output = self.run_command(cmd, f"Collecting {key}")
            self.data[f"9ID_{key}"] = output[:500] if output else "N/A"
    
    def collect_storage(self):
        """Collect storage information"""
        logger.info("Collecting storage data")
        
        storage_cmds = {
            "Disk Info": 'wmic logicaldisk get name, size, freespace /format:list',
            "Physical Media": 'wmic physicalmedia get serienumber /value',
            "Volume Info": 'wmic logicaldisk list brief /value'
        }
        
        for key, cmd in storage_cmds.items():
            output = self.run_command(cmd, f"Storage: {key}")
            self.data[f"storage_{key}"] = output[:500] if output else "N/A"
    
    def collect_network(self):
        """Collect network information"""
        logger.info("Collecting network data")
        
        network_cmds = {
            "Network Adapters": 'ipconfig /all',
            "Routing Table": 'route print',
            "Active Connections": 'netstat -an'
        }
        
        for key, cmd in network_cmds.items():
            output = self.run_command(cmd, f"Network: {key}")
            self.data[f"network_{key}"] = output[:500] if output else "N/A"
    
    def collect_windows_specific(self):
        """Collect Windows-specific data"""
        logger.info("Collecting Windows-specific data")
        
        windows_cmds = {
            "OS Info": 'systeminfo',
            "Installed Software": 'wmic product list brief /value',
            "Services": 'wmic service list brief /value'
        }
        
        for key, cmd in windows_cmds.items():
            output = self.run_command(cmd, f"Windows: {key}")
            self.data[f"windows_{key}"] = output[:500] if output else "N/A"
    
    def collect_peripherals(self):
        """Collect peripheral information"""
        logger.info("Collecting peripheral data")
        
        peripherals_cmds = {
            "USB Devices": 'wmic logicaldisk get description',
            "PnP Devices": 'wmic pnpdevice list brief /value',
            "Keyboards/Mice": 'wmic path win32_pointingdevice get name'
        }
        
        for key, cmd in peripherals_cmds.items():
            output = self.run_command(cmd, f"Peripherals: {key}")
            self.data[f"peripherals_{key}"] = output[:500] if output else "N/A"
    
    def collect_tpm(self):
        """Collect TPM information"""
        logger.info("Collecting TPM data")
        
        tpm_cmd = 'wmic os get name, version'
        output = self.run_command(tpm_cmd, "TPM Info")
        self.data["tpm_info"] = output[:500] if output else "N/A"
    
    def export_txt(self):
        """Export to TXT format"""
        txt_file = self.results_dir / f'audit_{self.timestamp}.txt'
        
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Hardware Audit Report - {datetime.now()}\n")
                f.write("=" * 80 + "\n\n")
                
                for key, value in self.data.items():
                    f.write(f"\n{key}:\n")
                    f.write("-" * 40 + "\n")
                    f.write(str(value) + "\n")
            
            logger.info(f"Exported TXT: {txt_file}")
            return str(txt_file)
        except Exception as e:
            logger.error(f"TXT export failed: {str(e)}")
            return None
    
    def export_json(self):
        """Export to JSON format"""
        json_file = self.results_dir / f'remote_{self.timestamp}.json'
        
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported JSON: {json_file}")
            return str(json_file)
        except Exception as e:
            logger.error(f"JSON export failed: {str(e)}")
            return None
    
    def export_csv(self):
        """Export to CSV format"""
        csv_file = self.results_dir / f'remote_{self.timestamp}.csv'
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Field', 'Value'])
                
                for key, value in self.data.items():
                    writer.writerow([key, str(value)])
            
            logger.info(f"Exported CSV: {csv_file}")
            return str(csv_file)
        except Exception as e:
            logger.error(f"CSV export failed: {str(e)}")
            return None
    
    def run_full_audit(self):
        """Execute complete audit"""
        logger.info("Starting full audit")
        
        self.collect_nine_ids()
        self.collect_storage()
        self.collect_network()
        self.collect_windows_specific()
        self.collect_peripherals()
        self.collect_tpm()
        
        # Export to all formats
        self.export_txt()
        self.export_json()
        self.export_csv()
        
        logger.info("Audit completed successfully")

def main():
    """Entry point - executes silently"""
    try:
        auditor = SilentAuditor()
        auditor.run_full_audit()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.critical(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    main()