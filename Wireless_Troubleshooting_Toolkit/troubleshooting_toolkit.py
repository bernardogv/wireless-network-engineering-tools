#!/usr/bin/env python3
"""
Wireless Network Troubleshooting Toolkit
Author: Bernardo Gallegos Vallejo
Description: Automated wireless troubleshooting tool that identifies common issues
             and performs root cause analysis for warehouse/enterprise environments
"""

import datetime
import random
import json
from enum import Enum
from collections import defaultdict, deque

class IssueType(Enum):
    CONNECTIVITY = "Connectivity Issue"
    PERFORMANCE = "Performance Degradation"
    ROAMING = "Roaming Problems"
    INTERFERENCE = "RF Interference"
    CAPACITY = "Capacity Exceeded"
    AUTHENTICATION = "Authentication Failures"
    COVERAGE = "Coverage Gap"

class SeverityLevel(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class WirelessTroubleshooter:
    def __init__(self):
        self.issue_history = deque(maxlen=1000)  # Keep last 1000 issues
        self.resolution_database = self._build_resolution_database()
        self.diagnostic_results = {}
        self.report_file = "troubleshooting_report.json"
        
    def _build_resolution_database(self):
        """Build database of known issues and resolutions"""
        return {
            IssueType.CONNECTIVITY: {
                "symptoms": [
                    "Client cannot connect to SSID",
                    "Frequent disconnections",
                    "Cannot obtain IP address",
                    "Connection timeouts"
                ],
                "diagnostics": [
                    "Check signal strength",
                    "Verify SSID broadcast",
                    "Check authentication settings",
                    "Verify DHCP pool availability",
                    "Check VLAN configuration"
                ],
                "common_causes": {
                    "Signal too weak": {
                        "threshold": -75,  # dBm
                        "resolution": "Increase AP density or TX power"
                    },
                    "Authentication mismatch": {
                        "check": "802.1X vs PSK configuration",
                        "resolution": "Verify client supplicant settings"
                    },
                    "DHCP exhaustion": {
                        "check": "DHCP pool utilization > 90%",
                        "resolution": "Expand DHCP scope or reduce lease time"
                    },
                    "Wrong VLAN": {
                        "check": "VLAN ID mismatch",
                        "resolution": "Correct VLAN assignment on SSID"
                    }
                }
            },
            IssueType.PERFORMANCE: {
                "symptoms": [
                    "Slow data transfer",
                    "High latency",
                    "Intermittent connectivity",
                    "Poor application performance"
                ],
                "diagnostics": [
                    "Measure throughput",
                    "Check channel utilization",
                    "Analyze retry rates",
                    "Check for hidden nodes",
                    "Measure SNR"
                ],
                "common_causes": {
                    "High channel utilization": {
                        "threshold": 80,  # percent
                        "resolution": "Change channel or add more APs"
                    },
                    "Co-channel interference": {
                        "check": "Multiple APs on same channel",
                        "resolution": "Implement proper channel plan"
                    },
                    "Low SNR": {
                        "threshold": 20,  # dB
                        "resolution": "Reduce interference or improve signal"
                    },
                    "Client density": {
                        "threshold": 50,  # clients per AP
                        "resolution": "Add capacity with more APs"
                    }
                }
            },
            IssueType.ROAMING: {
                "symptoms": [
                    "Devices stick to distant APs",
                    "Connection drops during movement",
                    "Voice call quality issues",
                    "Slow roaming transitions"
                ],
                "diagnostics": [
                    "Check 802.11k/v/r support",
                    "Analyze roaming thresholds",
                    "Verify AP overlap",
                    "Check roaming logs"
                ],
                "common_causes": {
                    "Insufficient AP overlap": {
                        "threshold": -67,  # dBm at cell edge
                        "resolution": "Adjust AP placement for 20% overlap"
                    },
                    "Sticky client behavior": {
                        "check": "Client roaming aggressiveness",
                        "resolution": "Enable 802.11v BSS transition"
                    },
                    "Missing fast roaming": {
                        "check": "802.11r not enabled",
                        "resolution": "Enable fast BSS transition"
                    }
                }
            },
            IssueType.INTERFERENCE: {
                "symptoms": [
                    "Intermittent performance issues",
                    "High retry rates",
                    "CRC errors",
                    "Unpredictable behavior"
                ],
                "diagnostics": [
                    "Spectrum analysis",
                    "Check non-WiFi interference",
                    "Analyze channel overlap",
                    "Review error counters"
                ],
                "common_causes": {
                    "Non-WiFi interference": {
                        "sources": ["Bluetooth", "Microwaves", "Radar"],
                        "resolution": "Change channels or shield source"
                    },
                    "Adjacent channel interference": {
                        "check": "Overlapping channels in use",
                        "resolution": "Use only non-overlapping channels"
                    },
                    "Rogue APs": {
                        "check": "Unknown SSIDs detected",
                        "resolution": "Locate and remove rogue devices"
                    }
                }
            }
        }
    
    def diagnose_issue(self, issue_type, symptoms, environment_data):
        """Perform automated diagnosis based on symptoms"""
        diagnosis = {
            "timestamp": datetime.datetime.now().isoformat(),
            "issue_type": issue_type.value,
            "symptoms": symptoms,
            "severity": self._calculate_severity(issue_type, symptoms),
            "environment": environment_data,
            "diagnostics_performed": [],
            "findings": [],
            "recommendations": []
        }
        
        # Get relevant diagnostics for issue type
        if issue_type in self.resolution_database:
            issue_info = self.resolution_database[issue_type]
            
            # Perform diagnostics
            for diagnostic in issue_info["diagnostics"]:
                result = self._perform_diagnostic(diagnostic, environment_data)
                diagnosis["diagnostics_performed"].append({
                    "test": diagnostic,
                    "result": result
                })
            
            # Analyze common causes
            for cause, details in issue_info["common_causes"].items():
                if self._check_condition(cause, details, environment_data):
                    diagnosis["findings"].append({
                        "cause": cause,
                        "details": details,
                        "confidence": random.uniform(0.7, 0.95)  # Simulated confidence
                    })
                    diagnosis["recommendations"].append(details.get("resolution", ""))
        
        # Add to history
        self.issue_history.append(diagnosis)
        self.diagnostic_results = diagnosis
        
        return diagnosis
    
    def _calculate_severity(self, issue_type, symptoms):
        """Calculate issue severity based on type and symptoms"""
        # Critical: Connectivity issues affecting many users
        if issue_type == IssueType.CONNECTIVITY and len(symptoms) > 2:
            return SeverityLevel.CRITICAL.name
        
        # High: Performance or roaming issues in production
        if issue_type in [IssueType.PERFORMANCE, IssueType.ROAMING]:
            return SeverityLevel.HIGH.name
        
        # Medium: Interference or capacity issues
        if issue_type in [IssueType.INTERFERENCE, IssueType.CAPACITY]:
            return SeverityLevel.MEDIUM.name
        
        return SeverityLevel.LOW.name
    
    def _perform_diagnostic(self, diagnostic, environment_data):
        """Simulate diagnostic test results"""
        # In real implementation, these would interface with actual tools
        diagnostic_results = {
            "Check signal strength": f"{environment_data.get('signal_strength', -65)} dBm",
            "Verify SSID broadcast": "SSID visible" if random.random() > 0.1 else "SSID hidden",
            "Check authentication settings": "WPA2-Enterprise configured correctly",
            "Verify DHCP pool availability": f"{random.randint(60, 95)}% utilized",
            "Check VLAN configuration": f"VLAN {environment_data.get('vlan', 100)} configured",
            "Measure throughput": f"{random.randint(50, 150)} Mbps",
            "Check channel utilization": f"{random.randint(40, 90)}%",
            "Analyze retry rates": f"{random.randint(5, 30)}%",
            "Measure SNR": f"{random.randint(15, 35)} dB",
            "Check 802.11k/v/r support": "Enabled" if random.random() > 0.3 else "Disabled",
            "Spectrum analysis": "Interference detected on channel 6" if random.random() > 0.5 else "Clear"
        }
        
        return diagnostic_results.get(diagnostic, "Test completed")
    
    def _check_condition(self, cause, details, environment_data):
        """Check if a specific condition is met"""
        # Simulate condition checking
        if "threshold" in details:
            if "signal" in cause.lower():
                return environment_data.get("signal_strength", -65) < details["threshold"]
            elif "utilization" in cause.lower():
                return random.randint(70, 95) > details["threshold"]
            elif "snr" in cause.lower():
                return random.randint(15, 25) < details["threshold"]
        
        # Random chance for other conditions
        return random.random() > 0.6
    
    def analyze_patterns(self):
        """Analyze historical issues to identify patterns"""
        if len(self.issue_history) < 10:
            return {"message": "Insufficient data for pattern analysis"}
        
        patterns = {
            "issue_frequency": defaultdict(int),
            "time_patterns": defaultdict(list),
            "location_patterns": defaultdict(int),
            "recurring_issues": []
        }
        
        # Analyze issue frequency
        for issue in self.issue_history:
            patterns["issue_frequency"][issue["issue_type"]] += 1
            
            # Extract hour for time pattern analysis
            timestamp = datetime.datetime.fromisoformat(issue["timestamp"])
            hour = timestamp.hour
            patterns["time_patterns"][issue["issue_type"]].append(hour)
            
            # Location patterns (if available)
            location = issue["environment"].get("location", "Unknown")
            patterns["location_patterns"][location] += 1
        
        # Identify recurring issues
        issue_counts = defaultdict(int)
        for issue in self.issue_history:
            key = f"{issue['issue_type']}_{issue['symptoms'][0] if issue['symptoms'] else ''}"
            issue_counts[key] += 1
        
        patterns["recurring_issues"] = [
            {"issue": k, "occurrences": v} 
            for k, v in issue_counts.items() 
            if v > 2
        ]
        
        return patterns
    
    def generate_runbook(self, issue_type):
        """Generate automated runbook for specific issue type"""
        if issue_type not in self.resolution_database:
            return {"error": "Issue type not found"}
        
        issue_info = self.resolution_database[issue_type]
        
        runbook = {
            "title": f"Troubleshooting Runbook: {issue_type.value}",
            "created": datetime.datetime.now().isoformat(),
            "issue_type": issue_type.value,
            "steps": []
        }
        
        # Step 1: Identify symptoms
        runbook["steps"].append({
            "step": 1,
            "action": "Identify Symptoms",
            "details": "Check for the following symptoms:",
            "checklist": issue_info["symptoms"]
        })
        
        # Step 2: Initial diagnostics
        runbook["steps"].append({
            "step": 2,
            "action": "Run Initial Diagnostics",
            "details": "Perform these diagnostic tests:",
            "checklist": issue_info["diagnostics"]
        })
        
        # Step 3: Check common causes
        step_num = 3
        for cause, details in issue_info["common_causes"].items():
            runbook["steps"].append({
                "step": step_num,
                "action": f"Check for {cause}",
                "details": details.get("check", f"Verify {cause}"),
                "resolution": details.get("resolution", "Apply standard fix")
            })
            step_num += 1
        
        # Final step: Escalation
        runbook["steps"].append({
            "step": step_num,
            "action": "Escalation",
            "details": "If issue persists after all checks:",
            "checklist": [
                "Document all findings",
                "Collect debug logs",
                "Escalate to L3 support",
                "Create ticket with all diagnostic data"
            ]
        })
        
        return runbook
    
    def generate_report(self):
        """Generate comprehensive troubleshooting report"""
        patterns = self.analyze_patterns()
        
        report = {
            "report_title": "Wireless Network Troubleshooting Analysis",
            "generated": datetime.datetime.now().isoformat(),
            "summary": {
                "total_issues_analyzed": len(self.issue_history),
                "most_common_issue": max(patterns["issue_frequency"].items(), 
                                        key=lambda x: x[1])[0] if patterns["issue_frequency"] else "N/A",
                "critical_issues": sum(1 for i in self.issue_history 
                                     if i["severity"] == SeverityLevel.CRITICAL.name)
            },
            "latest_diagnosis": self.diagnostic_results,
            "patterns": patterns,
            "recommendations": self._generate_recommendations(patterns)
        }
        
        # Save report
        with open(self.report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _generate_recommendations(self, patterns):
        """Generate recommendations based on patterns"""
        recommendations = []
        
        # Check for high frequency issues
        for issue_type, count in patterns["issue_frequency"].items():
            if count > 5:
                recommendations.append({
                    "priority": "High",
                    "issue": issue_type,
                    "recommendation": f"Frequent {issue_type} detected. Consider systematic review of infrastructure."
                })
        
        # Check for time-based patterns
        for issue_type, hours in patterns["time_patterns"].items():
            if hours:
                peak_hour = max(set(hours), key=hours.count)
                if hours.count(peak_hour) > 3:
                    recommendations.append({
                        "priority": "Medium",
                        "issue": f"{issue_type} peaks at {peak_hour}:00",
                        "recommendation": "Consider capacity planning for peak hours"
                    })
        
        return recommendations

def simulate_warehouse_issue():
    """Simulate a real warehouse wireless issue"""
    troubleshooter = WirelessTroubleshooter()
    
    # Simulate performance issue in warehouse
    print("="*60)
    print("WIRELESS TROUBLESHOOTING TOOLKIT")
    print("="*60)
    print("\nScenario: Warehouse staff reporting slow scanner performance")
    print("Location: Shipping area, rows 45-50")
    print("Time: Peak shipping hours (14:00)")
    
    symptoms = [
        "Slow data transfer",
        "Scanner app freezing",
        "Intermittent connectivity"
    ]
    
    environment = {
        "location": "Shipping_Area_West",
        "signal_strength": -72,
        "connected_clients": 85,
        "channel": 6,
        "vlan": 200,
        "ap_model": "Cisco 9130",
        "time": "14:00"
    }
    
    # Run diagnosis
    print("\nRunning automated diagnostics...")
    diagnosis = troubleshooter.diagnose_issue(
        IssueType.PERFORMANCE,
        symptoms,
        environment
    )
    
    # Display results
    print("\nDIAGNOSIS RESULTS:")
    print(f"Severity: {diagnosis['severity']}")
    print(f"\nDiagnostics performed:")
    for diag in diagnosis["diagnostics_performed"]:
        print(f"  - {diag['test']}: {diag['result']}")
    
    print(f"\nRoot Cause Analysis:")
    for finding in diagnosis["findings"]:
        print(f"  - {finding['cause']} (Confidence: {finding['confidence']:.0%})")
    
    print(f"\nRecommendations:")
    for rec in diagnosis["recommendations"]:
        print(f"  - {rec}")
    
    # Generate runbook
    print("\n" + "-"*60)
    print("Generating troubleshooting runbook...")
    runbook = troubleshooter.generate_runbook(IssueType.PERFORMANCE)
    print(f"Runbook created: {runbook['title']}")
    
    # Save runbook
    with open("performance_runbook.json", 'w') as f:
        json.dump(runbook, f, indent=2)
    
    print("Runbook saved to: performance_runbook.json")
    
    # Generate report
    report = troubleshooter.generate_report()
    print(f"\nFull report saved to: {troubleshooter.report_file}")

if __name__ == "__main__":
    simulate_warehouse_issue()
