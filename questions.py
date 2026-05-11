"""Question classes for the quiz tracker."""

from abc import ABC, abstractmethod
from typing import Optional
import json
import random


class Question(ABC):
    """Abstract base class for all question types."""
    
    def __init__(self, id: str, question_text: str, points: int, difficulty: str):
        self.id = id
        self.question_text = question_text
        self.points = points
        self.difficulty = difficulty
    
    @abstractmethod
    def display(self) -> str:
        """Return the question text for display."""
        pass
    
    @abstractmethod
    def check_answer(self, user_answer: str) -> bool:
        """Check if the user's answer is correct."""
        pass
    
    @abstractmethod
    def get_correct_answer(self) -> str:
        """Return the correct answer."""
        pass
    
    def get_points(self) -> int:
        """Return the points for this question."""
        return self.points
    
    def get_difficulty(self) -> str:
        """Return the difficulty level."""
        return self.difficulty


class MultipleChoiceQuestion(Question):
    """Multiple choice question with options."""
    
    def __init__(
        self,
        id: str,
        question_text: str,
        options: list[str],
        correct_option: int,
        points: int = 10,
        difficulty: str = "medium"
    ):
        super().__init__(id, question_text, points, difficulty)
        self.options = options
        self.correct_option = correct_option
    
    def display(self) -> str:
        """Display question with numbered options."""
        result = f"Q: {self.question_text}\n"
        for i, option in enumerate(self.options):
            result += f"  {i + 1}. {option}\n"
        return result
    
    def check_answer(self, user_answer: str) -> bool:
        """Check answer by option number (1-indexed)."""
        try:
            answer_num = int(user_answer.strip())
            return answer_num == self.correct_option + 1
        except ValueError:
            return False
    
    def get_correct_answer(self) -> str:
        """Return the correct option text."""
        return self.options[self.correct_option]


class ShortAnswerQuestion(Question):
    """Short answer question requiring text response."""
    
    def __init__(
        self,
        id: str,
        question_text: str,
        correct_answer: str,
        points: int = 10,
        difficulty: str = "medium",
        case_sensitive: bool = False
    ):
        super().__init__(id, question_text, points, difficulty)
        self.correct_answer = correct_answer
        self.case_sensitive = case_sensitive
    
    def display(self) -> str:
        """Display question text only."""
        return f"Q: {self.question_text}\n"
    
    def check_answer(self, user_answer: str) -> bool:
        """Check answer by comparing text."""
        if self.case_sensitive:
            return user_answer.strip() == self.correct_answer
        return user_answer.strip().lower() == self.correct_answer.lower()
    
    def get_correct_answer(self) -> str:
        """Return the correct answer."""
        return self.correct_answer


class QuestionBank:
    """Collection of questions with loading and filtering capabilities."""
    
    def __init__(self):
        self.questions: List[Question] = []
    
    def load_from_file(self, filepath: str) -> None:
        """Load questions from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for q in data:
            if q.get('type') == 'multiple_choice':
                question = MultipleChoiceQuestion(
                    id=q['id'],
                    question_text=q['question_text'],
                    options=q['options'],
                    correct_option=q['correct_option'],
                    points=q.get('points', 10),
                    difficulty=q.get('difficulty', 'medium')
                )
            elif q.get('type') == 'short_answer':
                question = ShortAnswerQuestion(
                    id=q['id'],
                    question_text=q['question_text'],
                    correct_answer=q['correct_answer'],
                    points=q.get('points', 10),
                    difficulty=q.get('difficulty', 'medium'),
                    case_sensitive=q.get('case_sensitive', False)
                )
            else:
                continue
            self.questions.append(question)
    
    def get_random(self, difficulty: Optional[str] = None, count: int = 1) -> List[Question]:
        """Select random questions, optionally filtered by difficulty."""
        import random
        
        filtered = self.questions
        if difficulty:
            filtered = [q for q in filtered if q.get_difficulty() == difficulty]
        
        if count >= len(filtered):
            return filtered
        
        return random.sample(filtered, count)
    
    def get_by_difficulty(self, difficulty: str) -> List[Question]:
        """Get all questions matching a difficulty level."""
        return [q for q in self.questions if q.get_difficulty() == difficulty]
    
    def size(self) -> int:
        """Return total number of questions."""
        return len(self.questions)


class QuestionBank:
    """Manages a collection of questions."""
    
    def __init__(self):
        self.questions: list[Question] = []
    
    def load_from_file(self, filepath: str) -> None:
        """Load questions from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        for q_data in data:
            if 'options' in q_data:
                question = MultipleChoiceQuestion(
                    id=q_data['id'],
                    question_text=q_data['question_text'],
                    options=q_data['options'],
                    correct_option=q_data['correct_option'],
                    points=q_data.get('points', 10),
                    difficulty=q_data.get('difficulty', 'medium')
                )
            else:
                question = ShortAnswerQuestion(
                    id=q_data['id'],
                    question_text=q_data['question_text'],
                    correct_answer=q_data['correct_answer'],
                    points=q_data.get('points', 10),
                    difficulty=q_data.get('difficulty', 'medium'),
                    case_sensitive=q_data.get('case_sensitive', False)
                )
            self.questions.append(question)
    
    def get_all(self) -> list[Question]:
        """Return all questions."""
        return self.questions.copy()
    
    def get_random(self, count: int = 1, difficulty: Optional[str] = None) -> list[Question]:
        """Get random questions, optionally filtered by difficulty."""
        filtered = self.questions
        if difficulty:
            filtered = [q for q in self.questions if q.get_difficulty() == difficulty]
        
        if count >= len(filtered):
            return filtered.copy()
        
        return random.sample(filtered, count)
    
    def get_by_difficulty(self, difficulty: str) -> list[Question]:
        """Filter questions by difficulty level."""
        return [q for q in self.questions if q.get_difficulty() == difficulty]
    
    def size(self) -> int:
        """Return the total number of questions."""
        return len(self.questions)
