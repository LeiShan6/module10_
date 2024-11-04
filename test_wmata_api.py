# Module 10 Assignment: Building an Automated CI/CD Pipeline - Lei Shan
# Part 2: Creating Unit Tests for Manual Execution
from wmata_api import app
import json
import unittest

class WMATATest(unittest.TestCase):
    # Ensure both endpoints return a 200 HTTP code
    def test_http_success(self):
        escalator_response = app.test_client().get('/incidents/escalators').status_code
        self.assertEqual(escalator_response, 200, "Expected 200 HTTP status code for /incidents/escalators")

        elevator_response = app.test_client().get('/incidents/elevators').status_code
        self.assertEqual(elevator_response, 200, "Expected 200 HTTP status code for /incidents/elevators")

    # Ensure all returned incidents have the 4 required fields
    def test_required_fields(self):
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]

        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        for incident in json_response:
            for field in required_fields:
                self.assertIn(field, incident, f"Missing required field '{field}' in incident {incident}")

    # Ensure all entries returned by the /escalators endpoint have a UnitType of "ESCALATOR"
    def test_escalators(self):
        response = app.test_client().get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        for incident in json_response:
            if incident.get("UnitType") == "ESCALATOR":
                self.assertEqual(incident.get("UnitType"), "ESCALATOR",
                                 f"Expected 'UnitType' to be 'ESCALATOR', got {incident.get('UnitType')}")

    # Ensure all entries returned by the /elevators endpoint have a UnitType of "ELEVATOR"
    def test_elevators(self):
        response = app.test_client().get('/incidents/elevators')
        json_response = json.loads(response.data.decode())

        for incident in json_response:
            if incident.get("UnitType") == "ELEVATOR":
                self.assertEqual(incident.get("UnitType"), "ELEVATOR",
                                 f"Expected 'UnitType' to be 'ELEVATOR', got {incident.get('UnitType')}")

if __name__ == "__main__":
    unittest.main()
