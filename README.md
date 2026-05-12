# Vehicle Parking App (VP-MAD-2)

A Modern Application Development II (MAD-II) project for managing parking lots, spots, and user reservations with role-based authentication, background tasks, email automation, and admin management dashboards.

---

## Project Overview

The **Vehicle Parking App** is a web-based solution that enables:
- **Users** 
- Register and login through token-based authentication

- View available parking lots and spot statuses

- Reserve & cancel parking spots

- Track active reservation duration

- View past reservation history through summaries

- Download past reservations history as CSV file

- **Admins** 
- Create & manage parking lots

- Auto-generate spots based on capacity

- View all users & reservations

- Identify which user is occupying which spot

- Monitor system activity through admin dashboards

- Sends Daily Reminders

- Sends Monthly Reports to the Users

---

## 🗃️ Database Models & Relationships

- **User**: Stores registration details (name, email, phone number, password).
- **Role**: Defines roles like `User`, `Admin`.
- **UserRole**: Mapping between users and their roles (many-to-many).
- **ParkingLot**: Information about each parking location.
- **ParkingSpot**: Individual parking spots linked to a lot.
- **Reservation**: Tracks user bookings, timestamps, and cost.

Relationships:
- Users ↔ Roles (Many-to-Many)
- ParkingLot ↔ ParkingSpots (One-to-Many)
- User ↔ Reservations (One-to-Many)
- ParkingSpot ↔ Reservations (One-to-Many)

---

## Key Features

- **Admin Dashboard:** Manage parking lots, spots, and view user activity.
- **User Dashboard:** Book parking spots and view reservation history.
- **Authentication and Role Management:** Secure login for admin and user.
- **Summary Charts:** Visualize parking spot usage(user side), reservation and income stats(admin side).
- **Responsive UI:** Built via CSS

---

## Technologies Used 
- **Frontend**

- Vue 3: Modern JavaScript framework for building user interfaces.

- Pinia: State management for handling authentication state, user data & UI state.

- Vue Router: Client-side routing for navigation and protected routes.

- HTML5 & CSS3: Core structure and styling for responsive UI.

- Implemented vue Components to reduce redundancy

- **Backend**

- Flask: Python backend framework for building RESTful APIs.

- Flask-SQLAlchemy: ORM layer for managing the SQLite database.

- Flask-Security Token-based authentication and role management.

- Flask-CORS: Enables secure communication between Vue frontend and Flask backend.

- SQLite: Lightweight relational database storing users, lots, spots, and reservations.

- **Backend Jobs**

- Celery: Handles asynchronous tasks such as email sending and scheduled jobs.

- Redis: Message broker for Celery workers and Celery Beat scheduler.

## Milestones

1. **Database Models and Schema setup**
- Designed database models for User, Role, ParkingLot, ParkingSpot, and Reservation.
- Implemented relationships between users, lots, spots, and reservations.
- Built a full set of REST APIs for authentication, lot/spot management, and reservation handling.
- Added token-based authentication endpoints using Flask-Security.

2. **Authenticatiom and Role Management**
- Implemented token-based registration and login (no sessions).
- Stored token + role using Pinia and browser storage.
- Applied role-based access control for user/admin routes in both frontend and backend.
- Auto-restored login state even after browser refresh.

3. **Admin Dashboard and Lot/Spot Management**
- Built Vue-based admin dashboard to:
    - Create parking lots
    - Auto-generate parking spots based on capacity
    - Update/edit lots
    - View all users and their active reservations
- Auto-generated parking spots based on lot capacity.
- Admin can view spot statuses and all registered users with their active spot.
- Added CSV export feature for reservation data.  

4. **User Dashboard and Reservation System**
- Users can view available lots and auto-reserve the first available spot.
- Tracked `parking_timestamp` on occupation and `leaving_timestamp` on release.
- Users can view their parking history and reservation status.

5. **Reservation History and Summary**
- Calculated and displayed parking duration.
- Maintained reservation history per user. 
- CSV download option to view past reservations

6. **Slot Time Calculation and Parking Cost**
- Calculated total cost based on parking time and lot’s price per unit.
- Displayed cost summary in both user (via tables) and admin (via summary) views.

7. **Background Jobs & Email Automation**
- Integrated Celery to send emails asynchronously.
- Added Celery Beat for scheduled tasks.

8. **Frontend and Backend Validation**
- Added HTML5-based frontend validations (e.g., required fields, email format).
- Backend validations for duplicate users, empty fields, and invalid states.

9. **Responsive UI and Styling**
- Styled the app using clean custom CSS.
- Ensured responsiveness across mobile, tablet, and desktop devices.
- Added modals, navigation guards, and dynamic role-based UI behavior.

## Optional Enhancements Implemented
7. **Charts and Visualization**
- Integrated Matplotlib for generating server-side graphs.
- Visualizations include total revenue, parking activity and lot utilization stats.

## Installation & Setup

### Backend Setup (Flask)

- Clone the repository

```bash
git clone https://github.com/sheengauhar/vehicle-parking-app-v2
```

- Navigate to backend folder

```bash
cd backend
```

- Install backend dependencies

```bash
pip install -r requirements.txt
```

- Run Flask server

```bash
py-3.13 app.py
```

Backend runs on:
`http://localhost:5000`

---

### Frontend Setup (Vue)

- Navigate to frontend folder

```bash
cd frontend
```

- Install frontend dependencies

```bash
npm install
```

- Start Vue development server

```bash
npm run dev
```

Frontend runs on:
`http://localhost:5173`

---

### Redis Setup

Start Redis server:

```bash
redis-server
```

---

### Celery Worker

Navigate to backend folder:

```bash
cd backend
```

Run Celery worker:

```bash
celery -A celery_app.celery worker --loglevel=info --pool=solo
```

It handles background tasks such as:
- generating user's parking history CSV
- sending daily reminders
- sending monthly reports

---

### Celery Beat Scheduler

Run scheduled reminder tasks:

```bash
celery -A celery_app.celery beat --loglevel=info
```





## Folder Structure
VEHICLE-PARKING-APP-V2/
│
├── backend/
│   ├── controllers/
│   │   ├── authentication.py
│   │   ├── config.py
│   │   ├── create_database_instance.py
│   │   ├── crud_api.py
│   │   ├── database.py
│   │   └── models.py
|   |   |_ user_datastore.py
│   │   
│   ├── instance/
│   │   └── project2.sqlite
│   │
│   ├── app.py
│   ├── cache_instance.py
│   ├── celery_app.py
│   ├── mail.py
│   ├── package.json
│   ├── package-lock.json
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── icons/
│   │   │   ├── ParkingLotCard.vue
│   │   │   └── ParkingSpots.vue
│   │   │
│   │   ├── router/
│   │   │   └── index.js
│   │   │
│   │   ├── stores/
│   │   │   ├── authStore.js
│   │   │   ├── counter.js
│   │   │   └── parkingLotStore.js
│   │   │
│   │   ├── views/
│   │   │   ├── AddParkingLot.vue
│   │   │   ├── AdminDashboard.vue
│   │   │   ├── AdminSummary.vue
│   │   │   ├── AdminUsers.vue
│   │   │   ├── BookSpots.vue
│   │   │   ├── ConfirmBooking.vue
│   │   │   ├── EditParkingLot.vue
│   │   │   ├── EditProfile.vue
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── UserDashboard.vue
│   │   │   └── UserSummary.vue
│   │   │
│   │   ├── App.vue
│   │   └── main.js
│   │
│   ├── index.html
│   ├── jsconfig.json
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
