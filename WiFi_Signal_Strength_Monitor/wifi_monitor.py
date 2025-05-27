#!/usr/bin/env python3
"""
Cross-Platform WiFi Signal Strength Monitor
Author: Bernardo Gallegos Vallejo
Description: Monitors WiFi signal strength across different operating systems
"""

import subprocess
import time
import re
import datetime
import csv
import os
import platform
import sys

class WiFiMonitor:
    def __init__(self):
        self.log_file = "wifi_signal_log.csv"
        self.os_type = platform.system()
        self.setup_log_file()
    
    def setup_log_file(self):
        """Initialize CSV log file with headers"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'SSID', 'Signal_Strength_dBm', 'Quality_Percent', 'Channel', 'Frequency_MHz'])
    
    def get_wifi_info(self):
        """Get WiFi information based on operating system"""
        if self.os_type == "Darwin":  # macOS
            return self.get_wifi_info_macos()
        elif self.os_type == "Linux":
            return self.get_wifi_info_linux()
        elif self.os_type == "Windows":
            return self.get_wifi_info_windows()
        else:
            print(f"Unsupported operating system: {self.os_type}")
            return None
    
    def get_wifi_info_macos(self):
        """Get WiFi information on macOS using airport utility"""
        try:
            # Get current WiFi status
            airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
            
            # Get current network info
            result = subprocess.run([airport_path, '-I'], capture_output=True, text=True)
            output = result.stdout
            
            # Parse the output
            ssid_match = re.search(r'SSID: (.+)', output)
            signal_match = re.search(r'agrCtlRSSI: (-?\d+)', output)
            channel_match = re.search(r'channel: (\d+)', output)
            
            ssid = ssid_match.group(1).strip() if ssid_match else "Unknown"
            signal_strength = int(signal_match.group(1)) if signal_match else 0
            channel = int(channel_match.group(1)) if channel_match else 0
            
            # Calculate quality from signal strength
            quality = self.calculate_quality_from_signal(signal_strength)
            
            # Estimate frequency from channel (simplified)
            if 1 <= channel <= 14:
                frequency = 2412 + (channel - 1) * 5
            else:
                frequency = 5180 + (channel - 36) * 5
            
            return {
                'ssid': ssid,
                'signal_strength': signal_strength,
                'quality': quality,
                'channel': channel,
                'frequency': frequency
            }
        except FileNotFoundError:
            # Try alternative method using system_profiler
            try:
                result = subprocess.run(['system_profiler', 'SPAirPortDataType'], capture_output=True, text=True)
                output = result.stdout
                
                # Basic parsing for system_profiler output
                ssid_match = re.search(r'Current Network Information:\s+(.+?):', output)
                signal_match = re.search(r'Signal / Noise: (-?\d+) dBm', output)
                
                ssid = ssid_match.group(1).strip() if ssid_match else "Unknown"
                signal_strength = int(signal_match.group(1)) if signal_match else -70
                
                return {
                    'ssid': ssid,
                    'signal_strength': signal_strength,
                    'quality': self.calculate_quality_from_signal(signal_strength),
                    'channel': 0,  # Not available in this method
                    'frequency': 0
                }
            except Exception as e:
                print(f"Error getting WiFi info on macOS: {e}")
                return None
    
    def get_wifi_info_linux(self):
        """Get WiFi information on Linux"""
        try:
            # Try using nmcli first (more common on modern Linux)
            result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid,signal,chan', 'dev', 'wifi'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.startswith('yes:'):
                        parts = line.split(':')
                        if len(parts) >= 4:
                            ssid = parts[1]
                            signal = int(parts[2]) if parts[2] else 0
                            channel = int(parts[3]) if parts[3] else 0
                            
                            # Convert signal percentage to dBm (approximate)
                            signal_dbm = -100 + (signal * 0.7)
                            
                            return {
                                'ssid': ssid,
                                'signal_strength': int(signal_dbm),
                                'quality': signal,
                                'channel': channel,
                                'frequency': 2412 + (channel - 1) * 5 if channel <= 14 else 5180 + (channel - 36) * 5
                            }
            
            # Fallback to iwconfig if nmcli fails
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            # ... (previous iwconfig parsing code)
            
        except Exception as e:
            print(f"Error getting WiFi info on Linux: {e}")
            return None
    
    def get_wifi_info_windows(self):
        """Get WiFi information on Windows"""
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                                  capture_output=True, text=True)
            output = result.stdout
            
            ssid_match = re.search(r'SSID\s+: (.+)', output)
            signal_match = re.search(r'Signal\s+: (\d+)%', output)
            channel_match = re.search(r'Channel\s+: (\d+)', output)
            
            ssid = ssid_match.group(1).strip() if ssid_match else "Unknown"
            signal_percent = int(signal_match.group(1)) if signal_match else 0
            channel = int(channel_match.group(1)) if channel_match else 0
            
            # Convert percentage to approximate dBm
            signal_dbm = -100 + (signal_percent * 0.7)
            
            return {
                'ssid': ssid,
                'signal_strength': int(signal_dbm),
                'quality': signal_percent,
                'channel': channel,
                'frequency': 2412 + (channel - 1) * 5 if channel <= 14 else 5180 + (channel - 36) * 5
            }
        except Exception as e:
            print(f"Error getting WiFi info on Windows: {e}")
            return None
    
    def calculate_quality_from_signal(self, signal_dbm):
        """Calculate quality percentage from signal strength"""
        if signal_dbm >= -30:
            return 100
        elif signal_dbm >= -67:
            return 75
        elif signal_dbm >= -70:
            return 50
        elif signal_dbm >= -80:
            return 25
        else:
            return 0
    
    def log_data(self, wifi_info):
        """Log WiFi data to CSV file"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                wifi_info['ssid'],
                wifi_info['signal_strength'],
                wifi_info['quality'],
                wifi_info['channel'],
                wifi_info['frequency']
            ])
    
    def display_info(self, wifi_info):
        """Display WiFi information in a formatted way"""
        print("\n" + "="*50)
        print(f"WiFi Signal Monitor - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Operating System: {self.os_type}")
        print("="*50)
        print(f"Network SSID: {wifi_info['ssid']}")
        print(f"Signal Strength: {wifi_info['signal_strength']} dBm")
        print(f"Signal Quality: {wifi_info['quality']}%")
        
        if wifi_info['channel'] > 0:
            print(f"Channel: {wifi_info['channel']}")
        if wifi_info['frequency'] > 0:
            print(f"Frequency: {wifi_info['frequency']} MHz")
        
        # Signal strength indicator
        if wifi_info['signal_strength'] >= -50:
            status = "Excellent"
        elif wifi_info['signal_strength'] >= -60:
            status = "Good"
        elif wifi_info['signal_strength'] >= -70:
            status = "Fair"
        else:
            status = "Poor"
        
        print(f"Connection Status: {status}")
    
    def monitor(self, interval=5):
        """Main monitoring loop"""
        print(f"Starting WiFi Signal Strength Monitor on {self.os_type}...")
        print(f"Logging data to: {self.log_file}")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                wifi_info = self.get_wifi_info()
                if wifi_info:
                    self.display_info(wifi_info)
                    self.log_data(wifi_info)
                else:
                    print("Unable to retrieve WiFi information")
                    print("Note: On macOS, you may need to run with sudo or check WiFi is enabled")
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")
            print(f"Log saved to: {self.log_file}")

if __name__ == "__main__":
    monitor = WiFiMonitor()
    monitor.monitor(interval=5)  # Monitor every 5 seconds