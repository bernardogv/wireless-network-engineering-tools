#!/usr/bin/env python3
"""
Diagnostic Flowchart Generator
Author: Bernardo Gallegos Vallejo
Description: Generates visual troubleshooting flowcharts for wireless issues
"""

def generate_connectivity_flowchart():
    """Generate ASCII flowchart for connectivity troubleshooting"""
    
    flowchart = """
    WIRELESS CONNECTIVITY TROUBLESHOOTING FLOWCHART
    ==============================================
    
                    [Client Cannot Connect]
                            |
                            v
                    <Signal Strength OK?>
                    /                  \\
                  NO                    YES
                  |                      |
                  v                      v
          [Check Coverage]         <SSID Visible?>
          - Add AP                /            \\
          - Increase TX Power   NO              YES
          - Relocate AP         |                |
                               v                 v
                        [Check SSID Config]  <Auth Success?>
                        - Enable broadcast   /            \\
                        - Verify SSID name  NO            YES
                                           |               |
                                           v               v
                                    [Check Auth Type]  <Gets IP?>
                                    - PSK vs 802.1X   /        \\
                                    - Credentials    NO         YES
                                    - RADIUS server   |          |
                                                     v          v
                                              [Check DHCP]   [Connected]
                                              - Pool size     SUCCESS!
                                              - Lease time
                                              - VLAN config
    
    Common Solutions:
    ----------------
    1. Signal Issues: Aim for -67 dBm or better at client location
    2. Auth Issues: Verify WPA2 settings match between client and AP
    3. DHCP Issues: Ensure VLAN has DHCP scope with available addresses
    4. SSID Issues: Confirm SSID is broadcasting and spelled correctly
    """
    
    return flowchart

def generate_performance_flowchart():
    """Generate ASCII flowchart for performance troubleshooting"""
    
    flowchart = """
    WIRELESS PERFORMANCE TROUBLESHOOTING FLOWCHART
    =============================================
    
                    [Slow Performance]
                            |
                            v
                    <Check SNR > 25dB?>
                    /                \\
                  NO                  YES
                  |                    |
                  v                    v
          [Improve SNR]          <Channel Util < 60%?>
          - Reduce noise         /                    \\
          - Improve signal      NO                     YES
          - Change channel      |                       |
                               v                        v
                    [Channel Congestion]          <Retry Rate < 10%?>
                    - Change channel              /                  \\
                    - Reduce channel width       NO                   YES
                    - Add more APs               |                     |
                                                v                     v
                                        [High Interference]    <Client Count < 30?>
                                        - Find source          /                \\
                                        - Shield/remove       NO                 YES
                                        - Change band         |                   |
                                                             v                   v
                                                    [Capacity Issue]      [Check Backend]
                                                    - Add more APs        - Wired network
                                                    - Load balance        - Server/app
                                                    - Band steering       - WAN link
    
    Performance Targets:
    -------------------
    - SNR: > 25 dB (30+ dB ideal)
    - Channel Utilization: < 60% (< 40% ideal)
    - Retry Rate: < 10% (< 5% ideal)
    - Clients per AP: < 30 for scanners, < 50 for IoT
    """
    
    return flowchart

def generate_roaming_flowchart():
    """Generate ASCII flowchart for roaming troubleshooting"""
    
    flowchart = """
    WIRELESS ROAMING TROUBLESHOOTING FLOWCHART
    =========================================
    
                    [Roaming Issues]
                            |
                            v
                    <802.11k Enabled?>
                    /               \\
                  NO                 YES
                  |                   |
                  v                   v
          [Enable 802.11k]      <802.11v Enabled?>
          Neighbor reports      /               \\
                              NO                 YES
                              |                   |
                              v                   v
                      [Enable 802.11v]      <802.11r Enabled?>
                      BSS Transition        /               \\
                                          NO                 YES
                                          |                   |
                                          v                   v
                                  [Enable 802.11r]    <Check Coverage Overlap>
                                  Fast BSS Trans      -67dBm at boundaries?
                                                     /                    \\
                                                   NO                      YES
                                                   |                        |
                                                   v                        v
                                           [Adjust Coverage]         <Min RSSI Set?>
                                           - AP placement           /            \\
                                           - TX power              NO             YES
                                                                  |               |
                                                                  v               v
                                                          [Set Min RSSI]   [Check Client]
                                                          -75 to -80 dBm   - Roam aggress
                                                                          - Driver update
    
    Roaming Best Practices:
    ----------------------
    - Cell overlap: 15-20% at -67 dBm
    - Min RSSI: -75 to -80 dBm (forces roam)
    - Enable all: 802.11k + v + r
    - Same VLAN across APs for L2 roaming
    """
    
    return flowchart

def save_flowcharts():
    """Save all flowcharts to files"""
    flowcharts = {
        "connectivity_flowchart.txt": generate_connectivity_flowchart(),
        "performance_flowchart.txt": generate_performance_flowchart(),
        "roaming_flowchart.txt": generate_roaming_flowchart()
    }
    
    for filename, content in flowcharts.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Saved: {filename}")

if __name__ == "__main__":
    print("Generating Wireless Troubleshooting Flowcharts...")
    print("="*50)
    
    # Display connectivity flowchart
    print(generate_connectivity_flowchart())
    
    # Save all flowcharts
    save_flowcharts()
    
    print("\nFlowcharts generated successfully!")
    print("These visual guides help with systematic troubleshooting")
