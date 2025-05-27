#!/usr/bin/env python3
"""
WiFi Signal Strength Simulator & Analyzer
Author: Bernardo Gallegos Vallejo
Description: Simulates WiFi environments to demonstrate understanding of wireless concepts
"""

import random
import time
import datetime
import csv
import os
import math

class WiFiSimulator:
    def __init__(self):
        self.log_file = "wifi_analysis_log.csv"
        self.setup_log_file()
        
        # Simulate different WiFi environments
        self.environments = {
            "Office": {
                "base_signal": -45,
                "interference": 5,
                "channel_congestion": [1, 6, 11],  # Common 2.4GHz channels
                "peak_hours": [9, 10, 11, 14, 15, 16]  # Business hours
            },
            "Warehouse": {
                "base_signal": -55,
                "interference": 10,
                "channel_congestion": [1, 6, 11],
                "peak_hours": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
            },
            "Data_Center": {
                "base_signal": -40,
                "interference": 3,
                "channel_congestion": [36, 40, 44, 48],  # 5GHz channels
                "peak_hours": list(range(24))  # 24/7 operation
            }
        }
        
        self.current_environment = "Office"
        self.access_points = self.generate_access_points()
    
    def setup_log_file(self):
        """Initialize CSV log file with headers"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp', 'Environment', 'SSID', 'BSSID', 
                    'Signal_Strength_dBm', 'Noise_Floor_dBm', 'SNR_dB',
                    'Channel', 'Frequency_MHz', 'Channel_Utilization_%',
                    'Connected_Clients', 'Interference_Level'
                ])
    
    def generate_access_points(self):
        """Generate realistic access points for the environment"""
        aps = []
        env = self.environments[self.current_environment]
        
        # Generate multiple APs as would be in a real environment
        num_aps = random.randint(3, 8)
        for i in range(num_aps):
            channel = random.choice(env["channel_congestion"])
            aps.append({
                "ssid": f"Corp-WiFi-{i+1}" if self.current_environment != "Warehouse" 
                        else f"WH-Scanner-{i+1}",
                "bssid": f"AA:BB:CC:DD:{i:02X}:{random.randint(0,255):02X}",
                "channel": channel,
                "frequency": self.channel_to_frequency(channel),
                "base_signal": env["base_signal"] + random.randint(-10, 5),
                "clients": random.randint(10, 50)
            })
        return aps
    
    def channel_to_frequency(self, channel):
        """Convert channel number to frequency"""
        if channel <= 14:  # 2.4 GHz band
            return 2412 + (channel - 1) * 5
        else:  # 5 GHz band
            return 5180 + (channel - 36) * 5
    
    def calculate_signal_with_interference(self, base_signal, hour):
        """Calculate signal strength with time-based interference"""
        env = self.environments[self.current_environment]
        
        # Add interference during peak hours
        interference = 0
        if hour in env["peak_hours"]:
            interference = random.randint(0, env["interference"])
        
        # Add random fluctuation
        fluctuation = random.uniform(-3, 3)
        
        # Add distance simulation (people/equipment moving)
        distance_factor = math.sin(time.time() / 10) * 5
        
        return base_signal - interference + fluctuation + distance_factor
    
    def calculate_channel_utilization(self, channel, hour):
        """Calculate channel utilization percentage"""
        base_utilization = 20
        
        # Higher utilization during peak hours
        env = self.environments[self.current_environment]
        if hour in env["peak_hours"]:
            base_utilization += 30
        
        # Add random variation
        utilization = base_utilization + random.randint(-10, 20)
        
        # Ensure within valid range
        return max(0, min(100, utilization))
    
    def calculate_snr(self, signal_strength):
        """Calculate Signal-to-Noise Ratio"""
        noise_floor = -95 + random.randint(-2, 2)  # Typical noise floor
        snr = signal_strength - noise_floor
        return signal_strength, noise_floor, snr
    
    def analyze_environment(self):
        """Analyze current WiFi environment"""
        current_hour = datetime.datetime.now().hour
        results = []
        
        for ap in self.access_points:
            signal = self.calculate_signal_with_interference(
                ap["base_signal"], current_hour
            )
            signal_dbm, noise_floor, snr = self.calculate_snr(signal)
            
            utilization = self.calculate_channel_utilization(
                ap["channel"], current_hour
            )
            
            # Determine interference level
            if snr < 20:
                interference = "High"
            elif snr < 30:
                interference = "Medium"
            else:
                interference = "Low"
            
            results.append({
                'ssid': ap["ssid"],
                'bssid': ap["bssid"],
                'signal_strength': round(signal_dbm, 1),
                'noise_floor': noise_floor,
                'snr': round(snr, 1),
                'channel': ap["channel"],
                'frequency': ap["frequency"],
                'utilization': utilization,
                'clients': ap["clients"] + random.randint(-5, 5),
                'interference': interference
            })
        
        return results
    
    def log_data(self, ap_data):
        """Log WiFi data to CSV file"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for ap in ap_data:
                writer.writerow([
                    timestamp,
                    self.current_environment,
                    ap['ssid'],
                    ap['bssid'],
                    ap['signal_strength'],
                    ap['noise_floor'],
                    ap['snr'],
                    ap['channel'],
                    ap['frequency'],
                    ap['utilization'],
                    ap['clients'],
                    ap['interference']
                ])
    
    def display_analysis(self, ap_data):
        """Display WiFi analysis in a formatted way"""
        print("\n" + "="*80)
        print(f"WiFi Environment Analysis - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Environment: {self.current_environment}")
        print("="*80)
        
        # Sort by signal strength
        ap_data.sort(key=lambda x: x['signal_strength'], reverse=True)
        
        print(f"{'SSID':<20} {'Signal':<8} {'SNR':<8} {'Ch':<4} {'Util%':<7} {'Clients':<8} {'Interference'}")
        print("-"*80)
        
        for ap in ap_data[:5]:  # Show top 5 APs
            print(f"{ap['ssid']:<20} "
                  f"{ap['signal_strength']:<8.1f} "
                  f"{ap['snr']:<8.1f} "
                  f"{ap['channel']:<4} "
                  f"{ap['utilization']:<7} "
                  f"{ap['clients']:<8} "
                  f"{ap['interference']}")
        
        # Channel analysis
        print("\nChannel Congestion Analysis:")
        channel_counts = {}
        for ap in ap_data:
            ch = ap['channel']
            channel_counts[ch] = channel_counts.get(ch, 0) + 1
        
        for ch, count in sorted(channel_counts.items()):
            print(f"  Channel {ch}: {count} APs detected")
        
        # Recommendations
        print("\nRecommendations:")
        high_interference = [ap for ap in ap_data if ap['interference'] == 'High']
        if high_interference:
            print(f"  - {len(high_interference)} APs showing high interference")
            print("  - Consider channel reassignment or power adjustment")
        
        congested_channels = [ch for ch, count in channel_counts.items() if count > 2]
        if congested_channels:
            print(f"  - Channels {congested_channels} are congested")
            print("  - Consider using DFS channels or 5GHz band")
    
    def simulate(self, duration_minutes=5):
        """Run the simulation"""
        print("Starting WiFi Environment Simulator...")
        print(f"Simulating {self.current_environment} environment")
        print(f"Logging data to: {self.log_file}")
        print("Press Ctrl+C to stop simulation\n")
        
        # Allow environment switching
        print("Commands:")
        print("  Type 'office', 'warehouse', or 'data_center' to switch environments")
        print("  Press Ctrl+C to stop\n")
        
        try:
            start_time = time.time()
            while True:
                # Analyze current environment
                ap_data = self.analyze_environment()
                self.display_analysis(ap_data)
                self.log_data(ap_data)
                
                # Wait for next iteration
                time.sleep(10)
                
                # Occasionally regenerate APs (simulating movement/changes)
                if random.random() < 0.1:
                    self.access_points = self.generate_access_points()
                
        except KeyboardInterrupt:
            print("\n\nSimulation stopped by user")
            print(f"Log saved to: {self.log_file}")
            print("\nThis simulation demonstrates understanding of:")
            print("- Signal strength and SNR calculations")
            print("- Channel utilization and interference")
            print("- Time-based network patterns")
            print("- Multi-AP environment analysis")

if __name__ == "__main__":
    simulator = WiFiSimulator()
    simulator.simulate()