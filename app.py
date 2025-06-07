from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask server is running.'

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    if 'latitude' in data and 'longitude' in data:
        print(f"Received location: Latitude={data['latitude']}, Longitude={data['longitude']}")
        return jsonify({"status": "success", "message": "Location updated"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
