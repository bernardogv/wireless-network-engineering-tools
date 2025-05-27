#!/usr/bin/env python3
"""
Channel Plan Visualizer
Author: Bernardo Gallegos Vallejo
Description: Visualizes the channel assignment plan for warehouse AP deployment
"""

import json

def visualize_channel_plan(report_file="channel_optimization_report.json"):
    """Create ASCII visualization of channel assignments"""
    
    try:
        with open(report_file, 'r') as f:
            report = json.load(f)
    except FileNotFoundError:
        print("No report found. Run channel_optimizer.py first.")
        return
    
    layout = report['layout_analysis']
    width = layout['ap_grid']['width']
    length = layout['ap_grid']['length']
    
    # Create channel map from report
    channel_grid = []
    sample_aps = report['channel_plan_summary']['sample_assignments']
    
    print("\n" + "="*60)
    print("CHANNEL ASSIGNMENT VISUALIZATION")
    print("="*60)
    print(f"Facility: {report['warehouse']}")
    print(f"Grid Size: {width} x {length} APs")
    print(f"Primary Band: {report['executive_summary']['primary_band']}")
    print("\nChannel Layout (5 GHz):")
    print("-" * 60)
    
    # Define color codes for channels (using numbers for simplicity)
    channel_colors = {
        36: "36", 40: "40", 44: "44", 48: "48",
        149: "149", 153: "153", 157: "157", 161: "161"
    }
    
    # Generate full grid visualization
    channels_used = report['channel_plan_summary']['channels_used']
    channel_pattern = channels_used * (width * length // len(channels_used) + 1)
    
    print("\nChannel Grid Pattern:")
    print("(Each number represents an AP's channel assignment)")
    print()
    
    for row in range(min(length, 10)):  # Show first 10 rows
        row_channels = []
        for col in range(min(width, 15)):  # Show first 15 columns
            idx = row * width + col
            channel = channel_pattern[idx % len(channel_pattern)]
            row_channels.append(f"{channel:>3}")
        
        print(f"Row {row+1:2}: " + " ".join(row_channels))
    
    if length > 10 or width > 15:
        print("\n... (showing partial grid for clarity)")
    
    # Show channel usage statistics
    print("\n" + "-" * 60)
    print("CHANNEL USAGE SUMMARY:")
    print(f"Unique channels used: {len(channels_used)}")
    print(f"Channels: {', '.join(map(str, sorted(channels_used)))}")
    
    # Calculate minimum channel separation
    sorted_channels = sorted(channels_used)
    min_separation = min(sorted_channels[i+1] - sorted_channels[i] 
                        for i in range(len(sorted_channels)-1))
    print(f"Minimum channel separation: {min_separation * 5} MHz")
    
    # Show coverage statistics
    print("\n" + "-" * 60)
    print("COVERAGE STATISTICS:")
    dimensions = layout['dimensions']
    coverage_area = dimensions['width'] * dimensions['length']
    print(f"Total area: {coverage_area:,} square meters")
    print(f"APs deployed: {width * length}")
    print(f"Area per AP: {coverage_area / (width * length):.1f} square meters")
    print(f"Estimated coverage: {report['executive_summary']['estimated_coverage']}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    visualize_channel_plan()