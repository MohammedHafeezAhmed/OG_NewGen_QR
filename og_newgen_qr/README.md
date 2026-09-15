# OG_NewGen_QR
NewGen_QR : A streamlined, session-based QR attendance platform engineered to facilitate secure, real-time attendance capture through seamless QR-driven verification.

The system enables an administrator or teacher to create an attendance session, generate a unique QR-enabled link, share it with students, and monitor attendance in real time — all through a single web application.

## ✨ Key Highlights

* 🔐 **Session-Based Attendance** — Every attendance session generates a unique session ID.
* ⏱️ **Time-Bound Sessions** — Attendance sessions automatically expire after 10 minutes.
* 📱 **Mobile QR Scanning** — Students can scan their college ID QR codes directly using their phone camera.
* ⚡ **Real-Time Attendance Tracking** — The admin dashboard continuously updates attendance data.
* 🚫 **Duplicate Prevention** — A student cannot register the same USN twice within a session.
* 📲 **WhatsApp Sharing** — Attendance links can be shared directly with a WhatsApp group.
* 📊 **Live Attendance Dashboard** — Attendance is displayed dynamically as students check in.
* 🌐 **Single Web Application** — Admin and student interfaces are served through the same Flask application.
* ☁️ **Deployment Ready** — Structured for deployment as a Python web service.

## 🧩 How It Works

```text
Admin
  │
  │ Creates Attendance Session
  ▼
Flask Backend
  │
  │ Generates unique session
  ▼
Attendance Link
  │
  ├── Shared with Students
  │
  ▼
Student Phone
  │
  │ Scans College ID QR
  ▼
Flask API
  │
  │ Validates session + USN
  ▼
Attendance Recorded
  │
  ▼
Live Admin Dashboard
```

## 🚀 Core Features

### Admin Dashboard

The administrator can:

* Create and manage teacher/subject presets
* Enter the subject name
* Enter the teacher's WhatsApp number
* Generate a unique attendance session
* Generate a time-limited attendance link
* Share the session through WhatsApp
* Monitor students joining the session
* View live attendance
* Send attendance information to the teacher

### Student Attendance

Students can:

1. Open the attendance link.
2. Allow camera access.
3. Scan their college ID QR code.
4. Submit their USN.
5. Receive confirmation once attendance is recorded.

The system prevents duplicate attendance submissions for the same USN during a session.

## 🛠️ Technology Stack

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| **Python**       | Backend development                   |
| **Flask**        | Web framework and REST APIs           |
| **HTML5**        | Application structure                 |
| **CSS3**         | User interface styling                |
| **JavaScript**   | Client-side functionality             |
| **html5-qrcode** | QR code scanning                      |
| **Gunicorn**     | Production WSGI server                |
| **Git & GitHub** | Version control and source management |

## 📁 Project Structure

```text
QR-Attendance-System/
│
├── app.py
├── requirements.txt
│
└── templates/
    ├── admin.html
    └── scan.html
```


## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000/admin
```

## 🌐 Deployment

The application can be deployed as a Python web service on platforms that support Flask applications.

For production deployment with Gunicorn:

```bash
gunicorn app:app
```

The application is designed so that both the administrator dashboard and student attendance interface operate through the same web application.

## 🔒 Attendance Validation

Each attendance session contains:

* A unique session identifier
* A creation timestamp
* An expiration timestamp
* A collection of recorded student USNs

When a student submits attendance, the backend validates the active session before recording the attendance.

This ensures that an expired attendance session cannot continue accepting submissions.

## 📈 Future Enhancements

Potential improvements include:

* Persistent database storage
* Student authentication
* Teacher authentication
* Attendance history and analytics
* Export attendance as CSV/Excel
* Role-based access control
* PostgreSQL integration
* Automated attendance reports
* Cloud-based session persistence
* Anti-proxy/anti-sharing verification
* Geolocation-based classroom validation

## 🎯 Project Objective

The project aims to replace manual attendance workflows with a lightweight, mobile-first system that makes attendance **faster, easier to monitor, and less prone to duplicate entries**.

It demonstrates practical implementation of:

* REST API development
* Backend session management
* QR-based verification
* Real-time frontend/backend communication
* Client-side browser APIs
* Flask routing
* Deployment-oriented application structure

## 👨‍💻 Author

**Hafeez Ahmed**

B.Tech — Computer Science & Engineering

---

⭐ If you find this project useful, consider giving the repository a star.
