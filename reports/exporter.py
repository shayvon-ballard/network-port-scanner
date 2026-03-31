import csv
import os
from datetime import datetime

def export_to_csv(scan_result):
    os.makedirs("reports/output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/output/scan_{scan_result['host']}_{timestamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Port", "Status", "Service", "Risk Level"])
        for port in scan_result["open_ports"]:
            writer.writerow([
                port["port"],
                port["status"],
                port["service"],
                port["risk"]
            ])

    return filename