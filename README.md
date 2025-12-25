# Sidequest

Sidequest is a Flask-based event finder web application where users can create, promote, and discover events through both a list-based interface and an interactive map. The platform supports user accounts, event categorization, search and filtering, and is designed to be fully responsive and user-friendly across devices.

---

## 🚀 Features

- User authentication and accounts
- Event creation and promotion by registered users
- Interactive map using **OpenStreetMap** and **Leaflet**
- Search and filtering by:
  - Address or city
  - Event category (e.g. music, arts & crafts, sports)
  - Keywords in event titles
- Toggle between:
  - Paginated list view
  - Map-based view
- Form validation and feedback messages using **WTForms**
- Responsive design for mobile and desktop use
- Clean and intuitive user experience

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Migrations:** Alembic / Flask-Migrate
- **Forms:** WTForms
- **Maps:** OpenStreetMap + Leaflet.js

---

## 📂 Project Structure (simplified)

event-finder/
│
├── event_finder/ # Flask application package
│ ├── routes.py
│ ├── models.py
│ ├── forms.py
│ ├── templates/
│ └── static/
│
├── migrations/ # Alembic migrations
├── requirements.txt
├── wsgi.py
└── README.md


---

## ⚙️ Setup & Installation

### 1. Clone the repository
(bash)
git clone https://github.com/wawayaga/event-finder
cd sidequest

2. Create and activate a virtual environment
python -m venv env
source env/bin/activate  # Linux / macOS

3. Install dependencies
pip install -r requirements.txt

4. Environment variables

Create a .env file in the project root:

SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///site.db


⚠️ Do not commit .env files to version control.

5. Initialize the database
flask db upgrade

6. Run the application
flask run


The app will be available at:

http://127.0.0.1:8080
