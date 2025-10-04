from datetime import datetime
import pytz
india = pytz.timezone('Asia/Kolkata')

from sqlalchemy import text
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from app import app

from flask import Flask, render_template, request, flash, redirect, url_for, session

from controllers.models import *
from sqlalchemy import text


@app.route('/')
def home():
    roles = session.get('roles', [])
    email = session.get('email')    
    user = User.query.filter_by(email = email).first()
    
    if not user:
        return render_template('home.html')

    if 'admin' in roles:
        lots = ParkingLot.query.all()
        lot_details = []
        for lot in lots:
            spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
            occupied = sum(1 for spot in spots if spot.status == 'occupied')
            total = len(spots)
            lot_details.append({
                'lot': lot,
                'spots': spots,
                'occupied': occupied,
                'total': total
            })
        return render_template('home.html', lot_details=lot_details)
    else:    
        reservations = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.parking_timestamp.desc()).all()
        return render_template('home.html', reservation=reservations, history=bool(reservations), now=datetime.now(india))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('login'))
        
        if user.password != password:
            flash('Incorrect password.', 'error')
            return redirect(url_for('login'))
        
        session['email'] = user.email
        roles = [role.name for role in user.roles]
        if not roles:
            roles = ['user']
        session['roles'] = roles

        flash('Login successful!', 'success')
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('roles', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == "POST":
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

    if not full_name or not email or not phone_number or not password:
        flash('Oops! Looks like you missed some fields. Please complete the form.', 'error')
        return redirect(url_for('register'))
    
    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('register'))
    
    if len(password)<6:
        flash('Password must be atleast 6 characters long.', 'error')
        return redirect(url_for('register'))
    
    existing_user = User.query.filter_by(email = email).first()
    if existing_user:
        flash('Email already registered', 'error')
        return redirect(url_for('register'))
    
    user_role = Role.query.filter_by(name='user').first()
    user = User(
        full_name = full_name,
        email = email,
        phone_number = phone_number,
        password = password
    )
    db.session.add(user)
    db.session.commit()
    flash('Awesome! You\'re all set. Time to log in and explore.', 'success')
    return redirect(url_for('login'))
    
@app.route('/view_user', methods=['POST'])
def view_user():
    spot_id = request.form['spot_id']
    spot = ParkingSpot.query.get(spot_id)
  
    reservation = Reservation.query.filter_by(spot_id=spot_id).order_by(Reservation.parking_timestamp.desc()).first()
    if reservation:
        user = reservation.user
        return render_template(
            'user_info.html',
            user=user,
            spot=spot,
            reservation=reservation
        )
    else:
        return "No reservation found for this spot", "error"
    
@app.route('/add_lots', methods=['GET', 'POST'])
def add_lots():
    if request.method =='GET':
        return render_template('add_lots.html')
    
    if request.method == 'POST':
        prime_location = request.form.get('prime_location')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        max_spots = request.form.get('max_spots')
        price = request.form.get('price')

        if not prime_location or not address or not pincode or not max_spots or not price:
            flash('All fields are required.', 'error')
            return redirect(url_for('add_lots'))

        existing_lot = ParkingLot.query.filter_by(address=address, pincode=pincode).first()
        if existing_lot:
            flash('Paking Lot with this pincode already exists.', 'error')
            return redirect(url_for('add_lots'))

        try:
            max_spots = int(max_spots)
            price = float(price)

        except ValueError:
            flash('Please enter valid numbers for Max Spots and Price', 'error')
            return redirect(url_for('add_lots'))
        
        new_lot = ParkingLot(
            prime_location = prime_location,
            address = address,
            pincode = pincode,
            max_spots = max_spots,
            price = price
        )

        db.session.add(new_lot)
        db.session.commit()

        for i in range(1, max_spots+1):
            spot_id = f"A{i}"
            new_spot = ParkingSpot(lot_id=new_lot.id, spot_number=spot_id, status='available')
            db.session.add(new_spot)
        db.session.commit()

        flash('Parking Lot and Spots created successfully!', 'success')
        return redirect(url_for('home'))

@app.route('/lot/<int:lot_id>/delete')
def delete_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    
    occupied_spot=ParkingSpot.query.filter_by(lot_id=lot.id, status='occupied').count()
    if occupied_spot>0:
        flash(f'Oops! You can\'t delete this lot while {occupied_spot} spot(s) are still occupied', 'error')
        return redirect(url_for('home'))
    
    spots=ParkingSpot.query.filter_by(lot_id=lot.id).all()
    for spot in spots:
        db.session.delete(spot)

    db.session.delete(lot)
    db.session.commit()
    flash('Parking Lot deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/lot/<int:lot_id>/edit', methods=['GET', 'POST'])
def edit_lot(lot_id):
    lot=ParkingLot.query.get(lot_id)
    
    if request.method=='POST':
        new_location = request.form['prime_location']
        new_address = request.form['address']
        new_pincode = request.form['pincode']
        new_max_spots = int(request.form['max_spots'])
        new_price = request.form['price']

        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id,status='occupied').count()
        if new_max_spots<occupied_spots:
            flash(f'Update failed: At least {occupied_spots} spots are currently occupied. Please adjust accordingly', 'error')
            return redirect(url_for('home'))
        
        lot.prime_location = new_location
        lot.address = new_address
        lot.pincode = new_pincode
        lot.max_spots = new_max_spots
        lot.price = new_price

        existing_spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        
        if new_max_spots>len(existing_spots):
            for i in range(len(existing_spots)+1, new_max_spots+1):
                new_spot = ParkingSpot(
                    lot_id = lot.id,
                    spot_number = f"A{i}",
                    status = 'available'
                )
                db.session.add(new_spot)
        
        elif new_max_spots<len(existing_spots):
            removable = [s for s in reversed(existing_spots) if s.status!= 'occupied']
            to_remove = len(existing_spots) - new_max_spots
            for spot in removable[:to_remove]:
                db.session.delete(spot)

        db.session.commit()
        flash('Parking Lot updated successfully.', 'success')
        return redirect(url_for('home'))
    
    return render_template('edit_lot.html', lot = lot)

@app.route('/admin/users')
def view_users():    
    users = User.query.all()
    return render_template('view_users.html', users=users)

@app.route('/admin/edit-profile', methods=['GET','POST'])
def edit_profile():
    user = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        user.full_name = request.form['name']
        user.phone_number = request.form['phone']

        db.session.commit()
        flash('Profile Updated Successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('edit_profile.html', user=user)

@app.route('/user/reservation')
def book_spot():
    lots = ParkingLot.query.all()
    lot_data=[]
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id = lot.id, status = 'available'). all()
        lot_data.append({'lot': lot, 'available_spots': spots})
    return render_template('book_spots.html', lot_data = lot_data)

@app.route('/user/reservation/lot/<int:lot_id>', methods=['GET', 'POST'], endpoint='confirm_booking')
def book_lot(lot_id):
    user_email = session.get('email')
    user = User.query.filter_by(email=user_email).first()
    if not user:
        flash("User not found.", 'error')
        return redirect(url_for('home'))

    lot = ParkingLot.query.get(lot_id)
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').first()

    if not spot:
        flash("No available spots in this lot.", "error")
        return redirect(url_for('book_spot'))

    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number')
        parking_timestamp = datetime.now(india)
        cost = request.form.get('cost_per_unit')

        spot.status = 'occupied'
        spot.user_email = user_email
        db.session.commit()

        history = Reservation(
            spot_id=spot.id,
            user_id=user.id,
            vehicle_number=vehicle_number,
            parking_timestamp=parking_timestamp,
            status='parked',
            cost_per_unit_time=spot.parking_lot.price,
            total_cost=0,
            leaving_timestamp=None
        )

        db.session.add(history)
        db.session.commit()

        flash(f'Successfully booked {spot.spot_number} spot in {lot.prime_location} Lot!', 'success')
        return redirect(url_for('home'))

    current_time = datetime.now(india).strftime('%Y-%m-%dT%H:%M')
    return render_template('confirm_booking.html', lot=lot, spot=spot, current_time=current_time)

@app.route('/user/confirm/release/spot/<int:reservation_id>', methods = ['GET'])
def confirm_release_spot(reservation_id):
    reservation = Reservation.query.get(reservation_id)
    return render_template('release_spot.html', reservation = reservation)

@app.route('/user/release/<int:reservation_id>', methods=['POST'])
def release_spot(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if reservation.status == 'parked':
        reservation.leaving_timestamp = datetime.now(india)
        if reservation.parking_timestamp.tzinfo is None:
            reservation.parking_timestamp = india.localize(reservation.parking_timestamp)
        duration = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
        reservation.total_cost = round(duration * reservation.cost_per_unit_time, 2)
        reservation.status = 'left'

        spot = ParkingSpot.query.get(reservation.spot_id)
        spot.status = 'available'
        spot.user_email = None

        db.session.commit()
        flash(f"Spot released! Total Cost: ₹{reservation.total_cost}", 'success')
    else:
        flash("Spot already released.", 'error')

    return redirect(url_for('home'))

@app.route('/admin-chart')
def admin_chart():
    query = text('''
        SELECT parking_lot.prime_location, SUM(reservation.total_cost)
        FROM reservation
        JOIN parking_spot ON reservation.spot_id = parking_spot.id
        JOIN parking_lot ON parking_spot.lot_id = parking_lot.id
        GROUP BY parking_lot.prime_location
    ''')
    results = db.session.execute(query).fetchall()

    labels = [row[0] for row in results]
    values = [row[1] for row in results]

    plt.pie(values, labels=labels, autopct = "%1.1f%%", startangle=90)
    plt.title("Revenue From Each Parking Lot", fontweight='bold', pad=20)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_url = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    bar_lables=[]
    occupied_spots_count=[]
    available_spots_count=[]

    lots = ParkingLot.query.all()
    for lot in lots:
        bar_lables.append(lot.prime_location)
        occupied = ParkingSpot.query.filter_by(lot_id = lot.id, status='occupied').count()
        available = ParkingSpot.query.filter_by(lot_id = lot.id, status='available').count()
        occupied_spots_count.append(occupied)
        available_spots_count.append(available)

    x=range(len(bar_lables))
    plt.figure(figsize=(10,6))
    plt.bar(x, occupied_spots_count, width = 0.4, label = 'Occupied', color=['red'])
    plt.bar(x, available_spots_count, width=0.2, label = 'Available', align='edge', color=['green'])
    plt.xticks(x,bar_lables)
    plt.ylabel("Number of Spots")
    plt.title("Spot Status Per Lot")
    plt.legend()


    buf2 = BytesIO()
    plt.tight_layout()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    chart2 = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close()

    return render_template("admin_chart.html", chart_url=chart_url, chart2=chart2)


@app.route('/user/summary/used_spots')
def user_chart():
    query = text("""
    SELECT parking_spot.spot_number, COUNT(reservation.id) as usage_count
    FROM reservation
    JOIN parking_spot ON reservation.spot_id = parking_spot.id
    WHERE reservation.status = 'left'
    GROUP BY parking_spot.spot_number
    """)

    results = db.session.execute(query).fetchall()
    labels = [row[0] for row in results]  # spot_number
    values = [row[1] for row in results]  # from COUNT

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values, color='skyblue', edgecolor='black')
    plt.xlabel("Spot Number")
    plt.ylabel("Number of Times Used")
    plt.title("Already Used Parking Spots", fontweight='bold', pad=20)
 
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart_user_url = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return render_template("user_chart.html", chart_user_url=chart_user_url)













