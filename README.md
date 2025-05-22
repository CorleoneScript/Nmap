# 🔍 Swiss Army Knife Network Scanner

A sophisticated and user-friendly **Python-based CLI tool** for automating advanced network scanning operations with real-time progress updates, colorful output, and automated result saving. Perfect for network administrators, security professionals, and system administrators.

```
                                    .:^
             ^                     /   :
'`.        /;/                    /    /
\  \      /;/                    /    /
 \\ \    /;/                    /  ///
  \\ \  /;/                    /  ///
   \  \/_/____________________/    /
    `/                         \  /
HZ  {  o              o  }'
     \_________________________/
```



## ✨ Key Features

- 🎯 **19 Specialized Scan Types** — From stealthy reconnaissance to comprehensive analysis
- 🎨 **Intelligent Color Coding** — Visual distinction between open, filtered, and closed ports
- 📊 **Dynamic Progress Tracking** — Real-time completion percentage, current port status, and time estimates
- 💾 **Automated Result Management** — Systematic saving of scan results with timestamped filenames
- 🛡️ **Comprehensive Security Suite** — Full support for vulnerability, authentication, and exploitation scripts
- 🔄 **Cross-Platform Compatibility** — Works seamlessly on Windows, Linux, and macOS

## 🛠️ Prerequisites & Installation

### System Requirements:
- Python 3.7 or higher
- Nmap scanning utility
- Administrative privileges for certain scan types

### Installation Steps:

```bash
# Install Nmap based on your operating system
# Windows (Using Chocolatey):
choco install nmap

# Linux (Debian/Ubuntu):
sudo apt install nmap

# macOS (Using Homebrew):
brew install nmap

# Clone the repository
git clone https://github.com/RevShellX/Nmap.git
cd Nmap
```

## 🚀 Usage Guide

1. Launch the scanner with appropriate privileges:
   ```bash
   python nmap.py
   ```

2. Follow the interactive menu:
   - Enter target domain/IP
   - Select from 19 specialized scan types
   - Monitor real-time scan progress
   - Optionally save results

## 📚 Available Scan Types

| ID | Type             | Description                       | Parameters                                              |
|----|------------------|-----------------------------------|---------------------------------------------------------|
| 1  | All-in-One       | Comprehensive scan with all scripts | `-sS -sU -sV -O -A -p- --script default,vuln,auth,brute,exploit` |
| 2  | Stealth SYN      | Low-profile SYN scan              | `-sS -p-`                                               |
| 3  | TCP Connect      | Full TCP handshake                | `-sT -p-`                                               |
| 4  | UDP              | UDP port analysis                 | `-sU -p-`                                               |
| 5  | Version Detection| Service version identification    | `-sV -p-`                                               |
| 6  | OS Detection     | Operating system fingerprinting   | `-O -p-`                                                |
| 7  | Comprehensive    | Combined detection techniques     | `-sS -sV -O -A -p-`                                     |
| 8  | Quick            | Fast port analysis                | `-F`                                                    |
| 9  | Intensive        | Detailed aggressive scan          | `-T4 -A -v -p-`                                         |
| 10 | NULL             | TCP NULL flag scan                | `-sN -p-`                                               |
| 11 | FIN              | TCP FIN flag scan                 | `-sF -p-`                                               |
| 12 | XMAS             | TCP XMAS flag scan                | `-sX -p-`                                               |
| 13 | Ping             | Host discovery                    | `-sn`                                                   |
| 14 | Vulnerability    | NSE vulnerability assessment      | `-sV --script vuln -p-`                                 |
| 15 | Default Scripts  | Standard NSE scripts              | `-sV --script default -p-`                              |
| 16 | Authentication   | Auth-related NSE scripts          | `-sV --script auth -p-`                                 |
| 17 | Brute Force      | Password brute forcing            | `-sV --script brute -p-`                                |
| 18 | Exploit          | Exploitation scripts              | `-sV --script exploit -p-`                              |
| 19 | Aggressive       | Full aggressive scan              | `-T4 -A -v --script aggressive -p-`                     |

## 📋 Sample Output

```plaintext
╔════════════════════════════════════════════╗
║        Advanced Nmap Scanning Suite        ║
║    All-in-One Security Scanning Tool      ║
╚════════════════════════════════════════════╝

Progress: 45.32% (29,692/65,535 ports) | Current: 29,692 | Elapsed: 127s | ETA: 153s
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
443/tcp  open     https
3306/tcp filtered mysql
```

## 🔧 Technical Features

- **Real-time Progress Tracking**
  - Completion percentage
  - Current port status
  - Elapsed time monitoring
  - Estimated time remaining

- **Intelligent Color Coding*
  - Green: Open ports
  - Blue: Filtered ports
  - Yellow: Closed ports
  - Red: Errors/Warnings

- **Automated Result Management**
  - Timestamp-based file naming
  - Organized storage in Downloads folder
  - Clean output formatting

## ⚠️ Legal Disclaimer

This tool is provided for **authorized security testing and educational purposes only**. Users must:
- Obtain explicit permission before scanning any networks or systems
- Comply with all applicable local, state, and federal laws
- Understand that unauthorized scanning may be illegal

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The Nmap Security Scanner team
- Python community
- All contributors and users

