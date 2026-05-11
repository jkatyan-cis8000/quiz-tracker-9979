"""Unit tests for QuestionBank class."""

import unittest
import json
import tempfile
from pathlib import Path

from questions import MultipleChoiceQuestion, ShortAnswerQuestion
from bank import QuestionBank


class TestQuestionBank(unittest.TestCase):
    """Tests for QuestionBank class."""
    
    def setUp(self):
        self.bank = QuestionBank()
    
    def test_add_question(self):
        question = MultipleChoiceQuestion(
            id="q1",
            question_text="Test",
            options=["A", "B"],
            correct_option=0
        )
        self.bank.add_question(question)
        self.assertEqual(self.bank.size(), 1)
    
    def test_load_from_file(self):
        data = {
            "questions": [
                {
                    "id": "q1",
                    "type": "multiple_choice",
                    "question_text": "Test?",
                    "options": ["A", "B"],
                    "correct_option": 0
                },
                {
                    "id": "q2",
                    "type": "short_answer",
                    "question_text": "Answer?",
                    "correct_answer": "test"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        
        try:
            count = self.bank.load_from_file(temp_path)
            self.assertEqual(count, 2)
            self.assertEqual(self.bank.size(), 2)
        finally:
            Path(temp_path).unlink()
    
    def test_get_random(self):
        self.bank.load_from_file('sample_question_bank.json')
        questions = self.bank.get_random(3)
        self.assertEqual(len(questions), 3)
    
    def test_get_random_with_difficulty(self):
        self.bank.load_from_file('sample_question_bank.json')
        questions = self.bank.get_random(difficulty="easy")
        self.assertTrue(all(q.get_difficulty() == "easy" for q in questions))
    
    def test_get_by_difficulty(self):
        self.bank.load_from_file('sample_question_bank.json')
        easy_questions = self.bank.get_by_difficulty("easy")
        self.assertTrue(all(q.get_difficulty() == "easy" for q in easy_questions))
    
    def test_get_by_type(self):
        self.bank.load_from_file('sample_question_bank.json')
        mc_questions = self.bank.get_by_type("multiple_choice")
        self.assertTrue(all(isinstance(q, MultipleChoiceQuestion) for q in mc_questions))
    
    def test_get_all(self):
        self.bank.load_from_file('sample_question_bank.json')
        all_questions = self.bank.get_all()
        self.assertEqual(len(all_questions), self.bank.size())
    
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.bank.load_from_file('nonexistent.json')


if __name__ == '__main__':
    unittest.main()
