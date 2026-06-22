from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class SetLog(BaseModel):
    reps: int
    weight_kg: float
    rpe: Optional[float] = None
    completed: bool

class ExerciseLog(BaseModel):
    exercise_id: UUID
    sets: List[SetLog]

class WorkoutLog(BaseModel):
    user_id: UUID
    name: str
    exercises: List[ExerciseLog]
