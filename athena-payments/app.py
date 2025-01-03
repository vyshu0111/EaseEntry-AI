from flask import Flask, render_template, request, flash, session
from random import randint
from conn import *

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        number_of_tickets = 0
        total_amount = 0
        booking_id = None

        # Check if the validate button was clicked
        if "validate" in request.form:
            number_of_tickets = get_number_of_tickets_by_booking_email(email)
            if number_of_tickets > 0:
                total_amount = number_of_tickets * 100
                # Store email and number of tickets in session
                session['email'] = email
                session['number_of_tickets'] = number_of_tickets
                session['total_amount'] = total_amount
            else:
                flash("No tickets are found in the booking, please Book first.", "danger")
            return render_template("index.html", email=email, number_of_tickets=number_of_tickets, total_amount=total_amount)

        # Check if the pay button was clicked
        elif "pay" in request.form:
            number_of_tickets = session.get('number_of_tickets', 0)
            total_amount = session.get('total_amount', 0)
            email = session.get('email')

            if number_of_tickets > 0:
                booking_id = randint(1000, 9999)
                flash(f"Your tickets ({number_of_tickets}) are confirmed. Booking ID: {booking_id}", "success")
                send_confirmation_email(email, number_of_tickets, booking_id)
                amount = number_of_tickets * 100
                add_to_payments(booking_id, email, amount)

                # Remove session data after processing payment
                session.pop('email', None)
                session.pop('number_of_tickets', None)
                session.pop('total_amount', None)

            return render_template("index.html", email=email, number_of_tickets=number_of_tickets, booking_id=booking_id)

    return render_template("index.html")

def get_number_of_tickets_by_booking_email(email):
    response = supabase.table("bookings").select("no-of-tickets").eq("booking-email", email).execute()
    if response.data:
        return response.data[0].get("no-of-tickets", 0)
    return 0

if __name__ == "__main__":
    app.run(debug=True)
