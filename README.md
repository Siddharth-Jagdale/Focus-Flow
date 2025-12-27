📌 FocusFlow – Digital Notes & Task Organizer

FocusFlow is a Python-based desktop GUI application built using Tkinter and SQLite, designed to help users efficiently manage notes and tasks in one place.
The application focuses on simplicity, productivity, and clean UI, inspired by modern productivity tools.

🚀 Features
🔐 Authentication

Login with username and password

Signup for new users

User-specific data handling

📊 Dashboard

Central navigation hub

Displays total number of notes and tasks

Profile icon with popup menu

Logout and theme toggle options

📝 Notes Management

Add notes with title, category, and content

View notes in a table format

Delete notes

Notes stored securely in SQLite database

✅ Task Management

Add tasks with priority and due date

Mark tasks as completed

Delete tasks

Filter tasks by priority (Low / Medium / High)

View tasks in a table format

🎨 UI Enhancements

Light / Dark mode support

Profile popup with fade-in animation

Full-screen responsive layout

📤 Export

Export notes to CSV

Export tasks to CSV

🛠️ Technologies Used
________________________________________________________
| Technology	      |          Purpose                |  
| Python	          |      Core programming language  | 
| Tkinter	          |       GUI development           |
| SQLite	          |       Database                  | 
| VS Code	          |       Development environment   |
|___________________|_________________________________|

📁 Project Folder Structure
FocusFlow/
│
├── login.py          # Login screen & authentication
├── signup.py         # User registration
├── dashboard.py      # Main dashboard
├── notes.py          # Notes management
├── tasks.py          # Task management
├── theme.py          # Light/Dark theme logic
├── ui_helper.py      # Theme application helpers
├── exporter.py       # CSV export functionality
├── app.db            # SQLite database
├── README.md         # Project documentation

🗄️ Database Schema
Users Table:

__________________________________________________
| Column	        |          Type                |  
| id	            |      INTEGER (Primary Key)   | 
| username	      |       TEXT                   |
| password	      |       TEXT                   | 
|_________________|______________________________|


Notes Table:
__________________________________________________
| Column	        |          Type                |  
| id	            |       INTEGER                | 
| user_id	        |       INTEGER                |
| title	          |       TEXT                   | 
| content         |       TEXT                   |
| category        |       TEXT                   | 
| created_at      |       TEXT                   |
|_________________|______________________________|

Tasks Table:
__________________________________________________
| Column	        |          Type                |  
| id	            |       INTEGER                | 
| user_id	        |       INTEGER                |
| title	          |       TEXT                   | 
| priority        |       TEXT                   |
| status          |       TEXT                   | 
| due_date        |       TEXT                   |
|_________________|______________________________|

⚙️ How to Run the Project
1️⃣ Clone the Repository

git clone <repository-url>
cd FocusFlow

2️⃣ Ensure Python is Installed

python --version
(Recommended: Python 3.9+)

3️⃣ Run the Application

python login.py


🎯 Application Flow

User launches the application

Login or Signup screen appears

After login → Dashboard opens

User can:

Manage notes

Manage tasks

Toggle theme

Export data

Logout returns user to login screen


🔮 Future Enhancements

Password encryption (hashing)

Task reminders and notifications

Analytics dashboard (charts)

Search functionality

Cloud database integration

Advanced UI animations


🧑‍💻 Author

Developed by:
Siddharth Jagdale


📜 License

This project is developed for academic and learning purposes.

⭐ Final Note

FocusFlow demonstrates the practical use of Python GUI programming with database integration, focusing on clean design, modular code structure, and real-world usability.
