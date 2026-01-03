# 🖥️ CyberMonitor - Linux System Monitor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Real-time system monitoring tool with professional DevOps aesthetics**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Autostart](#-autostart-configuration) • [Screenshots](#-screenshots)

</div>

---

## 🎯 Features

- ✨ **Real-time monitoring**: CPU, RAM, SWAP, GPU, Disk usage and temperatures
- 🎨 **Cyber/DevOps aesthetic**: Professional terminal-style interface
- ⚡ **Lightweight**: Low resource consumption (~0.5% CPU, ~30MB RAM)
- 🔄 **Auto-refresh**: Updates every 1.5 seconds
- 📊 **ASCII progress bars**: Visual representation of metrics
- 🎨 **Color-coded alerts**: Green → Yellow → Red based on usage
- 🪟 **Normal window behavior**: Minimizable and doesn't block other windows
- 🚀 **Auto-start support**: Run on system boot

---

## 📋 Requirements

- **OS**: Linux (Debian/Ubuntu based distros, Arch, Fedora, etc.)
- **Python**: 3.8 or higher
- **Dependencies**:
  - `python3-tk` (Tkinter)
  - `psutil` (System monitoring)
  - `lm-sensors` (Temperature sensors)

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/BRUNO1993-CIBER/monitor-linux.git
cd monitor-linux
```

### 2. Install system dependencies

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install python3-tk python3-venv lm-sensors
```

**Arch Linux:**
```bash
sudo pacman -S tk python-pip lm_sensors
```

**Fedora:**
```bash
sudo dnf install python3-tkinter lm_sensors
```

### 3. Configure sensors (first time only)

```bash
sudo sensors-detect
# Press ENTER to accept all defaults
```

### 4. Create virtual environment and install Python dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install psutil
```

### 5. Run the monitor

```bash
python3 mini_conky.py
```

---

## 🎮 Usage

### Running manually

```bash
# Navigate to project directory
cd /path/to/monitor-linux

# Activate virtual environment
source .venv/bin/activate

# Run in foreground
python3 mini_conky.py

# Or run in background
python3 mini_conky.py &
```

### Stopping the monitor

```bash
pkill -f mini_conky.py
```

### Check if running

```bash
ps aux | grep mini_conky.py
```

---

## 🔄 Autostart Configuration

### Method 1: Desktop Entry (Recommended)

**1. Create launcher script:**

```bash
nano start_monitor.sh
```

**Add this content:**
```bash
#!/bin/bash
cd "/path/to/monitor-linux"
source .venv/bin/activate
python3 mini_conky.py &
deactivate
```

**Make executable:**
```bash
chmod +x start_monitor.sh
```

**2. Create autostart entry:**

```bash
mkdir -p ~/.config/autostart
nano ~/.config/autostart/cybermonitor.desktop
```

**Add this content:**
```ini
[Desktop Entry]
Type=Application
Name=CyberMonitor
Comment=System Monitor - DevOps Style
Exec=/path/to/monitor-linux/start_monitor.sh
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
StartupNotify=false
Categories=Utility;System;
```

**Replace `/path/to/monitor-linux/` with your actual path!**

---

### Method 2: Systemd User Service (Advanced)

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/cybermonitor.service
```

**Add this content:**
```ini
[Unit]
Description=CyberMonitor System Monitor
After=graphical-session.target

[Service]
Type=forking
WorkingDirectory=/path/to/monitor-linux
ExecStart=/bin/bash -c 'source .venv/bin/activate && python3 mini_conky.py &'
Restart=on-failure
RestartSec=5
Environment=DISPLAY=:0
Environment=XAUTHORITY=%h/.Xauthority

[Install]
WantedBy=default.target
```

**Enable and start:**
```bash
systemctl --user daemon-reload
systemctl --user enable cybermonitor.service
systemctl --user start cybermonitor.service

# Check status
systemctl --user status cybermonitor.service
```

---

## 🎨 Customization

Edit `mini_conky.py` to customize:

### Colors
```python
self.bg_color = "#0a0e27"      # Background
self.fg_primary = "#00ff41"     # Primary (green)
self.fg_secondary = "#00d9ff"   # Secondary (cyan)
self.fg_warning = "#ffaa00"     # Warning (orange)
self.fg_danger = "#ff3366"      # Danger (red)
```

### Window Size
```python
self.width = 280   # Width in pixels
self.height = 200  # Height in pixels
```

### Update Interval
```python
self.root.after(1500, self.update_stats)  # 1500ms = 1.5 seconds
```

---

## 📊 Monitored Metrics

| Metric | Description | Color Coding |
|--------|-------------|--------------|
| **CPU** | Total CPU usage percentage | Green < 50% < Yellow < 75% < Red |
| **TEMP** | CPU temperature (°C) | Based on temperature value |
| **RAM** | Memory usage with amount used | Green < 50% < Yellow < 75% < Red |
| **SWAP** | Swap memory usage | Green < 50% < Yellow < 75% < Red |
| **GPU** | GPU temperature if available | Based on temperature value |
| **DISK** | Root partition (/) usage | Green < 50% < Yellow < 75% < Red |

---

## 🐛 Troubleshooting

### Temperatures show "N/A"

```bash
# Reconfigure sensors
sudo sensors-detect
sensors  # Check if temperatures are detected
```

### NVIDIA GPU temperature not showing

```bash
sudo apt install nvidia-smi  # For NVIDIA GPUs
```

### AMD GPU temperature not showing

```bash
# Install amdgpu drivers and ensure lm-sensors detects them
sensors
```

### Monitor not starting on boot

```bash
# Check autostart file exists
ls -la ~/.config/autostart/cybermonitor.desktop

# Check script permissions
ls -la /path/to/monitor-linux/start_monitor.sh

# Test script manually
/path/to/monitor-linux/start_monitor.sh
```

### High CPU usage

```bash
# Increase update interval in mini_conky.py
# Change from 1500 to 3000 (3 seconds)
self.root.after(3000, self.update_stats)
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter
- **System Monitoring**: psutil
- **Temperature Reading**: lm-sensors
- **Font**: JetBrains Mono (falls back to monospace)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Bruno**

- GitHub: [@BRUNO1993-CIBER](https://github.com/BRUNO1993-CIBER)
- Repository: [monitor-linux](https://github.com/BRUNO1993-CIBER/monitor-linux)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ for the Linux community**

</div>