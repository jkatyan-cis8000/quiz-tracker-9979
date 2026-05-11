"""Unit tests for Question classes."""

import unittest
from questions import MultipleChoiceQuestion, ShortAnswerQuestion


class TestMultipleChoiceQuestion(unittest.TestCase):
    """Tests for MultipleChoiceQuestion class."""
    
    def setUp(self):
        self.question = MultipleChoiceQuestion(
            id="q1",
            question_text="What is 2 + 2?",
            options=["3", "4", "5", "6"],
            correct_option=1,
            points=10,
            difficulty="easy"
        )
    
    def test_display(self):
        display = self.question.display()
        self.assertIn("What is 2 + 2?", display)
        self.assertIn("1. 3", display)
        self.assertIn("2. 4", display)
    
    def test_correct_answer(self):
        self.assertTrue(self.question.check_answer("2"))
        self.assertEqual(self.question.get_correct_answer(), "4")
    
    def test_incorrect_answer(self):
        self.assertFalse(self.question.check_answer("1"))
        self.assertFalse(self.question.check_answer("3"))
    
    def test_invalid_answer(self):
        self.assertFalse(self.question.check_answer("abc"))
    
    def test_get_points(self):
        self.assertEqual(self.question.get_points(), 10)
    
    def test_get_difficulty(self):
        self.assertEqual(self.question.get_difficulty(), "easy")


class TestShortAnswerQuestion(unittest.TestCase):
    """Tests for ShortAnswerQuestion class."""
    
    def setUp(self):
        self.question = ShortAnswerQuestion(
            id="q2",
            question_text="What is H2O?",
            correct_answer="water",
            points=15,
            difficulty="medium",
            case_sensitive=False
        )
    
    def test_display(self):
        display = self.question.display()
        self.assertIn("What is H2O?", display)
    
    def test_correct_answer_case_insensitive(self):
        self.assertTrue(self.question.check_answer("WATER"))
        self.assertTrue(self.question.check_answer("Water"))
        self.assertTrue(self.question.check_answer("water"))
    
    def test_correct_answer_case_sensitive(self):
        question_sensitive = ShortAnswerQuestion(
            id="q3",
            question_text="Capital of France?",
            correct_answer="Paris",
            case_sensitive=True
        )
        self.assertTrue(question_sensitive.check_answer("Paris"))
        self.assertFalse(question_sensitive.check_answer("paris"))
    
    def test_correct_answer(self):
        self.assertTrue(self.question.check_answer("water"))
        self.assertEqual(self.question.get_correct_answer(), "water")
    
    def test_incorrect_answer(self):
        self.assertFalse(self.question.check_answer("oil"))
        self.assertFalse(self.question.check_answer(""))
    
    def test_get_points(self):
        self.assertEqual(self.question.get_points(), 15)
    
    def test_get_difficulty(self):
        self.assertEqual(self.question.get_difficulty(), "medium")


if __name__ == '__main__':
    unittest.main()
