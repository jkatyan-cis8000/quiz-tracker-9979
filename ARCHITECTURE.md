# Quiz Tracker Architecture

## 1. Module Structure

```
quiz-tracker/
├── main.py              # Entry point, orchestrates quiz session
├── quiz.py              # Core Quiz class, session management
├── questions.py         # Question classes and factories
├── bank.py              # Question bank loading and storage
├── scoring.py           # Score calculation and tracking
├── ui.py                # User interface display functions
├── config.py            # Configuration loading and defaults
└── ARCHITECTURE.md      # This file
```

## 2. Class Definitions and Responsibilities

### Question Classes (`questions.py`)

**Question (abstract base)**
- `id`: str - Unique identifier
- `question_text`: str - The question prompt
- `points`: int - Point value for correct answer
- `difficulty`: str - Easy/Medium/Hard
- `display()`: void - Render question to user
- `check_answer(user_answer)`: bool - Validate answer
- `get_correct_answer()`: str - Return correct answer

**MultipleChoiceQuestion extends Question**
- `options`: list[str] - Available choices
- `correct_option`: int - Index of correct choice
- `display()` - Shows question with numbered options
- `check_answer(user_answer)` - Validates against option index

**ShortAnswerQuestion extends Question**
- `correct_answer`: str - Expected answer text
- `case_sensitive`: bool - Whether case matters
- `display()` - Shows question text only
- `check_answer(user_answer)` - Normalizes and compares text

### Question Bank (`bank.py`)

**QuestionBank**
- `questions`: list[Question] - Collection of loaded questions
- `load_from_file(filepath)`: void - Load questions from JSON/YAML
- `get_random(difficulty=None, count=1)`: list[Question] - Select random subset
- `get_by_difficulty(difficulty)`: list[Question] - Filter by difficulty
- `size()`: int - Total question count

### Quiz Session (`quiz.py`)

**QuizSession**
- `bank`: QuestionBank - Source of questions
- `questions`: list[Question] - Current quiz questions
- `user_answers`: dict[str, str] - Map question_id → answer
- `score`: int - Current score
- `show_correct_after`: bool - Display answers flag
- `start(bank, question_count, show_correct_after)`: void - Initialize session
- `present_question(question)`: str - Display and get user input
- `grade_question(question_id, answer)`: bool - Check and score
- `calculate_final_score()`: int - Compute total
- `display_results()`: void - Show score and answers if enabled

### Scoring (`scoring.py`)

**ScoreCalculator**
- `calculate_per_question(question, is_correct)`: int - Points for single question
- `apply_difficulty_multiplier(question, points)`: int - Boost for harder questions
- `calculate_final(score, total_possible)`: dict - Complete score report

### Configuration (`config.py`)

**Config**
- `default_question_count`: int
- `default_difficulty`: str
- `default_show_correct`: bool
- `question_file_paths`: list[str]
- `load_from_file(filepath)`: Config
- `get(key)`: any - Retrieve config value

### UI Layer (`ui.py`)

**UI**
- `display_welcome()`: void
- `display_question(question, index, total)`: void
- `get_user_input(question)`: str
- `display_result_summary(quiz)`: void
- `display_question_review(question, user_answer, is_correct)`: void

## 3. Data Flow

```
┌─────────────┐
│   main.py   │
│ (entry)     │
└──────┬──────┘
       │
       │ 1. Load config
       ▼
┌─────────────┐
│  config.py  │
│  (settings) │
└──────┬──────┘
       │
       │ 2. Load question bank
       ▼
┌─────────────┐
│   bank.py   │
│  (storage)  │
└──────┬──────┘
       │
       │ 3. Create quiz session
       ▼
┌─────────────┐
│   quiz.py   │
│  (orchestra)│
└──────┬──────┘
       │
       │ 4. Present questions
       ▼
┌─────────────┐
│   ui.py     │
│  (display)  │
└──────┬──────┘
       │
       │ 5. Get user input
       ▼
┌─────────────┐
│ questions.py│
│ (validate)  │
└──────┬──────┘
       │
       │ 6. Score calculation
       ▼
┌─────────────┐
│ scoring.py  │
│ (compute)   │
└──────┬──────┘
       │
       │ 7. Display results
       ▼
┌─────────────┐
│   ui.py     │
│  (output)   │
└─────────────┘
```

## 4. Configuration Options

**config.yaml** (example):
```yaml
default_question_count: 10
default_difficulty: medium
default_show_correct: true
question_files:
  - data/questions.json
  - data/extra.json
scoring:
  difficulty_multiplier:
    easy: 1.0
    medium: 1.5
    hard: 2.0
```

**Runtime Parameters:**
- `question_count`: Number of questions per quiz
- `difficulty_filter`: Filter by difficulty level
- `show_correct_after`: Whether to reveal answers at end
- `randomize`: Shuffle question order

## 5. File Organization

### Core Modules
| File | Purpose | Key Classes |
|------|---------|-------------|
| `main.py` | Script entry point | QuizApp (runner) |
| `quiz.py` | Session management | QuizSession |
| `questions.py` | Question types | Question, MultipleChoiceQuestion, ShortAnswerQuestion |
| `bank.py` | Question persistence | QuestionBank |
| `scoring.py` | Score computation | ScoreCalculator |
| `ui.py` | User interaction | UI |

### Data Files
| Path | Purpose |
|------|---------|
| `data/questions.json` | Default question bank (JSON format) |
| `data/config.yaml` | Application configuration |
| `logs/` | Quiz session logs (optional) |

### Design Principles
- **Separation of Concerns**: UI, logic, and data are in separate modules
- **Open/Closed**: Easy to add new question types without modifying existing code
- **Dependency Injection**: QuizSession receives QuestionBank, not creates it
- **State Management**: QuizSession holds all session state, no global variables
- **Configurable**: External config file, no hardcoded values
