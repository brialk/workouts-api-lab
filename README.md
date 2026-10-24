# workouts-api-lab
Workouts API

A Flask REST API for tracking workouts and the exercises done in them. Built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.

Description

This API lets you create, view, and delete workouts and exercises, and add exercises to a workout with reps, sets, and/or duration. Data is stored in a SQLite database.

Data is checked at three levels so bad data can't get in:

Level	Examples
Table constraints	Exercise names are required and unique; category must be Cardio, Strength, Flexibility, or Balance; workout duration must be greater than 0; reps, sets, and duration cannot be negative
Model validations (@validates)	Exercise name can't be blank; category must be an allowed value; workout duration must be a positive whole number; workout date must be a real date
Schema validations (Marshmallow)	Required fields; name length; category must be one of the allowed values; duration at least 1; reps/sets/duration at least 0; an exercise added to a workout needs reps and sets, or a duration
Data model
Exercise: id, name, category, equipment_needed
Workout: id, date, duration_minutes, notes
WorkoutExercise (join table): id, workout_id, exercise_id, reps, sets, duration_seconds

A workout has many exercises through WorkoutExercise, and an exercise has many workouts through WorkoutExercise. Deleting a workout or exercise also deletes its WorkoutExercise rows.

Installation

You need Python 3 and Git.

Clone the repo and move into it:
bash
   git clone https://github.com/YOUR-USERNAME/workouts-api-lab.git
   cd workouts-api-lab
Install the dependencies and activate the virtual environment. Option A: pipenv (uses the included Pipfile):
bash
   pipenv install
   pipenv shell

Option B: venv + pip (uses requirements.txt):

bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
Create and seed the database:
bash
   cd server
   export FLASK_APP=app.py
   flask db init
   flask db migrate -m 'create exercises, workouts, workout_exercises'
   flask db upgrade head
   python seed.py

If the migrations/ folder already exists in the repo, skip flask db init. You can re-run python seed.py at any time to reset the data.

Running the app

From the server/ folder, with the virtual environment active:

bash
python app.py

The API runs at http://localhost:5555. You can also use flask run -p 5555.

Try it in your browser: http://localhost:5555/workouts/1

Screenshot

Show Image

API Endpoints
Workouts
Method	Endpoint	Description
GET	/workouts	List all workouts
GET	/workouts/<id>	Show one workout with its exercises, including reps, sets, and duration
POST	/workouts	Create a workout
DELETE	/workouts/<id>	Delete a workout and its associated WorkoutExercises
Exercises
Method	Endpoint	Description
GET	/exercises	List all exercises
GET	/exercises/<id>	Show one exercise and its associated workouts
POST	/exercises	Create an exercise
DELETE	/exercises/<id>	Delete an exercise and its associated WorkoutExercises
Adding an exercise to a workout
Method	Endpoint	Description
POST	/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises	Add an exercise to a workout with reps/sets and/or duration
Response codes
Code	Meaning
200	Success
201	Created
204	Deleted (no content)
400	Invalid data (validation failed); the response lists what was wrong
404	Workout or exercise not found
Example requests

Create a workout:

bash
curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-10-23", "duration_minutes": 50, "notes": "Upper body"}'

Create an exercise:

bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Plank", "category": "Strength", "equipment_needed": false}'

Add exercise 1 to workout 2 (3 sets of 8 reps):

bash
curl -X POST http://localhost:5555/workouts/2/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 8, "sets": 3}'

Or use a duration instead of reps and sets:

bash
curl -X POST http://localhost:5555/workouts/2/exercises/3/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"duration_seconds": 60}'

Allowed exercise categories: Cardio, Strength, Flexibility, Balance.

Project structure
.
├── Pipfile
├── requirements.txt
├── README.md
├── images/
│   └── workout.png
└── server/
    ├── app.py        # Flask app and endpoints
    ├── models.py     # SQLAlchemy models, constraints, validations
    ├── schemas.py    # Marshmallow schemas and schema validations
    ├── seed.py       # Sample data
    └── migrations/   # Database migrations
Dependencies

Listed in the Pipfile and requirements.txt:

Flask
Flask-SQLAlchemy
Flask-Migrate
Marshmallow
Tests

This project has no automated test files. Endpoints and validations were checked manually with curl and the browser, using the example requests above.
## Screenshot

![GET /workouts/1 response](images/workout.png)