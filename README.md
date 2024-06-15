# Poetry Web Application

## Live Website

The website is deployed at: [https://brittaniwrotethis.pythonanywhere.com/](https://brittaniwrotethis.pythonanywhere.com/)

## Description

This is a web application designed for managing poetry, artwork, and subscriber interactions. Administrators have the 
capability to create, update, and delete poems and artwork. They can also customize their bio page and view subscriber 
analytics, including count and email addresses. Users, on the other hand, can explore the admin's biography, poems, and 
artwork. They can also subscribe for updates or unsubscribe, as well as directly contact the admin.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/katikimble/britt_webpage.git
    cd britt_webpage
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables by creating a `.env` file and adding the following:
    ```
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///site.db
    MAIL_SERVER=smtp.example.com
    MAIL_PORT=587
    MAIL_USE_TLS=true
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    ADMIN_USERNAME=admin
    ADMIN_EMAIL=admin@example.com
    ADMIN_PASSWORD=adminpassword
    ```

### Database Setup

You have two options for setting up the database: using Flask-Migrate for migrations or running custom scripts directly.

#### Using Flask-Migrate

1. **Initialize Migration Repository:**

    ```sh
    flask db init
    ```

2. **Generate Initial Migration:**

    ```sh
    flask db migrate -m "Initial migration."
    ```

3. **Apply Initial Migration:**

    ```sh
    flask db upgrade
    ```

4. **Create Initial Admin User:**

    ```sh
    python create_admin.py
    ```

#### Using Custom Scripts

1. **Create Database Tables:**

    ```sh
    python create_database.py
    ```

2.  **Clear Database (when needed):**

    ```sh
    python clear_database.py
    ```

## Usage

1. Run the application:
    ```sh
    flask run
    ```
   Or, if using the script:

    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.


## Folder Structure
```
britt_webpage/
├── poetry_app/
│   ├── __init__.py
│   ├── models.py
│   ├── about/
│   │   ├── static/
│   │   │   ├── pictures/
│   │   │   └── styles/
│   │   ├── templates/
│   │   │   └── about/
│   │   └── views.py
│   ├── admin/
│   │   ├── static/
│   │   │   └── styles/
│   │   ├── templates/
│   │   │   └── admin/
│   │   ├── forms.py
│   │   └── views.py
│   ├── art/
│   │   ├── static/
│   │   │   └── styles/
│   │   ├── templates/
│   │   │   └── art/
│   │   ├── forms.py
│   │   └── views.py
│   ├── contact/
│   │   ├── static/
│   │   │   ├── pictures/
│   │   │   └── styles/
│   │   ├── templates/
│   │   │   └── contact/
│   │   ├── forms.py
│   │   └── views.py
│   ├── main/
│   │   ├── templates/
│   │   │   └── main/
│   │   └── views.py
│   ├── poems/
│   │   ├── static/
│   │   │   └── styles/
│   │   ├── templates/
│   │   │   └── poems/
│   │   └── views.py
│   ├── subscribe/
│   │   ├── static/
│   │   │   └── styles/
│   │   ├── templates/
│   │   │   └── subcribe/
│   │   ├── forms.py
│   │   └── views.py
│   ├── static/
│   │   ├── pictures/
│   │   ├── styles/
│   │   └── uploads/
│   └── templates/
├── migrations/
├── create_database.py
├── create_admin.py
├── clear_database.py
├── app.py
├── .env
├── requirements.txt
└── README.md
```