
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
API_URL = (
    "https://vpic.nhtsa.dot.gov/api/vehicles/"
    "GetVehicleVariableList?format=json"
)


@app.route("/items", methods=["GET"])
def get_items():
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        data = response.json()

        filtered = [
            item for item in data["Results"]
            if item.get("GroupName") == "Active Safety System"
        ]

        return jsonify(filtered), 200

    except requests.exceptions.RequestException as error:
        return jsonify({"error": str(error)}), 503

    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Invalid API response"}), 502


if __name__ == "__main__":
    app.run(port=5002, debug=True)
