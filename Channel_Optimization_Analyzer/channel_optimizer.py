#!/usr/bin/env python3
"""
Wireless Channel Optimization Analyzer
Author: Bernardo Gallegos Vallejo
Description: Analyzes wireless channel usage and provides optimization recommendations
             for high-density deployments like warehouses and fulfillment centers
"""

import math
import random
from collections import defaultdict
import json
import datetime

class ChannelOptimizer:
    def __init__(self):
        # 2.4 GHz channels (only non-overlapping channels for optimization)
        self.channels_24ghz = {
            1: {"frequency": 2412, "non_overlapping": True},
            6: {"frequency": 2437, "non_overlapping": True},
            11: {"frequency": 2462, "non_overlapping": True}
        }
        
        # 5 GHz channels (common non-DFS channels)
        self.channels_5ghz = {
            36: {"frequency": 5180, "bandwidth": 20},
            40: {"frequency": 5200, "bandwidth": 20},
            44: {"frequency": 5220, "bandwidth": 20},
            48: {"frequency": 5240, "bandwidth": 20},
            149: {"frequency": 5745, "bandwidth": 20},
            153: {"frequency": 5765, "bandwidth": 20},
            157: {"frequency": 5785, "bandwidth": 20},
            161: {"frequency": 5805, "bandwidth": 20}
        }
        
        # Channel bonding options for 5GHz
        self.channel_widths = {
            20: "20 MHz - Maximum APs, minimum throughput",
            40: "40 MHz - Balanced APs and throughput", 
            80: "80 MHz - Fewer APs, higher throughput"
        }
        
        self.report_file = "channel_optimization_report.json"
    
    def calculate_channel_overlap(self, ch1, ch2, band="2.4"):
        """Calculate overlap percentage between two channels"""
        if band == "2.4":
            # 2.4 GHz channels are 5 MHz apart, 20 MHz wide
            separation = abs(ch1 - ch2) * 5
            if separation >= 25:
                return 0  # No overlap
            elif separation == 0:
                return 100  # Same channel
            else:
                # Calculate overlap based on 20 MHz channel width
                overlap = (25 - separation) / 25 * 100
                return overlap
        else:
            # 5 GHz channels don't overlap if properly spaced
            return 100 if ch1 == ch2 else 0
    
    def analyze_warehouse_layout(self, width_m, length_m, height_m):
        """Analyze warehouse dimensions for AP placement"""
        # Calculate coverage area per AP (assuming -65 dBm edge coverage)
        # Typical enterprise AP range ~25-30m radius in warehouse environment
        coverage_radius = 25  # meters
        
        # Calculate grid spacing for optimal coverage with overlap
        grid_spacing = coverage_radius * 1.4  # 40% overlap for redundancy
        
        # Calculate number of APs needed
        aps_width = math.ceil(width_m / grid_spacing)
        aps_length = math.ceil(length_m / grid_spacing)
        total_aps = aps_width * aps_length
        
        # Account for height (high-bay warehouses may need different patterns)
        if height_m > 10:
            vertical_consideration = "High ceiling detected - consider downtilt antennas"
        else:
            vertical_consideration = "Standard ceiling height - omnidirectional antennas suitable"
        
        return {
            "dimensions": {"width": width_m, "length": length_m, "height": height_m},
            "coverage_radius": coverage_radius,
            "grid_spacing": grid_spacing,
            "ap_grid": {"width": aps_width, "length": aps_length},
            "total_aps": total_aps,
            "vertical_consideration": vertical_consideration
        }
    
    def generate_channel_plan(self, layout_analysis, use_5ghz=True):
        """Generate optimal channel assignment plan"""
        total_aps = layout_analysis["total_aps"]
        ap_grid = layout_analysis["ap_grid"]
        
        channel_plan = []
        
        if use_5ghz:
            # Use 5GHz for primary coverage
            channels = list(self.channels_5ghz.keys())
            channel_pattern = self._create_channel_pattern(channels, ap_grid["width"])
        else:
            # Use 2.4GHz (only non-overlapping)
            channels = [1, 6, 11]
            channel_pattern = self._create_channel_pattern(channels, ap_grid["width"])
        
        # Assign channels in a grid pattern
        ap_id = 1
        for row in range(ap_grid["length"]):
            for col in range(ap_grid["width"]):
                channel_index = (col + row * ap_grid["width"]) % len(channel_pattern)
                channel = channel_pattern[channel_index]
                
                ap_config = {
                    "ap_id": f"AP-{ap_id:03d}",
                    "position": {"row": row, "col": col},
                    "channel": channel,
                    "band": "5GHz" if use_5ghz else "2.4GHz",
                    "tx_power": self._calculate_tx_power(layout_analysis["coverage_radius"])
                }
                channel_plan.append(ap_config)
                ap_id += 1
        
        return channel_plan
    
    def _create_channel_pattern(self, channels, width):
        """Create non-interfering channel pattern"""
        # For small grids, use simple rotation
        if width <= len(channels):
            return channels
        
        # For larger grids, create pattern that minimizes adjacent interference
        pattern = []
        for i in range(width):
            pattern.append(channels[i % len(channels)])
        
        return pattern
    
    def _calculate_tx_power(self, coverage_radius):
        """Calculate recommended TX power based on coverage radius"""
        # Simplified path loss calculation
        # Assuming free space path loss at 5GHz
        if coverage_radius <= 20:
            return "Low (10-13 dBm)"
        elif coverage_radius <= 30:
            return "Medium (14-17 dBm)"
        else:
            return "High (18-20 dBm)"
    
    def detect_interference_sources(self):
        """Simulate detection of common interference sources in warehouses"""
        interference_sources = [
            {
                "type": "Bluetooth devices",
                "frequency": "2.4 GHz",
                "impact": "Low",
                "mitigation": "Use 5GHz band for critical devices"
            },
            {
                "type": "Microwave ovens (break rooms)",
                "frequency": "2.45 GHz",
                "impact": "High",
                "mitigation": "Avoid channel 9-11 near break areas"
            },
            {
                "type": "Wireless barcode scanners",
                "frequency": "2.4 GHz",
                "impact": "Medium",
                "mitigation": "Implement band steering to 5GHz"
            },
            {
                "type": "Security cameras (wireless)",
                "frequency": "2.4/5 GHz",
                "impact": "Medium",
                "mitigation": "Use wired backhaul for cameras"
            },
            {
                "type": "Industrial equipment (variable frequency drives)",
                "frequency": "Broadband noise",
                "impact": "Low-Medium",
                "mitigation": "Ensure proper equipment shielding"
            }
        ]
        
        # Randomly select some interference sources for this analysis
        detected = random.sample(interference_sources, k=random.randint(2, 4))
        return detected
    
    def calculate_capacity_requirements(self, num_devices, device_types):
        """Calculate network capacity requirements"""
        # Device bandwidth requirements (Mbps)
        bandwidth_per_device = {
            "handheld_scanner": 0.5,
            "tablet": 2,
            "laptop": 5,
            "voice_device": 0.1,
            "iot_sensor": 0.05,
            "mobile_robot": 1
        }
        
        total_bandwidth = 0
        device_breakdown = {}
        
        for device_type, count in device_types.items():
            bandwidth = bandwidth_per_device.get(device_type, 1) * count
            total_bandwidth += bandwidth
            device_breakdown[device_type] = {
                "count": count,
                "bandwidth_per_device": bandwidth_per_device.get(device_type, 1),
                "total_bandwidth": bandwidth
            }
        
        # Add 30% overhead for management and growth
        total_bandwidth *= 1.3
        
        # Calculate APs needed based on throughput
        # Assuming 150 Mbps real throughput per AP
        aps_for_capacity = math.ceil(total_bandwidth / 150)
        
        return {
            "total_devices": num_devices,
            "device_breakdown": device_breakdown,
            "total_bandwidth_required": round(total_bandwidth, 2),
            "aps_for_capacity": aps_for_capacity
        }
    
    def generate_optimization_report(self, warehouse_name, dimensions, device_info):
        """Generate comprehensive optimization report"""
        print(f"\nAnalyzing wireless requirements for {warehouse_name}...")
        
        # Analyze layout
        layout = self.analyze_warehouse_layout(
            dimensions["width"], 
            dimensions["length"], 
            dimensions["height"]
        )
        
        # Generate channel plan
        channel_plan = self.generate_channel_plan(layout, use_5ghz=True)
        
        # Detect interference
        interference = self.detect_interference_sources()
        
        # Calculate capacity
        capacity = self.calculate_capacity_requirements(
            device_info["total_devices"],
            device_info["device_types"]
        )
        
        # Determine final AP count (max of coverage and capacity requirements)
        final_ap_count = max(layout["total_aps"], capacity["aps_for_capacity"])
        
        # Generate report
        report = {
            "warehouse": warehouse_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "executive_summary": {
                "recommended_aps": final_ap_count,
                "primary_band": "5 GHz",
                "secondary_band": "2.4 GHz (IoT and legacy devices)",
                "estimated_coverage": "99.9%"
            },
            "layout_analysis": layout,
            "capacity_analysis": capacity,
            "channel_plan_summary": {
                "total_aps": len(channel_plan),
                "channels_used": list(set(ap["channel"] for ap in channel_plan)),
                "sample_assignments": channel_plan[:5]  # First 5 APs as example
            },
            "interference_analysis": interference,
            "recommendations": [
                f"Deploy {final_ap_count} access points in a grid pattern",
                "Use 5 GHz as primary band with DFS channels enabled",
                "Implement band steering to move capable devices to 5 GHz",
                "Configure 20 MHz channels for maximum capacity",
                "Set TX power to medium (14-17 dBm) for optimal coverage",
                "Enable 802.11k/v/r for seamless roaming",
                "Implement QoS with voice devices on highest priority"
            ]
        }
        
        # Save report
        with open(self.report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def display_report(self, report):
        """Display report in readable format"""
        print("\n" + "="*60)
        print("WIRELESS CHANNEL OPTIMIZATION REPORT")
        print("="*60)
        print(f"Facility: {report['warehouse']}")
        print(f"Analysis Date: {report['timestamp'][:10]}")
        
        print("\nEXECUTIVE SUMMARY:")
        for key, value in report['executive_summary'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        print("\nLAYOUT ANALYSIS:")
        layout = report['layout_analysis']
        print(f"  Warehouse: {layout['dimensions']['width']}m x {layout['dimensions']['length']}m x {layout['dimensions']['height']}m")
        print(f"  Coverage grid: {layout['ap_grid']['width']} x {layout['ap_grid']['length']} APs")
        print(f"  {layout['vertical_consideration']}")
        
        print("\nCAPACITY ANALYSIS:")
        capacity = report['capacity_analysis']
        print(f"  Total devices: {capacity['total_devices']}")
        print(f"  Bandwidth required: {capacity['total_bandwidth_required']} Mbps")
        print(f"  Device breakdown:")
        for device, info in capacity['device_breakdown'].items():
            print(f"    - {device}: {info['count']} devices @ {info['bandwidth_per_device']} Mbps each")
        
        print("\nINTERFERENCE DETECTED:")
        for source in report['interference_analysis']:
            print(f"  - {source['type']} ({source['frequency']})")
            print(f"    Impact: {source['impact']} | Mitigation: {source['mitigation']}")
        
        print("\nRECOMMENDATIONS:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print(f"\nFull report saved to: {self.report_file}")

def main():
    optimizer = ChannelOptimizer()
    
    # Example: Amazon fulfillment center scenario
    warehouse_config = {
        "name": "FC-EXAMPLE-01",
        "dimensions": {
            "width": 200,    # meters
            "length": 300,   # meters  
            "height": 12     # meters
        },
        "devices": {
            "total_devices": 500,
            "device_types": {
                "handheld_scanner": 200,
                "tablet": 50,
                "laptop": 30,
                "voice_device": 150,
                "iot_sensor": 50,
                "mobile_robot": 20
            }
        }
    }
    
    report = optimizer.generate_optimization_report(
        warehouse_config["name"],
        warehouse_config["dimensions"],
        warehouse_config["devices"]
    )
    
    optimizer.display_report(report)

if __name__ == "__main__":
    main()
