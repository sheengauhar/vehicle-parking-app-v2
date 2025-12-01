from celery import Celery 
from celery.schedules import crontab 
from datetime import datetime, timedelta
from app import app, db
from mail import send_email
from controllers.models import User, Reservation, ParkingLot, ParkingSpot
from sqlalchemy import func
import csv 
from io import StringIO

celery = Celery(
    'tasks',
    broker = 'redis://localhost:6379/0',
)

celery.conf.update(
    timezone = 'Asia/Kolkata', 
    enable_utc = False
)


@celery.task()
def generate_user_csv(user_id, email):
    with app.app_context():

        records = Reservation.query.filter_by(user_id=user_id).all()

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["Reservation ID", "Parking Lot", "Spot Number",
                         "Parked At", "Left At", "Amount"])

        for r in records:

            lot = r.spot.parking_lot.prime_location if r.spot else "N/A"
            spot = r.spot.spot_number if r.spot else "N/A"

            writer.writerow([
                r.id,
                lot,
                spot,
                r.parking_timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.parking_timestamp else "",
                r.leaving_timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.leaving_timestamp else "",
                r.total_cost if r.total_cost is not None else ""
            ])

        csv_content = output.getvalue()
        output.close()

        subject = "Your Parking CSV Export"
        body = "Hi,<br><br>Attached is the CSV export of your parking history.<br><br>Regards,<br>Vehicle Parking App Team"

        send_email(
            to_email=email,
            subject=subject,
            body=body,
            attachments=[("parking_report.csv", csv_content)]
        )

        return f"CSV export sent to {email}"


@celery.task()
def send_daily_reminder():
    with app.app_context():

        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        users_to_remind = User.query.filter(
            (User.last_visited == None) | (User.last_visited < today_start)
        ).all()

        subject = "Reminder to Check Parking App"
        body = (
            "Hi,\n\n"
            "You haven't visited the parking application today.\n"
            "If you need a parking spot, please log in and book.\n\n"
            "Regards,\n The Vehicle Parking App Team"
        ) 

        for user in users_to_remind:
            send_email(user.email, subject, body)

        return f"Sent reminders to {len(users_to_remind)} users."


def render_monthly_report_html(user, month_start, month_end, stats, reservations):
    html_rows = ""
    for r in reservations:
        lot_name = r.spot.parking_lot.prime_location if r.spot and r.spot.parking_lot else "Unknown lot"
        parked_at = r.parking_timestamp.strftime("%Y-%m-%d %H:%M")
        left_at = r.leaving_timestamp.strftime("%Y-%m-%d %H:%M") if r.leaving_timestamp else "Still parked / unknown"
        amount = r.total_cost if r.total_cost is not None else "N/A"
        html_rows += f"""
            <tr>
                <td>{r.id}</td>
                <td>{lot_name}</td>
                <td>{parked_at}</td>
                <td>{left_at}</td>
                <td>{amount}</td>
            </tr>
        """

    most_used = stats.get('most_used_lot', ('N/A', 0))
    html = f"""
    <html>
    <body>
      <h2>Monthly Parking Report — {month_start.strftime('%B %Y')}</h2>
      <p>Hi {user.full_name or user.email},</p>

      <p><strong>Total bookings:</strong> {stats.get('total_bookings', 0)}</p>
      <p><strong>Total amount spent:</strong> {stats.get('total_amount', 0)}</p>
      <p><strong>Most used parking lot:</strong> {most_used[0]} (used {most_used[1]} times)</p>

      <h3>Bookings detail</h3>
      <table border="1" cellpadding="6" cellspacing="0">
        <thead>
          <tr>
            <th>Reservation ID</th>
            <th>Parking Lot</th>
            <th>Parked At</th>
            <th>Left At</th>
            <th>Amount</th>
          </tr>
        </thead>
        <tbody>
          {html_rows if html_rows else '<tr><td colspan="5">No bookings this month.</td></tr>'}
        </tbody>
      </table>

      <p style="margin-top:20px">Regards,<br> The Vehicle Parking App Team</p>
    </body>
    </html>
    """
    return html

@celery.task()
def send_monthly_report():
    """Generates and sends monthly activity reports to all users for the previous calendar month."""
    with app.app_context():
        now = datetime.now()
        # compute previous calendar month
        first_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_month_end = first_of_this_month - timedelta(seconds=1)
        last_month_start = last_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        month_start = last_month_start
        month_end = last_month_end

        users = User.query.all()
        sent_count = 0

        for user in users:
            # fetch reservations for this user in last month
            reservations = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.parking_timestamp >= month_start,
                Reservation.parking_timestamp <= month_end
            ).order_by(Reservation.parking_timestamp).all()

            total_bookings = len(reservations)
            # total amount: use total_cost if present (assumption: total_cost is set at leaving)
            total_amount = sum((r.total_cost or 0) for r in reservations)

            # find most used parking lot for this user in last month
            most_used = db.session.query(
                ParkingLot.prime_location,
                func.count(Reservation.id).label('cnt')
            ).join(ParkingSpot, ParkingSpot.id == Reservation.spot_id) \
             .join(ParkingLot, ParkingLot.id == ParkingSpot.lot_id) \
             .filter(
                 Reservation.user_id == user.id,
                 Reservation.parking_timestamp >= month_start,
                 Reservation.parking_timestamp <= month_end
             ).group_by(ParkingLot.id).order_by(func.count(Reservation.id).desc()).first()

            most_used_lot = (most_used[0], most_used[1]) if most_used else ("N/A", 0)

            stats = {
                'total_bookings': total_bookings,
                'total_amount': total_amount,
                'most_used_lot': most_used_lot
            }

            subject = f"Your Monthly Parking Report — {month_start.strftime('%B %Y')}"
            html_body = render_monthly_report_html(user, month_start, month_end, stats, reservations)

            # send email (MailHog)
            print(f"[monthly report] sending report to {user.email} | bookings={total_bookings} amount={total_amount}")
            send_email(user.email, subject, html_body)

            sent_count += 1

        return f"Monthly reports sent to {sent_count} users."

celery.conf.beat_schedule = {
        'send-daily-reminder':{
                'task' : 'celery_app.send_daily_reminder',
                #'schedule' : crontab(hour=9, minute=0) #daily 9am
                'schedule' : timedelta(minutes=1)
                # 'schedule': 10,
        },

        'send-monthly-report':{
             'task': 'celery_app.send_monthly_report',
             'schedule': crontab(minute=0, hour=8, day_of_month='1'), 
        }
}