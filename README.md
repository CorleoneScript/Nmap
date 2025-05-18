Here's a **professional and visually appealing `README.md`** for your GitHub project, enhanced with structure, styling, and relevant emojis to make it both professional and engaging:

---

````markdown
# 🔍 Advanced Nmap Scanning Suite

A powerful and user-friendly **Python-based CLI tool** for automating advanced `nmap` scans with real-time progress updates, colorful output, and results saved to your Downloads folder. Perfect for pentesters, sysadmins, and network engineers.  
   
![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg) ![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

- 🧠 **Intelligent Scan Selection** — Choose from 19 powerful scan types
- 🎨 **Colorized Output** — Clear visual feedback for open, closed, and filtered ports
- 📊 **Live Progress Tracker** — Real-time scan percentage, current port, elapsed time, and ETA
- 💾 **Auto Save Results** — Export scan logs to your system’s Downloads folder
- 🧰 **All-in-One Scan Suite** — Includes comprehensive script support for vuln/auth/brute/exploit scans
- 🔐 **Root Check** — Ensures privileged scan types are executed with proper permissions

---

## 🛠️ Installation

Make sure you have **Nmap** and **Python 3.7+** installed.

```bash
# Install nmap
sudo apt install nmap        # Debian/Ubuntu
brew install nmap            # macOS (Homebrew)
choco install nmap           # Windows (Chocolatey)

# Clone this repository
git clone https://github.com/your-username/nmap-scanner-suite.git
cd nmap-scanner-suite

# Run the script
sudo python3 scanner.py
````

---

## 🚀 Usage

```bash
sudo python3 scanner.py
```

Follow the interactive prompts:

* Enter a domain/IP address ✅
* Choose a scan type (1–19) from the menu 🧪
* View real-time progress with ETA and elapsed time ⏱️
* Save results to your Downloads folder 📂

---

## 📚 Scan Types

| Option | Scan Type             | Description                      |
| ------ | --------------------- | -------------------------------- |
| 1      | All                   | Full scan with all scripts       |
| 2      | Stealth SYN           | Silent scan using `-sS`          |
| 3      | TCP Connect           | Basic TCP handshake scan         |
| 4      | UDP                   | Scan all UDP ports               |
| 5      | Version Detection     | Identify services on ports       |
| 6      | OS Detection          | Attempt OS fingerprinting        |
| 7      | Comprehensive         | All detection methods together   |
| 8      | Quick                 | Fast scan using `-F`             |
| 9      | Intensive             | Aggressive & verbose scan        |
| 10     | NULL                  | Send packets with no flags       |
| 11     | FIN                   | Send FIN-flag packets            |
| 12     | XMAS                  | Send all-flags packets           |
| 13     | Ping                  | Check for host availability only |
| 14     | Vulnerability Scripts | Run `vuln` scripts               |
| 15     | Default Scripts       | Run `default` scripts            |
| 16     | Auth Scripts          | Run `auth` scripts               |
| 17     | Brute Scripts         | Run `brute` scripts              |
| 18     | Exploit Scripts       | Run `exploit` scripts            |
| 19     | Aggressive            | All aggressive scripts and scans |

---

## 📦 Output Example

```text
Progress: 34.50% (22678/65535 ports) | Current: 22678 | Elapsed: 76s | ETA 145s
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
443/tcp   filtered https
```

---

## 🧑‍💻 Developer Notes

* Tested on **Linux**, **macOS**, and **Windows (with WSL)**
* Results are **colorized in terminal** and saved **without ANSI escape codes**
* Requires root/admin privileges for most scan types

---

## ⚠️ Disclaimer

This tool is intended for **educational** and **authorized security testing** purposes only.
**Do NOT** scan networks or systems without proper permission. Unauthorized scanning is illegal in many jurisdictions.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## ❤️ Contributions

Pull requests and issues are welcome!
If you find a bug or want to add features, feel free to open an issue or fork the project.

---

## 🙌 Credits

Made with 💻 and 🕵️ by [Your Name](https://github.com/your-username)

```

---

Let me know if you want me to generate a `README.md` file for download or include a project logo/banner!
```
