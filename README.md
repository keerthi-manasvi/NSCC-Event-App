#  NSCC Event Attendance & Registration System

**NSCC Event Attendance & Registration System** is a web-based platform designed to streamline event registration and attendance tracking using QR codes. It enables participants to register for events and check in via QR scanning, while providing organizers with real-time attendance monitoring and export capabilities.

---

##  Project Description

This system allows users to register for events by submitting their name, email, and a unique registration ID. Upon registration, each participant receives a unique QR code. At the event, organizers can scan these QR codes to mark attendance, which is timestamped and stored securely. The admin dashboard provides live tracking and an option to export attendance data to Excel.

---

##  Features

### Core Functionality

- **Participant Registration**  
  Users can register by providing their name, email, and registration ID.

- **QR Code Generation**  
  Each registrant receives a unique QR code for attendance verification.

- **QR Code Scanner**  
  Web/mobile-compatible scanner to mark attendance on-site.

- **Attendance Tracking**  
  Attendance is recorded with timestamps and duplicate prevention.

### Enhanced Capabilities

- **Excel Export**  
  Attendance data includes: Name, Email, ID, Status, Timestamp.

- **Sample Data**  
  Preloaded sample registrations and attendance records for testing.

- **Brownie Subtask: Admin Dashboard Enhancements**  
  Includes live attendance tracking and a one-click download option for Excel reports.

- **Admin Authentication System**  
  Admins can securely log in, log out, and sign up to access the dashboard.

- **Attendance Management Tools**  
  Admins can clear/reset attendance records when needed for new events.

---

##  Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap  
- **Backend**: Python + Django  
- **Database**: SQLite (default Django DB)  
- **QR Code Generation**: qrcode (Python library)  
- **QR Code Scanning**: html5-qrcode (JavaScript library)  
- **Excel Export**: openpyxl (via Django view)  
- **Deployment**: Render  

---

##  Setup Instructions

To run the project locally:

```bash
git clone https://github.com/keerthi-manasvi/NSCC-Event-App.git
cd NSCC-Event-App
npm install

---
## Live Deployment
You can access the deployed version of the app https://nscc1-event-app.onrender.com/
