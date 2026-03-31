import socket
from datetime import datetime

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt"
}

HIGH_RISK_PORTS = [21, 23, 445, 3389, 5900]

def get_service(port):
    return COMMON_PORTS.get(port, "Unknown")

def get_risk_level(port):
    if port in HIGH_RISK_PORTS:
        return "HIGH"
    elif port in COMMON_PORTS:
        return "MEDIUM"
    else:
        return "LOW"

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return {
                "port": port,
                "status": "open",
                "service": get_service(port),
                "risk": get_risk_level(port)
            }
    except socket.error:
        pass
    return None

def scan_host(host, ports=None, timeout=1):
    if ports is None:
        ports = list(COMMON_PORTS.keys())

    results = []
    for port in ports:
        result = scan_port(host, port, timeout)
        if result:
            results.append(result)

    return {
        "host": host,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_ports": results,
        "total_open": len(results),
        "high_risk_count": sum(1 for r in results if r["risk"] == "HIGH")
    }