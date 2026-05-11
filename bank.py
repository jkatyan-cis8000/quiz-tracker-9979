"""Question bank for loading and storing questions."""

import json
from pathlib import Path
from typing import Optional

from questions import MultipleChoiceQuestion, ShortAnswerQuestion, Question


class QuestionBank:
    """Manages a collection of questions."""
    
    def __init__(self):
        self.questions: list[Question] = []
    
    def add_question(self, question: Question) -> None:
        """Add a question to the bank."""
        self.questions.append(question)
    
    def load_from_file(self, filepath: str) -> int:
        """Load questions from a JSON file. Returns count of loaded questions."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Question file not found: {filepath}")
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        loaded_count = 0
        for question_data in data.get('questions', []):
            question = self._create_question_from_data(question_data)
            if question:
                self.add_question(question)
                loaded_count += 1
        
        return loaded_count
    
    def _create_question_from_data(self, data: dict) -> Optional[Question]:
        """Create a question instance from dictionary data."""
        question_type = data.get('type', 'multiple_choice')
        
        if question_type == 'multiple_choice':
            return MultipleChoiceQuestion(
                id=data['id'],
                question_text=data['question_text'],
                options=data['options'],
                correct_option=data['correct_option'],
                points=data.get('points', 10),
                difficulty=data.get('difficulty', 'medium')
            )
        elif question_type == 'short_answer':
            return ShortAnswerQuestion(
                id=data['id'],
                question_text=data['question_text'],
                correct_answer=data['correct_answer'],
                points=data.get('points', 10),
                difficulty=data.get('difficulty', 'medium'),
                case_sensitive=data.get('case_sensitive', False)
            )
        return None
    
    def get_random(self, count: int = 1, difficulty: Optional[str] = None) -> list[Question]:
        """Get random questions, optionally filtered by difficulty."""
        import random
        
        questions = self.questions
        if difficulty:
            questions = [q for q in questions if q.get_difficulty() == difficulty]
        
        if count >= len(questions):
            return questions.copy()
        
        return random.sample(questions, count)
    
    def get_by_difficulty(self, difficulty: str) -> list[Question]:
        """Get all questions of a specific difficulty."""
        return [q for q in self.questions if q.get_difficulty() == difficulty]
    
    def get_by_type(self, question_type: str) -> list[Question]:
        """Get all questions of a specific type."""
        if question_type == 'multiple_choice':
            return [q for q in self.questions if isinstance(q, MultipleChoiceQuestion)]
        elif question_type == 'short_answer':
            return [q for q in self.questions if isinstance(q, ShortAnswerQuestion)]
        return []
    
    def size(self) -> int:
        """Return the total number of questions."""
        return len(self.questions)
    
    def get_all(self) -> list[Question]:
        """Return all questions."""
        return self.questions.copy()
