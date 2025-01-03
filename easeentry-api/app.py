from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
import requests
from conn import *
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
# Function to add a booking
def add_booking(booking_email, phone, ticks):
    """
    Creates a booking with the user's email (text), phone number (numeric), and number of tickets (numeric).
    """
    response = supabase.table("bookings").insert({
        "booking-email": booking_email,
        "phone-number": phone,
        "no-of-tickets": ticks
    }).execute()

    if response.data:
        return {"success": True, "message": "Booking is made successfully"}
    else:
        return {"success": False, "message": "Booking is not successful"}

# Function to get booking details by booking ID
def get_details_of_booking_id(booking_id):
    """
    Fetches booking details from the 'payments' table based on booking ID.
    """
    response = supabase.table("payments").select("*").eq("booking-id", booking_id).execute()
    return response

# REST endpoint to add a booking (POST)
@app.route('/api/bookings', methods=['POST'])
def add_booking_endpoint():
    data = request.json
    booking_email = data.get('booking_email')
    phone = data.get('phone')
    ticks = data.get('ticks')

    if not booking_email or not isinstance(booking_email, str):
        return jsonify({"error": "Invalid or missing booking email"}), 400
    if phone is None or not isinstance(phone, int):
        return jsonify({"error": "Invalid or missing phone number"}), 400
    if ticks is None or not isinstance(ticks, int):
        return jsonify({"error": "Invalid or missing number of tickets"}), 400

    result = add_booking(booking_email, phone, ticks)
    
    if result["success"]:
        return jsonify({"message": result["message"]}), 201
    else:
        return jsonify({"error": result["message"]}), 400

# REST endpoint to get booking details by booking ID (GET)
@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    response = get_details_of_booking_id(booking_id)
    
    if response.data:
        return jsonify({"data": response.data}), 200
    else:
        return jsonify({"error": "Booking not found"}), 404
    

@app.route('/api/websiteinformation', methods=['GET'])
def get_website_information():
    url = 'https://athenamuseum.vercel.app'
    
    # Send a request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return jsonify({'error': 'Unable to fetch the website'}), 500
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all the text from the page
    text = soup.get_text(separator=' ', strip=True)
    
    # Prepare the JSON response
    data = {
        'url': url,
        'content': text
    }

    # Return the JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
