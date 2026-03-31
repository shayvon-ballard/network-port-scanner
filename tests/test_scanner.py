import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scanner.port_scanner import get_service, get_risk_level, scan_port

# --- Route Tests ---

def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_404_for_unknown_route(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404

# --- Scanner Logic Tests ---

def test_get_service_known_port():
    assert get_service(22) == "SSH"
    assert get_service(80) == "HTTP"
    assert get_service(443) == "HTTPS"
    assert get_service(3389) == "RDP"

def test_get_service_unknown_port():
    assert get_service(9999) == "Unknown"

def test_get_risk_level_high():
    assert get_risk_level(23) == "HIGH"
    assert get_risk_level(3389) == "HIGH"
    assert get_risk_level(445) == "HIGH"

def test_get_risk_level_medium():
    assert get_risk_level(22) == "MEDIUM"
    assert get_risk_level(80) == "MEDIUM"

def test_get_risk_level_low():
    assert get_risk_level(9999) == "LOW"

def test_scan_port_closed():
    result = scan_port("127.0.0.1", 9999, timeout=0.5)
    assert result is None