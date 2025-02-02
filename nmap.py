import subprocess
import datetime
import os
import sys
import time
import re
from pathlib import Path
import platform


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class ScanProgress:
    def __init__(self):
        self.start_time = time.time()
        self.total_ports = 0
        self.completed_ports = 0
        self.current_port = 0
        self.eta = None

    def update(self, line):
        """Update progress based on Nmap output line"""
        # Match port scan progress line
        progress_match = re.search(r'Completed ([0-9.]+)%', line)
        if progress_match:
            self.completed_ports = float(progress_match.group(1))

        # Match current port number
        port_match = re.search(r'Scanning port ([0-9]+)', line)
        if port_match:
            self.current_port = int(port_match.group(1))

        # Calculate ETA
        if self.completed_ports > 0:
            elapsed_time = time.time() - self.start_time
            total_time = (elapsed_time * 100) / self.completed_ports
            self.eta = total_time - elapsed_time

    def get_progress_line(self):
        """Generate progress line similar to Nmap's output"""
        elapsed = time.time() - self.start_time
        eta_str = f"ETA {int(self.eta)}s" if self.eta else "ETA ??:??"
        return (f"{Colors.BLUE}Progress: {self.completed_ports:.2f}% "
                f"({self.current_port}/65535 ports) "
                f"| Current: {self.current_port} "
                f"| Elapsed: {int(elapsed)}s "
                f"| {eta_str}{Colors.ENDC}")


def check_root():
    """Check if script is run with root privileges"""
    return os.geteuid() == 0


def get_downloads_path():
    """Get the downloads path for the current operating system"""
    if platform.system() == "Windows":
        return str(Path.home() / "Downloads")
    elif platform.system() == "Darwin":  # macOS
        return str(Path.home() / "Downloads")
    else:  # Linux and other Unix
        return str(Path.home() / "Downloads")


def save_results(results, target, scan_type):
    """Save scan results to the Downloads directory"""
    downloads_path = get_downloads_path()
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"nmap_scan_{target}_{scan_type}_{timestamp}.txt"
    full_path = os.path.join(downloads_path, filename)

    # Remove color codes for file output
    clean_results = results.replace('\033[95m', '').replace('\033[94m', '') \
        .replace('\033[92m', '').replace('\033[93m', '') \
        .replace('\033[91m', '').replace('\033[0m', '') \
        .replace('\033[1m', '')

    try:
        with open(full_path, 'w') as f:
            f.write(clean_results)
        return full_path
    except Exception as e:
        print(f"{Colors.FAIL}Error saving file: {str(e)}{Colors.ENDC}")
        return None


def run_nmap_scan(target, scan_type):
    """Execute an nmap scan and display results in real-time with native Nmap formatting"""
    try:
        scan_params = {
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

        if scan_type not in scan_params:
            return "Invalid scan type specified"

        if not check_root():
            print(
                f"{Colors.FAIL}Error: This script must be run as root. Please use: sudo python3 script.py{Colors.ENDC}")
            sys.exit(1)

        command = ['nmap', '-vv'] + scan_params[scan_type] + [target]

        print(
            f"\n{Colors.BOLD}Starting Nmap {' '.join(scan_params[scan_type])} scan at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
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

                    if "open" in line.lower():
                        line = line.replace("open", f"{Colors.GREEN}open{Colors.ENDC}")
                    elif "filtered" in line.lower():
                        line = line.replace("filtered", f"{Colors.BLUE}filtered{Colors.ENDC}")
                    elif "closed" in line.lower():
                        line = line.replace("closed", f"{Colors.WARNING}closed{Colors.ENDC}")

                    if "Completed" not in line and "Scanning port" not in line:
                        print(line)
                        output_lines.append(line)

            if stderr_line:
                line = stderr_line.strip()
                if line and "WARNING" not in line:
                    print(f"{Colors.FAIL}{line}{Colors.ENDC}")
                    output_lines.append(line)

        sys.stdout.write('\033[K')

        return_code = process.poll()

        if return_code == 0:
            print(f"\n{Colors.GREEN}Nmap scan completed successfully!{Colors.ENDC}")
            save_choice = input(
                f"\n{Colors.BOLD}Would you like to save the results to Downloads? (y/n): {Colors.ENDC}").lower()
            if save_choice == 'y':
                saved_path = save_results('\n'.join(output_lines), target, scan_type)
                if saved_path:
                    print(f"{Colors.GREEN}Results saved to: {saved_path}{Colors.ENDC}")
        else:
            print(f"\n{Colors.FAIL}Scan completed with errors (return code: {return_code}){Colors.ENDC}")

        return '\n'.join(output_lines)

    except subprocess.SubprocessError as e:
        return f"Error running scan: {str(e)}"


def main():
    print(f"""{Colors.HEADER}
    ╔════════════════════════════════════════════╗
    ║        Advanced Nmap Scanning Suite        ║
    ║    All-in-One Security Scanning Tool       ║
    ╚════════════════════════════════════════════╝
    {Colors.ENDC}""")

    try:
        subprocess.run(['nmap', '--version'], capture_output=True)
    except FileNotFoundError:
        print(f"{Colors.FAIL}Error: Nmap is not installed. Please install nmap first.{Colors.ENDC}")
        return

    while True:
        target = input(f"\n{Colors.BOLD}Enter target domain/IP (or 'quit' to exit): {Colors.ENDC}").strip()
        if target.lower() == 'quit':
            break

        print(f"\n{Colors.BOLD}Available scan types:{Colors.ENDC}")
        print("1.  All Scans Combined (Full port scan + All scripts)")
        print("2.  Stealth SYN Scan (-sS)")
        print("3.  TCP Connect Scan (-sT)")
        print("4.  UDP Scan (-sU)")
        print("5.  Version Detection (-sV)")
        print("6.  OS Detection (-O)")
        print("7.  Comprehensive Scan (-sS -sV -O -A)")
        print("8.  Quick Scan (-F)")
        print("9.  Intensive Scan (-T4 -A -v)")
        print("10. NULL Scan (-sN)")
        print("11. FIN Scan (-sF)")
        print("12. XMAS Scan (-sX)")
        print("13. Ping Scan (-sn)")
        print("14. Vulnerability Script Scan")
        print("15. Default Script Scan")
        print("16. Authentication Script Scan")
        print("17. Brute Force Script Scan")
        print("18. Exploit Script Scan")
        print("19. Aggressive Scan")

        try:
            choice = int(input(f"\n{Colors.BOLD}Select scan type (1-19): {Colors.ENDC}"))
            scan_types = {
                1: 'all',
                2: 'stealth',
                3: 'tcp_connect',
                4: 'udp',
                5: 'version',
                6: 'os',
                7: 'comprehensive',
                8: 'quick',
                9: 'intensive',
                10: 'null',
                11: 'fin',
                12: 'xmas',
                13: 'ping',
                14: 'script_vuln',
                15: 'script_default',
                16: 'script_auth',
                17: 'script_brute',
                18: 'script_exploit',
                19: 'aggressive'
            }

            if choice not in scan_types:
                print(f"{Colors.FAIL}Invalid choice. Please select a number between 1 and 19.{Colors.ENDC}")
                continue

            scan_type = scan_types[choice]
            results = run_nmap_scan(target, scan_type)

            if results:
                continue_scanning = input(
                    f"\n{Colors.BOLD}Would you like to perform another scan? (y/n): {Colors.ENDC}").lower()
                if continue_scanning != 'y':
                    break

        except ValueError:
            print(f"{Colors.FAIL}Invalid input. Please enter a number.{Colors.ENDC}")
            continue
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Scan interrupted by user. Exiting...{Colors.ENDC}")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Program interrupted by user. Exiting...{Colors.ENDC}")
        sys.exit(0)