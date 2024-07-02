from flask import Flask, jsonify, request
from databaseutils import get_all_booking_availability, add_booking, get_all_records

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello and welcome to Wema Therapy :)"


@app.route('/database')
def see_db():
    response = get_all_records()
    return jsonify(response)


@app.route('/availability/<date>')
def get_bookings(date):
    response = get_all_booking_availability(date)
    if response:
        return jsonify(response)
    else:
        return jsonify({"error": "No availability found for the given date"}), 404


@app.route("/booking", methods=["PUT"])
def book_appointment():
    booking = request.get_json()
    response = add_booking(
        _date=booking['date'],
        therapist_name=booking['therapist_name'],
        time=booking['time'],
        customer=booking['customer']
    )
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
