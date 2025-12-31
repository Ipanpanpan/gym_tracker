from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class Unit(Enum):
    KG = "kg"
    LBS = "lbs"

    def to_kg(self, value: float) -> float:
        if self == Unit.KG:
            return value
        return value * 0.453592

@dataclass
class ExerciseMetadata:
    name: str
    is_assisted: bool = False
    description: Optional[str] = None

@dataclass
class ExerciseSet:
    exercise: ExerciseMetadata
    weight: float
    unit: Unit
    reps: int

    @property
    def normalized_kg(self) -> float:
        return self.unit.to_kg(self.weight)

    def is_better_than(self, other: 'ExerciseSet') -> bool:
        """
        Returns True if this set represents a better performance than the other set.
        Assumes comparing sets of the same exercise.
        """
        if self.exercise.name != other.exercise.name:
            raise ValueError("Cannot compare sets of different exercises")
        
        # Priority 1: Weight (Intensity)
        my_weight = self.normalized_kg
        other_weight = other.normalized_kg
        
        weight_better = False
        
        if self.exercise.is_assisted:
            # For assisted, Lower weight is better (less help needed)
            if my_weight < other_weight:
                weight_better = True
            elif my_weight > other_weight:
                weight_better = False
            else:
                # Weights equal, check reps
                return self.reps > other.reps
        else:
            # Standard, Higher weight is better
            if my_weight > other_weight:
                weight_better = True
            elif my_weight < other_weight:
                weight_better = False
            else:
                # Weights equal, check reps
                return self.reps > other.reps
                
        return weight_better

    def __str__(self):
        return f"{self.exercise.name}: {self.weight} {self.unit.value} x {self.reps} reps ({'Assisted' if self.exercise.is_assisted else 'Standard'})"
