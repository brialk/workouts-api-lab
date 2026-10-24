from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


def not_found(name):
    return {'error': f'{name} not found'}, 404

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return WorkoutSchema(many=True, exclude=('workout_exercises',)).dump(workouts), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return not_found('Workout')
    return WorkoutSchema().dump(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = WorkoutSchema(exclude=('workout_exercises',)).load(request.get_json() or {})
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except ValueError as e:
        db.session.rollback()
        return {'errors': str(e)}, 400
    except IntegrityError:
        db.session.rollback()
        return {'errors': 'That breaks a database rule (for example, a duplicate name).'}, 400
    return WorkoutSchema(exclude=('workout_exercises',)).dump(workout), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return not_found('Workout')
    db.session.delete(workout)
    db.session.commit()
    return {}, 204

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return ExerciseSchema(many=True, exclude=('workout_exercises',)).dump(exercises), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return not_found('Exercise')
    return ExerciseSchema().dump(exercise), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = ExerciseSchema(exclude=('workout_exercises',)).load(request.get_json() or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except ValueError as e:
        db.session.rollback()
        return {'errors': str(e)}, 400
    except IntegrityError:
        db.session.rollback()
        return {'errors': 'That breaks a database rule (for example, a duplicate name).'}, 400
    return ExerciseSchema(exclude=('workout_exercises',)).dump(exercise), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return not_found('Exercise')
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout:
        return not_found('Workout')
    if not exercise:
        return not_found('Exercise')
    try:
        data = WorkoutExerciseSchema().load(request.get_json() or {})
        we = WorkoutExercise(workout=workout, exercise=exercise, **data)
        db.session.add(we)
        db.session.commit()
    except ValidationError as e:
        return {'errors': e.messages}, 400
    except ValueError as e:
        db.session.rollback()
        return {'errors': str(e)}, 400
    except IntegrityError:
        db.session.rollback()
        return {'errors': 'That breaks a database rule (for example, a duplicate name).'}, 400
    return WorkoutExerciseSchema().dump(we), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)