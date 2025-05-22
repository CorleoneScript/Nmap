#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import datetime
import os
import sys
import time
import re
from pathlib import Path
import platform

# ==================== Swiss Army Knife Banner ====================
print(r"""
     __________                                 
    .'----------`.                              
    | .--------. |                             
    | |########| |       __________              
    | |########| |      /__________\             
.----| `--------' |------|    --=-- |------------.
|    `----,-.-----'      |o ======  |            |
|   ______|_|_______     |__________|            |
|  /  %%%%%%%%%%%%  \                            |
| /  %%%%%%%%%%%%%%  \                           |
| ^^^^^^^^^^^^^^^^^^^^                           |
+------------------------------------------------+
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""")
# ==================== End Swiss Army Knife Banner ====================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def strip_colors(text: str) -> str:
    """Remove ANSI color codes from text."""
    return re.sub(r'\033\[[0-9;]*m', '', text)

def get_downloads_path() -> str:
    """Get the downloads path for the current operating system."""
    return str(Path.home() / "Downloads")

def save_results(results: str, target: str, scan_type: str) -> str:
    """Save scan results to the Downloads directory."""
    downloads_path = get_downloads_path()
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"nmap_scan_{target}_{scan_type}_{timestamp}.txt"
    full_path = os.path.join(downloads_path, filename)
    clean_results = strip_colors(results)
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(clean_results)
        return full_path
    except Exception as e:
        print(f"{Colors.FAIL}Error saving file: {str(e)}{Colors.ENDC}")
        return None

class ScanProgress:
    def __init__(self):
        self.start_time = time.time()
        self.completed_ports = 0.0
        self.current_port = 0
        self.eta = None

    def update(self, line: str) -> None:
        """Update progress based on Nmap output line."""
        progress_match = re.search(r'Completed ([0-9.]+)%', line)
        if progress_match:
            self.completed_ports = float(progress_match.group(1))
        port_match = re.search(r'Scanning port ([0-9]+)', line)
        if port_match:
            self.current_port = int(port_match.group(1))
        if self.completed_ports > 0:
            elapsed_time = time.time() - self.start_time
            total_time = (elapsed_time * 100) / self.completed_ports
            self.eta = total_time - elapsed_time

    def get_progress_line(self) -> str:
        elapsed = time.time() - self.start_time
        eta_str = f"ETA {int(self.eta)}s" if self.eta else "ETA ??:??"
        return (f"{Colors.BLUE}Progress: {self.completed_ports:.2f}% "
                f"({self.current_port}/65535 ports) "
                f"| Current: {self.current_port} "
                f"| Elapsed: {int(elapsed)}s "
                f"| {eta_str}{Colors.ENDC}")

SCAN_TYPES = {
    "1": ("all", "All Scans Combined (Full port scan + All scripts)"),
    "2": ("stealth", "Stealth SYN Scan (-sS)"),
    "3": ("tcp_connect", "TCP Connect Scan (-sT)"),
    "4": ("udp", "UDP Scan (-sU)"),
    "5": ("version", "Version Detection (-sV)"),
    "6": ("os", "OS Detection (-O)"),
    "7": ("comprehensive", "Comprehensive Scan (-sS -sV -O -A)"),
    "8": ("quick", "Quick Scan (-F)"),
    "9": ("intensive", "Intensive Scan (-T4 -A -v)"),
    "10": ("null", "NULL Scan (-sN)"),
    "11": ("fin", "FIN Scan (-sF)"),
    "12": ("xmas", "XMAS Scan (-sX)"),
    "13": ("ping", "Ping Scan (-sn)"),
    "14": ("script_vuln", "Vulnerability Script Scan"),
    "15": ("script_default", "Default Script Scan"),
    "16": ("script_auth", "Authentication Script Scan"),
    "17": ("script_brute", "Brute Force Script Scan"),
    "18": ("script_exploit", "Exploit Script Scan"),
    "19": ("aggressive", "Aggressive Scan"),
}

SCAN_PARAMS = {
    'all': ['-sS', '-sU', '-sV', '-O', '-A', '-p-', '--script', 'default,vuln,auth,brute,exploit'],
    'stealth': ['-sS', '-p-'],
    'tcp_connect': ['-sT', '-p-'],
    'udp': ['-sU', '-p-'],
    'version': ['-sV', '-p-'],
    'os': ['-O', '-p-'],
    'comprehensive': ['-sS', '-sV', '-O', '-A', '-p-'],
    'quick': ['-F'],
    'intensive': ['-T4', '-A', '-v', '-p-'],
    'null': ['-sN', '-p-'],
    'fin': ['-sF', '-p-'],
    'xmas': ['-sX', '-p-'],
    'ping': ['-sn'],
    'script_vuln': ['-sV', '--script', 'vuln', '-p-'],
    'script_default': ['-sV', '--script', 'default', '-p-'],
    'script_auth': ['-sV', '--script', 'auth', '-p-'],
    'script_brute': ['-sV', '--script', 'brute', '-p-'],
    'script_exploit': ['-sV', '--script', 'exploit', '-p-'],
    'aggressive': ['-T4', '-A', '-v', '--script', 'aggressive', '-p-']
}

def run_nmap_scan(target: str, scan_type: str) -> str:
    """Execute an nmap scan and display results in real-time with native Nmap formatting."""
    if scan_type not in SCAN_PARAMS:
        print(f"{Colors.FAIL}Invalid scan type specified.{Colors.ENDC}")
        return ""

    try:
        subprocess.run(['nmap', '--version'], capture_output=True, check=True)
    except Exception:
        print(f"{Colors.FAIL}Error: Nmap is not installed. Please install nmap first.{Colors.ENDC}")
        sys.exit(1)

    command = ['nmap', '-vv'] + SCAN_PARAMS[scan_type] + [target]

    print(
        f"\n{Colors.BOLD}Starting Nmap {' '.join(SCAN_PARAMS[scan_type])} scan at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"Scanning target: {Colors.GREEN}{target}{Colors.ENDC}\n")

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )

    output_lines = []
    progress = ScanProgress()
    last_progress_update = 0

    while True:
        stdout_line = process.stdout.readline()
        stderr_line = process.stderr.readline()

        if not stdout_line and not stderr_line and process.poll() is not None:
            break

        if stdout_line:
            line = stdout_line.strip()
            if line:
                progress.update(line)
                current_time = time.time()
                if current_time - last_progress_update >= 1:
                    sys.stdout.write('\033[K')
                    print(progress.get_progress_line(), end='\r')
                    last_progress_update = current_time

                colorized = line
                if "open" in line.lower():
                    colorized = line.replace("open", f"{Colors.GREEN}open{Colors.ENDC}")
                elif "filtered" in line.lower():
                    colorized = line.replace("filtered", f"{Colors.BLUE}filtered{Colors.ENDC}")
                elif "closed" in line.lower():
                    colorized = line.replace("closed", f"{Colors.WARNING}closed{Colors.ENDC}")

                if "Completed" not in line and "Scanning port" not in line:
                    print(colorized)
                    output_lines.append(colorized)

        if stderr_line:
            line = stderr_line.strip()
            if line and "WARNING" not in line:
                print(f"{Colors.FAIL}{line}{Colors.ENDC}")
                output_lines.append(line)

    sys.stdout.write('\033[K')
    return_code = process.poll()
    if return_code == 0:
        print(f"\n{Colors.GREEN}Nmap scan completed successfully!{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}Scan completed with errors (return code: {return_code}){Colors.ENDC}")

    return '\n'.join(output_lines)

def main():
    print(f"""{Colors.HEADER}
    ╔════════════════════════════════════════════╗
    ║        Advanced Nmap Scanning Suite        ║
    ║    All-in-One Security Scanning Tool       ║
    ╚════════════════════════════════════════════╝
    {Colors.ENDC}""")

    while True:
        target = input(f"\n{Colors.BOLD}Enter target domain/IP (or 'quit' to exit): {Colors.ENDC}").strip()
        if target.lower() == 'quit':
            break

        print(f"\n{Colors.BOLD}Available scan types:{Colors.ENDC}")
        for num, (_, desc) in SCAN_TYPES.items():
            print(f"{num}. {desc}")

        choice = input(f"\n{Colors.BOLD}Select scan type (1-{len(SCAN_TYPES)}): {Colors.ENDC}").strip()
        if choice not in SCAN_TYPES:
            print(f"{Colors.FAIL}Invalid choice. Please select a number between 1 and {len(SCAN_TYPES)}.{Colors.ENDC}")
            continue

        scan_type = SCAN_TYPES[choice][0]
        results = run_nmap_scan(target, scan_type)

        if results:
            save_choice = input(
                f"\n{Colors.BOLD}Would you like to save the results to Downloads? (y/n): {Colors.ENDC}").lower()
            if save_choice == 'y':
                saved_path = save_results(results, target, scan_type)
                if saved_path:
                    print(f"{Colors.GREEN}Results saved to: {saved_path}{Colors.ENDC}")

            continue_scanning = input(
                f"\n{Colors.BOLD}Would you like to perform another scan? (y/n): {Colors.ENDC}").lower()
            if continue_scanning != 'y':
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Program interrupted by user. Exiting...{Colors.ENDC}")
        sys.exit(0)
