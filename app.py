from flask import Flask, request, jsonify
import requests
API_KEY = "6654412fe0333669815376b5"
app = Flask(__name__)
@app.route("/", methods=["POST"])
def get_flight_status():
    data = request.get_json()
    try:
        flight_number = int(data.get("queryResult").get("parameters").get("flightnum"))
        airline_code = data.get("queryResult").get("parameters").get("airlinecode")
        flight_date = data.get("queryResult").get("parameters").get("date")
        print(flight_date)
        print(flight_number)
        print(airline_code)
    except (AttributeError, ValueError):
        print("Missing required information")
        return jsonify({"error": "Invalid flight information format."})
    url = f"https://api.flightapi.io/airline/{flight_number}/{airline_code}/{flight_date}?<apikey>"

    try:
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        print(response_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight status: {e}")
        return jsonify({"error": "Error fetching flight status."})

    if "error" in response_data:
        print(response_data["error"]["message"])
        return jsonify({"error": response_data["error"]["message"]})
    else:
        flight_status = response_data.get("data", {}).get("status")
        if flight_status:
            return jsonify({"fulfillmentText": f"Flight {flight_number} ({airline_code}) status: {flight_status}"})
        else:
            return jsonify({"fulfillmentText": f"Flight information not found for {flight_number} ({airline_code}) on {flight_date}"})

if __name__ == "__main__":
    app.run(debug=True)
