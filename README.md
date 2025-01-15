# Metamorphosis Tracker
A personal growth tool where users set a goal, track their progress, and visually see their transformation in the form of butterfly badges earned.

This application is built using Flask, SQLAlchemy, and SQLite, and it provides a user-friendly interface for managing personal development journeys.

## Features

- User Registration and Authentication
- Goal Creation and Management
- Progress Tracking


## Project Structure
metamorphosis_tracker/ 
├── pycache/ 
├── app.py 
├── database.py 
├── instance/ 
    ├── models.py 
├── README.md 
├── requirements.txt 
├── static/ 
├── templates/ │ 
             ├── create-new-goals.html 
             ├── dashboard.html  
             ├── goal_details.html 
             ├── index.html  
             ├── login.html 
             ├── register.html 
             ├── start-journey-form.html
             ├── tasks.html 
    

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/codeDragon35/metamorphosis_tracker.git
    cd metamorphosis_tracker
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    export FLASK_APP=app.py
    flask run
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Register a new account or log in with an existing account.

4. Create new goals, track your progress, and visualize your transformation journey.

## Configuration

You can configure the application settings in a separate configuration file. Create a `config.py` file and add the following content:

```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///metamorphosis_tracker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


Then, update app.py to use the configuration file:
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

```

## Acknowledgements
- GitHub Copilot (GPT 4o)
- ChatGPT
- Dev.to (GitHub Copilot 1-Day Build Challenge)
- Flask
- SQLAlchemy
- Bootstrap

## Future Scope
- Features like notification reminders
- add more animations to more visually interpret the goal journey