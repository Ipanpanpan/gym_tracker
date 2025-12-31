import sqlite3
from typing import List, Tuple, Optional
from datetime import datetime
from models import ExerciseMetadata, ExerciseSet, Unit

DB_NAME = "gym_data.db"

class Database:
    def __init__(self, db_path: str = DB_NAME):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Exercises Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    is_assisted BOOLEAN NOT NULL DEFAULT 0,
                    description TEXT
                )
            ''')
            # Sets Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_id INTEGER NOT NULL,
                    weight REAL NOT NULL,
                    unit TEXT NOT NULL,
                    reps INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (exercise_id) REFERENCES exercises (id)
                )
            ''')
            
            # Seed default exercises if empty
            cursor.execute("SELECT count(*) FROM exercises")
            if cursor.fetchone()[0] == 0:
                self.seed_defaults()

    def seed_defaults(self):
        """Pre-populate with the examples."""
        self.add_exercise("Bench Press", is_assisted=False)
        self.add_exercise("Assisted Pull-up", is_assisted=True)
        self.add_exercise("Squat", is_assisted=False)
        self.add_exercise("Assisted Dip", is_assisted=True)

    def add_exercise(self, name: str, is_assisted: bool, description: str = "") -> int:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO exercises (name, is_assisted, description) VALUES (?, ?, ?)",
                    (name, is_assisted, description)
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Already exists
            return -1

    def get_exercises(self) -> List[Tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, is_assisted, description FROM exercises")
            return cursor.fetchall()

    def get_exercise_by_id(self, exercise_id: int) -> Optional[ExerciseMetadata]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, is_assisted, description FROM exercises WHERE id = ?", (exercise_id,))
            row = cursor.fetchone()
            if row:
                return ExerciseMetadata(name=row[0], is_assisted=bool(row[1]), description=row[2])
            return None

    def add_set(self, exercise_id: int, weight: float, unit: Unit, reps: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sets (exercise_id, weight, unit, reps) VALUES (?, ?, ?, ?)",
                (exercise_id, weight, unit.value, reps)
            )

    def get_history(self, exercise_id: int) -> List[Tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, weight, unit, reps, timestamp 
                FROM sets 
                WHERE exercise_id = ? 
                ORDER BY timestamp DESC
            ''', (exercise_id,))
            return cursor.fetchall()
