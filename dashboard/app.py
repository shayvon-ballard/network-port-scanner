from flask import Flask, render_template, request, redirect, url_for
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scanner.port_scanner import scan_host
from reports.exporter import export_to_csv

app = Flask(__name__)

scan_results = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        host = request.form.get("host", "").strip()
        if host:
            try:
                result = scan_host(host)
                scan_results.insert(0, result)
            except Exception as e:
                error = f"Scan failed: {str(e)}"

    return render_template("index.html", result=result, history=scan_results, error=error)

@app.route("/export/<host>")
def export(host):
    for result in scan_results:
        if result["host"] == host:
            export_to_csv(result)
            break
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)