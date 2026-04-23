#!/usr/bin/env python3
"""
Blue Team Reconnaissance - Interactive Menu
Hardware audit tool with menu options
Multiple export formats (TXT, CSV, JSON)
"""

import os
import sys
import json
import csv
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class Colors:
    """ANSI colors for terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class InteractiveAuditor:
    def __init__(self):
        self.data = {}
        self.results_dir = Path.home() / 'Desktop' / 'audit_reports'
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.mode = "full"  # "simple" or "full"
    
    def clear_screen(self):
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print header"""
        self.clear_screen()
        print(f"\n{Colors.BOLD}{Colors.BLUE}")
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 8 + "BLUE TEAM RECONNAISSANCE TOOL" + " " * 22 + "║")
        print("║" + " " * 14 + "Hardware Audit Suite v2" + " " * 20 + "║")
        print("╚" + "═" * 58 + "╝")
        print(f"{Colors.RESET}\n")
    
    def print_menu(self):
        """Print main menu"""
        self.print_header()
        print(f"{Colors.CYAN}=== AUDIT MODE ==={Colors.RESET}\n")
        print(f"  {Colors.GREEN}1{Colors.RESET}) Simple Audit (9 main hardware IDs)")
        print(f"  {Colors.GREEN}2{Colors.RESET}) Complete Audit (9 IDs + Storage + Network + Windows + Peripherals + TPM)")
        print(f"  {Colors.GREEN}3{Colors.RESET}) Exit\n")
    
    def print_export_menu(self):
        """Print export menu"""
        print(f"\n{Colors.CYAN}=== EXPORT FORMAT ==={Colors.RESET}\n")
        print(f"  {Colors.GREEN}1{Colors.RESET}) TXT (Plain text)")
        print(f"  {Colors.GREEN}2{Colors.RESET}) CSV (Spreadsheet)")
        print(f"  {Colors.GREEN}3{Colors.RESET}) JSON (Structured)")
        print(f"  {Colors.GREEN}4{Colors.RESET}) All formats")
        print(f"  {Colors.GREEN}5{Colors.RESET}) Cancel\n")
    
    def run_command(self, cmd: str, description: str = "") -> str:
        """Execute PowerShell command"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            if description:
                print(f"  ✓ {description}")
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            print(f"  ✗ {description} (timeout)")
            return ""
        except Exception as e:
            print(f"  ✗ {description} ({str(e)})")
            return ""
    
    def collect_nine_ids(self, verbose: bool = True):
        """Collect the 9 main hardware IDs"""
        if verbose:
            print(f"\n{Colors.YELLOW}[*] Collecting 9 main IDs...{Colors.RESET}\n")
        
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
            output = self.run_command(cmd, key)
            self.data[f"9ID_{key}"] = output[:1000] if output else "N/A"
        
        if verbose:
            print(f"\n{Colors.GREEN}✓ 9 IDs collected successfully{Colors.RESET}")
    
    def collect_storage(self, verbose: bool = True):
        """Collect storage information"""
        if verbose:
            print(f"\n{Colors.YELLOW}[*] Collecting storage data...{Colors.RESET}\n")
        
        storage_cmds = {
            "Disk Info": 'wmic logicaldisk get name, size, freespace /format:list',
            "Physical Media": 'wmic physicalmedia get serienumber /value',
            "Volume Info": 'wmic logicaldisk list brief /value'
        }
        
        for key, cmd in storage_cmds.items():
            output = self.run_command(cmd, key)
            self.data[f"storage_{key}"] = output[:1000] if output else "N/A"
        
        if verbose:
            print(f"\n{Colors.GREEN}✓ Storage collected{Colors.RESET}")
    
    def collect_network(self, verbose: bool = True):
        """Collect network information"""
        if verbose:
            print(f"\n{Colors.YELLOW}[*] Collecting network data...{Colors.RESET}\n")
        
        network_cmds = {
            "Network Adapters": 'ipconfig /all',
            "Routing Table": 'route print',
            "Active Connections": 'netstat -an'
        }
        
        for key, cmd in network_cmds.items():
            output = self.run_command(cmd, key)
            self.data[f"network_{key}"] = output[:1000] if output else "N/A"
        
        if verbose:
            print(f"\n{Colors.GREEN}✓ Network collected{Colors.RESET}")
    
    def collect_windows_specific(self, verbose: bool = True):
        """Collect Windows-specific data"""
        if verbose:
            print(f"\n{Colors.YELLOW}[*] Collecting Windows data...{Colors.RESET}\n")
        
        windows_cmds = {
            "OS Info": 'systeminfo',
            "Installed Software": 'wmic product list brief /value',
            "Running Services": 'tasklist /v'
        }
        
        for key, cmd in windows_cmds.items():
            output = self.run_command(cmd, key)
            self.data[f"windows_{key}"] = output[:1000] if output else "N/A"
        
        if verbose:
            print(f"\n{Colors.GREEN}✓ Windows info collected{Colors.RESET}")
    
    def collect_peripherals(self, verbose: bool = True):
        """Collect peripheral information"""
        if verbose:
            print(f"\n{Colors.YELLOW}[*] Collecting peripheral data...{Colors.RESET}\n")
        
        peripherals_cmds = {
            "USB Devices": 'wmic logicaldisk get description',
            "PnP Devices": 'wmic pnpdevice list brief /value',
            "Display Devices": 'wmic path win32_videocontroller get name'
        }
        
        for key, cmd in peripherals_cmds.items():
            output = self.run_command(cmd, key)
            self.data[f"peripherals_{key}"] = output[:1000] if output else "N/A"
        
        if verbose:
            print(f"\n{Colors.GREEN}✓ Peripherals collected{Colors.RESET}")
    
    def collect_tpm(self, verbose: bool = True):
        """Collect TPM information"""
        if verbose:
            print(f"\n{Colors.YELLOW}[*] Collecting TPM...{Colors.RESET}\n")
        
        tpm_cmd = 'wmic os get name, version, buildnumber'
        output = self.run_command(tpm_cmd, "TPM/OS Build Info")
        self.data["tpm_info"] = output[:1000] if output else "N/A"
        
        if verbose:
            print(f"\n{Colors.GREEN}✓ TPM collected{Colors.RESET}")
    
    def export_txt(self) -> str:
        """Export to TXT format"""
        txt_file = self.results_dir / f'audit_{self.timestamp}.txt'
        
        try:
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"╔{'═' * 78}╗\n")
                f.write(f"║ HARDWARE AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"╚{'═' * 78}╝\n\n")
                
                for key, value in self.data.items():
                    f.write(f"\n┌─ {key} {'─' * (70 - len(key))}\n")
                    f.write(f"│\n")
                    f.write(f"│ {str(value)}\n")
                    f.write(f"│\n")
            
            return str(txt_file)
        except Exception as e:
            print(f"{Colors.RED}Error exporting TXT: {str(e)}{Colors.RESET}")
            return ""
    
    def export_json(self) -> str:
        """Export to JSON format"""
        json_file = self.results_dir / f'remote_{self.timestamp}.json'
        
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": self.timestamp,
                    "mode": self.mode,
                    "data": self.data
                }, f, indent=2, ensure_ascii=False)
            
            return str(json_file)
        except Exception as e:
            print(f"{Colors.RED}Error exporting JSON: {str(e)}{Colors.RESET}")
            return ""
    
    def export_csv(self) -> str:
        """Export to CSV format"""
        csv_file = self.results_dir / f'remote_{self.timestamp}.csv'
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Field', 'Value'])
                
                for key, value in self.data.items():
                    writer.writerow([key, str(value)[:500]])
            
            return str(csv_file)
        except Exception as e:
            print(f"{Colors.RED}Error exporting CSV: {str(e)}{Colors.RESET}")
            return ""
    
    def show_export_result(self, files: List[str]):
        """Show export result"""
        print(f"\n{Colors.GREEN}╔" + "═" * 56 + "╗")
        print("║" + " EXPORT COMPLETED SUCCESSFULLY ".center(56) + "║")
        print("╚" + "═" * 56 + "╝\n{Colors.RESET}")
        
        for f in files:
            if f:
                print(f"  {Colors.CYAN}→{Colors.RESET} {f}")
        
        print(f"\n  {Colors.YELLOW}Location:{Colors.RESET} {self.results_dir}\n")
    
    def run_simple_audit(self):
        """Run simple audit"""
        self.mode = "simple"
        self.collect_nine_ids(verbose=True)
    
    def run_full_audit(self):
        """Run complete audit"""
        self.mode = "full"
        self.collect_nine_ids(verbose=True)
        self.collect_storage(verbose=True)
        self.collect_network(verbose=True)
        self.collect_windows_specific(verbose=True)
        self.collect_peripherals(verbose=True)
        self.collect_tpm(verbose=True)
    
    def main_loop(self):
        """Main loop"""
        while True:
            self.print_menu()
            choice = input(f"{Colors.BOLD}Select option [1-3]: {Colors.RESET}").strip()
            
            if choice == '1':
                self.run_simple_audit()
                self.export_prompt()
            elif choice == '2':
                self.run_full_audit()
                self.export_prompt()
            elif choice == '3':
                print(f"\n{Colors.YELLOW}Exiting...{Colors.RESET}\n")
                sys.exit(0)
            else:
                print(f"{Colors.RED}Invalid option!{Colors.RESET}")
                input("Press ENTER to continue...")
    
    def export_prompt(self):
        """Ask for export format"""
        self.print_header()
        self.print_export_menu()
        
        choice = input(f"{Colors.BOLD}Select format [1-5]: {Colors.RESET}").strip()
        
        files = []
        if choice == '1':
            f = self.export_txt()
            if f: files.append(f)
        elif choice == '2':
            f = self.export_csv()
            if f: files.append(f)
        elif choice == '3':
            f = self.export_json()
            if f: files.append(f)
        elif choice == '4':
            for func in [self.export_txt, self.export_csv, self.export_json]:
                f = func()
                if f: files.append(f)
        elif choice == '5':
            print(f"\n{Colors.YELLOW}Cancelled.{Colors.RESET}")
            input("Press ENTER to return to menu...")
            return
        
        if files:
            self.show_export_result(files)
        
        input("Press ENTER to return to menu...")

def main():
    """Entry point"""
    try:
        auditor = InteractiveAuditor()
        auditor.main_loop()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Interrupted by user.{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()