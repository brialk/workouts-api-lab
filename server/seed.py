#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    squat = Exercise(name='Squat', category='Strength', equipment_needed=True)
    run = Exercise(name='Running', category='Cardio', equipment_needed=False)
    stretch = Exercise(name='Hamstring Stretch', category='Flexibility', equipment_needed=False)
    db.session.add_all([squat, run, stretch])

    w1 = Workout(date=date(2026, 10, 19), duration_minutes=45, notes='Leg day')
    w2 = Workout(date=date(2026, 10, 21), duration_minutes=30, notes='Easy cardio')
    db.session.add_all([w1, w2])
    db.session.commit()

    db.session.add_all([
        WorkoutExercise(workout=w1, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=w1, exercise=stretch, duration_seconds=60),
        WorkoutExercise(workout=w2, exercise=run, duration_seconds=1200),
    ])
    db.session.commit()
    print('Seeded!')