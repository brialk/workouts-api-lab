from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

db = SQLAlchemy()

CATEGORIES = ('Cardio', 'Strength', 'Flexibility', 'Balance')

class Exercise(db.Model):
    __tablename__ = 'exercises'

    __table_args__ = (
        db.CheckConstraint(
            "category IN ('Cardio', 'Strength', 'Flexibility', 'Balance')",
            name='ck_exercises_category'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise must have a name.')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if value not in CATEGORIES:
            raise ValueError(f'Category must be one of: {", ".join(CATEGORIES)}.')
        return value

class Workout(db.Model):
    __tablename__ = 'workouts'

    __table_args__ = (
        db.CheckConstraint('duration_minutes > 0', name='ck_workouts_duration'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout',
        cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('Duration must be a positive whole number of minutes.')
        return value

    @validates('date')
    def validate_date(self, key, value):
        if not isinstance(value, date):
            raise ValueError('Date must be a real date.')
        return value

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    __table_args__ = (
        db.CheckConstraint('reps >= 0', name='ck_we_reps'),
        db.CheckConstraint('sets >= 0', name='ck_we_sets'),
        db.CheckConstraint('duration_seconds >= 0', name='ck_we_duration'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_counts(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f'{key} cannot be negative.')
        return value

