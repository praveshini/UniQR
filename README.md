	UNIQR

Get started
The QR Attendance System is an advanced attendance management application designed to streamline and automate the process of taking attendance. This system integrates QR code technology, face recognition, and geolocation data to ensure accurate and secure attendance tracking.Table of Contents
Features
Technologies Used
System Architecture
Usage
Database Schema
Features
QR Code Generation: Faculty generates unique QR codes for each course and class, ensuring a secure and efficient attendance process.
QR Code Scanning: Allows students to scan QR codes using their mobile devices to mark their attendance.
Face Recognition: Utilizes OpenCV to verify student identities through facial recognition, preventing proxy attendance.
Geolocation Tracking: Records the location (latitude and longitude) and timestamp of each student during attendance to verify their presence in the designated area.
Data Management: Securely stores attendance data in a PostgreSQL database.
Admin Dashboard: Provides an intuitive interface for administrators to manage courses, classes
Data Expiry: Automatically expires geolocation data after 10 minutes for privacy and security.
Technologies Used
Programming Languages: Python, HTML, CSS
Frameworks: Flask (web framework)
Database: PostgreSQL
Libraries: OpenCV (for face recognition), Geolocation APIs, QR code libraries
Other Tools: Git
System Architecture
Frontend: Built with HTML and CSS, providing a user-friendly interface for students and administrators.
Backend: Developed with Flask, handling requests, processing data, and interacting with the PostgreSQL database.
Database: PostgreSQL is used to store user data, attendance records, and geolocation data.
Face Recognition: OpenCV library is integrated for facial recognition to authenticate students.
QR Code Generation and Scanning: Libraries are used to generate and read QR codes for attendance purposes.
Geolocation Tracking: APIs are used to capture and verify the location of students during attendance.


Usage
Admin
Login: Access the admin dashboard at http://localhost:5000/admin.
Manage Classes,faculty,students: Add them
Faculty
Login:Access the faculty dashboard at  http://localhost:5000/admin.
Manage qr:Gnerates qr for particular class and share them

Student
Scan QR Code: Use the mobile app to scan the QR code displayed in the classroom.
Face Recognition: Complete the face recognition step to verify identity.
Geolocation Verification: Ensure the device location is enabled for geolocation tracking.
Database Schema
Tables
Admin: Stores user information including IDs, names, and roles (student or admin).
Course: Contains information about the courses.
Class: Details of classes associated with courses.
Student: Records of attendance including user ID, class ID, timestamp, and geolocation data.
Faculty: Contains latitude, longitude, and time fields for location data expiring after 10 minutes.
