# WiFi Signal Strength Monitor & Simulator

## Overview
This project contains two tools:
1. **wifi_monitor.py** - Real hardware WiFi monitoring (requires actual WiFi adapter)
2. **wifi_simulator.py** - WiFi environment simulator that demonstrates wireless concepts without hardware requirements

Both tools demonstrate understanding of wireless networking fundamentals including signal measurement, channel identification, interference analysis, and quality assessment.

## Features

### Monitor Features
- Real-time WiFi signal strength monitoring (dBm)
- Signal quality percentage calculation
- Channel and frequency detection
- CSV logging for historical analysis
- Signal status categorization (Excellent/Good/Fair/Poor)

### Simulator Features
- Simulates office, warehouse, and data center WiFi environments
- Models time-based interference patterns
- Channel congestion analysis
- Signal-to-Noise Ratio (SNR) calculations
- Multi-AP environment simulation
- Recommendations for network optimization

## Technical Concepts Demonstrated
1. **Signal Strength (RSSI)**: Understanding of dBm measurements and their significance
2. **Channel Mapping**: Converting frequencies to channel numbers for both 2.4GHz and 5GHz bands
3. **Signal-to-Noise Ratio (SNR)**: Calculating and interpreting SNR values
4. **Channel Utilization**: Understanding congestion and interference patterns
5. **Time-based Analysis**: Modeling peak usage hours and their impact
6. **Multi-AP Environments**: Simulating real-world enterprise WiFi deployments
7. **Interference Detection**: Identifying and categorizing interference levels
8. **Data Logging**: Capturing metrics over time for trend analysis

## Usage

### Real Monitoring (requires WiFi hardware)
```bash
python3 wifi_monitor.py
```

### Simulation Mode (no hardware required)
```bash
python3 wifi_simulator.py
```

## Signal Strength Reference
- **-30 to -50 dBm**: Excellent signal
- **-50 to -60 dBm**: Good signal  
- **-60 to -70 dBm**: Fair signal
- **-70 to -90 dBm**: Poor signal

## Output
- Console display of real-time metrics
- CSV log file (wifi_signal_log.csv) for analysis

## Requirements
- Python 3.x
- Operating System specific:
  - **macOS**: Built-in airport utility (may require sudo)
  - **Linux**: nmcli or iwconfig (wireless-tools package)
  - **Windows**: Built-in netsh command
- Administrator/sudo access may be required on some systems

## Future Enhancements
- Support for multiple network interfaces
- Graphical visualization of signal trends
- Alert system for signal degradation
- Enhanced multi-platform support
- Support for 6 GHz band (WiFi 6E)