from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from models import CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.List(
        fields.Nested('WorkoutExerciseSchema', exclude=('exercise',)),
        dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(load_default=None, allow_none=True)

    workout_exercises = fields.List(
        fields.Nested('WorkoutExerciseSchema', exclude=('workout',)),
        dump_only=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(load_default=None, allow_none=True, validate=validate.Range(min=0))
    sets = fields.Int(load_default=None, allow_none=True, validate=validate.Range(min=0))
    duration_seconds = fields.Int(load_default=None, allow_none=True,
                                  validate=validate.Range(min=0))

    workout = fields.Nested('WorkoutSchema', exclude=('workout_exercises',), dump_only=True)
    exercise = fields.Nested('ExerciseSchema', exclude=('workout_exercises',), dump_only=True)

    @validates_schema
    def check_effort(self, data, **kwargs):
        has_reps_sets = data.get('reps') is not None and data.get('sets') is not None
        has_duration = data.get('duration_seconds') is not None
        if not (has_reps_sets or has_duration):
            raise ValidationError('Provide reps and sets, or duration_seconds.')