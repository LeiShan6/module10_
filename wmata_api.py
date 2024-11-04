# Module 10 Assignment: Building an Automated CI/CD Pipeline - Lei Shan
# Part 1: Publishing a REST API Using FLASK
import json
import requests
from flask import Flask, Response

# URL to fetch elevator and escalator incident data
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"
app = Flask(__name__)

# Endpoint to get incidents by machine type (elevators or escalators)
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # Standardize unit_type to uppercase for consistent matching
    unit_type = unit_type.upper()

    # Validate that unit_type is either "elevators" or "escalators"
    if unit_type not in {"ELEVATORS", "ESCALATORS"}:
        return Response("Invalid unit_type. Use 'elevators' or 'escalators'.", status=400, mimetype="text/plain")

    # Map plural form to singular form to match data format
    unit_type_singular = "ELEVATOR" if unit_type == "ELEVATORS" else "ESCALATOR"

    # Fetch data
    response = requests.get(INCIDENTS_URL)
    if response.status_code != 200:
        return Response("Error retrieving data from the API.", status=500, mimetype="text/plain")

    # Parse the JSON response
    data = response.json()

    # Check for "ElevatorIncidents" in data and filter incidents by unit_type
    incidents = [
        {
            "StationCode": incident.get("StationCode"),
            "StationName": incident.get("StationName"),
            "UnitName": incident.get("UnitName"),
            "UnitType": incident.get("UnitType")
        }
        for incident in data.get("ElevatorIncidents", [])
        if incident.get("UnitType") == unit_type_singular
    ]

    # Return the filtered incidents as a JSON response
    return Response(json.dumps(incidents), mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)
