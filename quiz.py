"""Quiz engine for managing quiz sessions."""

from typing import List, Optional, Dict, Tuple
from questions import Question, MultipleChoiceQuestion, ShortAnswerQuestion, QuestionBank


class QuizSession:
    """Tracks a single quiz session's state and results."""
    
    def __init__(self, question_bank: QuestionBank):
        self.question_bank = question_bank
        self.current_question_index = 0
        self.questions_answered: List[Tuple[Question, str, bool]] = []
        self.score = 0
        self.total_points = 0
    
    def start(self, questions: List[Question]) -> None:
        """Start the quiz with the given questions."""
        self.current_question_index = 0
        self.questions_answered = []
        self.score = 0
        self.total_points = sum(q.get_points() for q in questions)
    
    def get_current_question(self) -> Optional[Question]:
        """Get the current question or None if quiz is complete."""
        if self.current_question_index >= len(self.questions_answered):
            return None
        return self.questions_answered[self.current_question_index][0]
    
    def answer_question(self, answer: str) -> bool:
        """Submit an answer for the current question."""
        if self.current_question_index >= len(self.questions_answered):
            return False
        
        question, _, _ = self.questions_answered[self.current_question_index]
        is_correct = question.check_answer(answer)
        
        if is_correct:
            self.score += question.get_points()
        
        self.questions_answered[self.current_question_index] = (
            question,
            answer,
            is_correct
        )
        
        self.current_question_index += 1
        return True
    
    def get_score(self) -> int:
        """Get the current score."""
        return self.score
    
    def get_total_points(self) -> int:
        """Get the total possible points."""
        return self.total_points
    
    def get_review_data(self) -> List[Tuple[Question, str, bool]]:
        """Get all questions with user answers and correctness for review."""
        return self.questions_answered.copy()
    
    def is_complete(self) -> bool:
        """Check if all questions have been answered."""
        return self.current_question_index >= len(self.questions_answered)


class QuizEngine:
    """Manages quiz flow, answer validation, scoring, and user responses."""
    
    def __init__(self, show_correct_answers: bool = False):
        self.show_correct_answers = show_correct_answers
        self.session: Optional[QuizSession] = None
        self.questions: List[Question] = []
    
    def load_questions(self, question_bank: QuestionBank, count: int = 10, 
                       difficulty: Optional[str] = None) -> bool:
        """Load questions from a question bank."""
        questions = question_bank.get_random(count=count, difficulty=difficulty)
        if not questions:
            return False
        
        self.questions = questions
        self.session = QuizSession(question_bank)
        self.session.start(questions)
        return True
    
    def get_current_question(self) -> Optional[Question]:
        """Get the current question for display."""
        if self.session is None:
            return None
        return self.session.get_current_question()
    
    def answer_question(self, answer: str) -> bool:
        """Submit an answer and advance to next question."""
        if self.session is None:
            return False
        return self.session.answer_question(answer)
    
    def get_score(self) -> int:
        """Get the current score."""
        if self.session is None:
            return 0
        return self.session.get_score()
    
    def get_total_points(self) -> int:
        """Get the total possible points."""
        if self.session is None:
            return 0
        return self.session.get_total_points()
    
    def is_complete(self) -> bool:
        """Check if the quiz is complete."""
        if self.session is None:
            return True
        return self.session.is_complete()
    
    def get_final_results(self) -> Dict:
        """Get final quiz results including score and review data."""
        if self.session is None:
            return {}
        
        results = {
            'score': self.session.get_score(),
            'total_points': self.session.get_total_points(),
            'percentage': round((self.session.get_score() / self.session.get_total_points()) * 100, 1) if self.session.get_total_points() > 0 else 0,
            'correct_answers': []
        }
        
        if self.show_correct_answers:
            for question, user_answer, is_correct in self.session.get_review_data():
                results['correct_answers'].append({
                    'question': question.question_text,
                    'user_answer': user_answer,
                    'correct_answer': question.get_correct_answer(),
                    'is_correct': is_correct,
                    'points_earned': question.get_points() if is_correct else 0
                })
        
        return results
    
    def get_review_data(self) -> List[Tuple[Question, str, bool]]:
        """Get review data for all questions."""
        if self.session is None:
            return []
        return self.session.get_review_data()
