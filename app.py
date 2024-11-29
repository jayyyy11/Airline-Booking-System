from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flights')
    flights = cursor.fetchall()
    conn.close()
    return render_template('index.html', flights=flights)

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    if request.method == 'POST':
        departure = request.form['departure']
        arrival = request.form['arrival']
        conn = get_db_connection()
        flights = conn.execute('SELECT * FROM flights WHERE departure_airport = ? AND arrival_airport = ?',
                               (departure, arrival)).fetchall()
        conn.close()
        return render_template('flights.html', flights=flights)
    return render_template('flights.html', flights=[])

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book(flight_id):
    if request.method == 'POST':
        user_id = 1  # Assume a logged-in user with user_id 1
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (user_id, flight_id, booking_date, status) VALUES (?, ?, CURRENT_TIMESTAMP, ?)',
                     (user_id, flight_id, 'Booked'))
        conn.commit()
        conn.close()
        return redirect(url_for('confirmation'))
    return render_template('booking.html', flight_id=flight_id)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        airline = request.form['airline']
        flight_number = request.form['flight_number']
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        total_seats = request.form['total_seats']
        price = request.form['price']

        conn = get_db_connection()
        conn.execute('INSERT INTO flights (airline, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, total_seats, available_seats, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (airline, flight_number, departure_airport, arrival_airport, departure_time, arrival_time, total_seats, total_seats, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_flight.html')

if __name__ == '__main__':
    app.run(debug=True)