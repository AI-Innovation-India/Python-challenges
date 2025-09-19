# -------------------------------
# Quiz Game App ❓
 
# Features:
 
# Multiple-choice questions (hardcoded in list/dict).
 
# User selects answers via radio buttons.
 
# Keep score using st.session_state.
 
# Show final score at the end.
# -------------------------------


import streamlit as st
import time
import random
from typing import Dict, List, Any
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="Quiz Master 🧠",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .quiz-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 1rem 0;
    }
    
    .question-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .score-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(17, 153, 142, 0.3);
    }
    
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .timer-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .result-excellent {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-good {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-fair {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .result-poor {
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .category-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .stRadio > div {
        background: #f8f9ff;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e4e7;
        margin: 0.5rem 0;
    }
    
    .stRadio > div:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Quiz Questions Database
QUIZ_CATEGORIES = {
    "General Knowledge": {
        "icon": "🌍",
        "color": "#667eea",
        "questions": [
            {
                "question": "What is the capital of Australia?",
                "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "correct": 2,
                "explanation": "Canberra is the capital city of Australia, chosen as a compromise between Sydney and Melbourne."
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": 1,
                "explanation": "Mars is called the Red Planet due to iron oxide (rust) on its surface."
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["African Elephant", "Blue Whale", "Giraffe", "Polar Bear"],
                "correct": 1,
                "explanation": "The Blue Whale is the largest mammal and the largest animal ever known to have lived on Earth."
            },
            {
                "question": "In which year did World War II end?",
                "options": ["1944", "1945", "1946", "1947"],
                "correct": 1,
                "explanation": "World War II ended in 1945 with the surrender of Japan in August."
            }
        ]
    },
    "Science & Technology": {
        "icon": "🔬",
        "color": "#11998e",
        "questions": [
            {
                "question": "What does 'AI' stand for in technology?",
                "options": ["Automatic Intelligence", "Artificial Intelligence", "Advanced Integration", "Automated Interface"],
                "correct": 1,
                "explanation": "AI stands for Artificial Intelligence, which refers to machine intelligence."
            },
            {
                "question": "What is the chemical symbol for gold?",
                "options": ["Go", "Gd", "Au", "Ag"],
                "correct": 2,
                "explanation": "Au is the chemical symbol for gold, derived from the Latin word 'aurum'."
            },
            {
                "question": "How many bones are in an adult human body?",
                "options": ["196", "206", "216", "226"],
                "correct": 1,
                "explanation": "An adult human body has 206 bones, while babies are born with about 270 bones."
            },
            {
                "question": "What is the speed of light in vacuum?",
                "options": ["299,792,458 m/s", "300,000,000 m/s", "299,000,000 m/s", "301,000,000 m/s"],
                "correct": 0,
                "explanation": "The speed of light in vacuum is exactly 299,792,458 meters per second."
            }
        ]
    },
    "Sports & Entertainment": {
        "icon": "⚽",
        "color": "#fa709a",
        "questions": [
            {
                "question": "How many players are there in a basketball team on court?",
                "options": ["4", "5", "6", "7"],
                "correct": 1,
                "explanation": "Each basketball team has 5 players on the court at any given time."
            },
            {
                "question": "Which movie won the Academy Award for Best Picture in 2020?",
                "options": ["1917", "Joker", "Parasite", "Once Upon a Time in Hollywood"],
                "correct": 2,
                "explanation": "Parasite won the Academy Award for Best Picture in 2020, making history as the first non-English film to win."
            },
            {
                "question": "In which sport would you perform a slam dunk?",
                "options": ["Tennis", "Basketball", "Volleyball", "Baseball"],
                "correct": 1,
                "explanation": "A slam dunk is a basketball shot where the player jumps and forces the ball down through the basket."
            },
            {
                "question": "How often are the Summer Olympic Games held?",
                "options": ["Every 2 years", "Every 3 years", "Every 4 years", "Every 5 years"],
                "correct": 2,
                "explanation": "The Summer Olympic Games are held every 4 years (quadrennially)."
            }
        ]
    }
}

class QuizValidator:
    @staticmethod
    def validate_player_name(name: str) -> Dict[str, Any]:
        """Validate player name"""
        name = name.strip()
        if not name:
            return {"is_valid": False, "message": "Player name cannot be empty!"}
        if len(name) < 2:
            return {"is_valid": False, "message": "Player name must be at least 2 characters long!"}
        if len(name) > 30:
            return {"is_valid": False, "message": "Player name must be less than 30 characters!"}
        if not name.replace(" ", "").replace("-", "").replace("_", "").isalnum():
            return {"is_valid": False, "message": "Player name can only contain letters, numbers, spaces, hyphens, and underscores!"}
        return {"is_valid": True, "message": "Valid player name!"}
    
    @staticmethod
    def validate_category_selection(category: str) -> Dict[str, Any]:
        """Validate category selection"""
        if not category or category == "Select a category":
            return {"is_valid": False, "message": "Please select a quiz category!"}
        if category not in QUIZ_CATEGORIES:
            return {"is_valid": False, "message": "Invalid category selected!"}
        return {"is_valid": True, "message": "Category selected!"}
    
    @staticmethod
    def validate_answer_selection(selected_answer: Any) -> Dict[str, Any]:
        """Validate answer selection"""
        if selected_answer is None:
            return {"is_valid": False, "message": "Please select an answer before proceeding!"}
        return {"is_valid": True, "message": "Answer selected!"}

class QuizGame:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize all session state variables"""
        default_values = {
            'quiz_started': False,
            'quiz_completed': False,
            'current_question': 0,
            'score': 0,
            'user_answers': [],
            'player_name': '',
            'selected_category': '',
            'quiz_questions': [],
            'start_time': None,
            'end_time': None,
            'show_explanation': False,
            'question_answered': False,
            'quiz_stats': {'total_quizzes': 0, 'best_score': 0, 'categories_played': set()}
        }
        
        for key, value in default_values.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def reset_quiz(self):
        """Reset quiz to initial state"""
        st.session_state.quiz_started = False
        st.session_state.quiz_completed = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.session_state.quiz_questions = []
        st.session_state.start_time = None
        st.session_state.end_time = None
        st.session_state.show_explanation = False
        st.session_state.question_answered = False
    
    def start_quiz(self, player_name: str, category: str):
        """Start a new quiz"""
        st.session_state.player_name = player_name
        st.session_state.selected_category = category
        st.session_state.quiz_questions = QUIZ_CATEGORIES[category]["questions"].copy()
        
        # Shuffle questions for variety
        random.shuffle(st.session_state.quiz_questions)
        
        st.session_state.quiz_started = True
        st.session_state.start_time = datetime.now()
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.user_answers = []
        st.session_state.question_answered = False
    
    def submit_answer(self, selected_answer_index: int):
        """Submit an answer and update score"""
        current_q = st.session_state.quiz_questions[st.session_state.current_question]
        is_correct = selected_answer_index == current_q["correct"]
        
        st.session_state.user_answers.append({
            'question_index': st.session_state.current_question,
            'selected': selected_answer_index,
            'correct': current_q["correct"],
            'is_correct': is_correct
        })
        
        if is_correct:
            st.session_state.score += 1
        
        st.session_state.question_answered = True
        st.session_state.show_explanation = True
    
    def next_question(self):
        """Move to next question or complete quiz"""
        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
            st.session_state.current_question += 1
            st.session_state.question_answered = False
            st.session_state.show_explanation = False
        else:
            self.complete_quiz()
    
    def complete_quiz(self):
        """Complete the quiz and update stats"""
        st.session_state.quiz_completed = True
        st.session_state.end_time = datetime.now()
        
        # Update quiz statistics
        st.session_state.quiz_stats['total_quizzes'] += 1
        if st.session_state.score > st.session_state.quiz_stats['best_score']:
            st.session_state.quiz_stats['best_score'] = st.session_state.score
        st.session_state.quiz_stats['categories_played'].add(st.session_state.selected_category)
    
    def get_performance_rating(self, score: int, total: int) -> Dict[str, str]:
        """Get performance rating based on score"""
        percentage = (score / total) * 100
        
        if percentage >= 90:
            return {"rating": "Excellent! 🏆", "class": "result-excellent", "message": "Outstanding performance! You're a quiz master!"}
        elif percentage >= 70:
            return {"rating": "Good! 👍", "class": "result-good", "message": "Great job! You have solid knowledge!"}
        elif percentage >= 50:
            return {"rating": "Fair 📚", "class": "result-fair", "message": "Not bad! Keep learning and improving!"}
        else:
            return {"rating": "Keep Trying! 💪", "class": "result-poor", "message": "Don't give up! Practice makes perfect!"}

def main():
    # Initialize quiz game
    quiz = QuizGame()
    
    # Main title
    st.markdown('<h1 class="main-title">🎯 Quiz Master Challenge</h1>', unsafe_allow_html=True)
    
    # Sidebar with stats and controls
    with st.sidebar:
        st.markdown("### 📊 Quiz Statistics")
        stats = st.session_state.quiz_stats
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Quizzes", stats['total_quizzes'])
        with col2:
            st.metric("Best Score", f"{stats['best_score']}/4")
        
        if stats['categories_played']:
            st.markdown("**Categories Played:**")
            for cat in stats['categories_played']:
                st.markdown(f"• {QUIZ_CATEGORIES[cat]['icon']} {cat}")
        
        st.markdown("---")
        
        if st.session_state.quiz_started and not st.session_state.quiz_completed:
            st.markdown("### 🎮 Current Quiz")
            progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
            st.progress(progress)
            st.markdown(f"Question {st.session_state.current_question + 1} of {len(st.session_state.quiz_questions)}")
            
            if st.button("🔄 Restart Quiz", type="secondary"):
                quiz.reset_quiz()
                st.rerun()
    
    # Main content area
    if not st.session_state.quiz_started:
        # Welcome screen and quiz setup
        st.markdown("""
        <div class="info-box">
            <h3>🎮 Welcome to Quiz Master Challenge!</h3>
            <p>Test your knowledge across different categories. Each quiz contains 4 carefully crafted questions 
            with instant feedback and explanations. Are you ready to challenge yourself?</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Player setup form
        with st.container():
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
            st.markdown("### 👤 Player Setup")
            
            # Player name input
            player_name = st.text_input(
                "Enter your name:",
                placeholder="Your awesome name here...",
                max_chars=30,
                key="player_name_input"
            )
            
            # Validate player name in real-time
            if player_name:
                name_validation = QuizValidator.validate_player_name(player_name)
                if name_validation["is_valid"]:
                    st.success(name_validation["message"])
                else:
                    st.error(name_validation["message"])
            
            st.markdown("### 📚 Choose Your Challenge")
            
            # Category selection with visual cards
            cols = st.columns(3)
            selected_category = None
            
            for i, (category, data) in enumerate(QUIZ_CATEGORIES.items()):
                with cols[i % 3]:
                    if st.button(
                        f"{data['icon']} {category}\n{len(data['questions'])} Questions",
                        key=f"cat_{category}",
                        use_container_width=True
                    ):
                        selected_category = category
            
            if selected_category:
                st.session_state.temp_category = selected_category
                st.markdown(f'<div class="category-badge">{QUIZ_CATEGORIES[selected_category]["icon"]} Selected: {selected_category}</div>', unsafe_allow_html=True)
            
            # Start quiz button
            start_col1, start_col2, start_col3 = st.columns([1, 2, 1])
            with start_col2:
                if st.button("🚀 Start Quiz Challenge!", type="primary", use_container_width=True):
                    # Validate inputs
                    name_validation = QuizValidator.validate_player_name(player_name)
                    category_validation = QuizValidator.validate_category_selection(
                        getattr(st.session_state, 'temp_category', '')
                    )
                    
                    if name_validation["is_valid"] and category_validation["is_valid"]:
                        quiz.start_quiz(player_name, st.session_state.temp_category)
                        st.rerun()
                    else:
                        if not name_validation["is_valid"]:
                            st.error(name_validation["message"])
                        if not category_validation["is_valid"]:
                            st.error(category_validation["message"])
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        # Active quiz interface
        current_q_index = st.session_state.current_question
        current_question = st.session_state.quiz_questions[current_q_index]
        
        # Quiz header
        st.markdown(f"""
        <div class="question-header">
            <h3>👋 {st.session_state.player_name} | {QUIZ_CATEGORIES[st.session_state.selected_category]['icon']} {st.session_state.selected_category}</h3>
            <div>Question {current_q_index + 1} of {len(st.session_state.quiz_questions)} | Current Score: {st.session_state.score}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Question container
        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
        
        st.markdown(f"### ❓ {current_question['question']}")
        
        if not st.session_state.question_answered:
            # Answer selection
            selected_answer = st.radio(
                "Choose your answer:",
                options=range(len(current_question["options"])),
                format_func=lambda x: f"{chr(65+x)}. {current_question['options'][x]}",
                key=f"q_{current_q_index}"
            )
            
            # Submit answer button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("✅ Submit Answer", type="primary", use_container_width=True):
                    answer_validation = QuizValidator.validate_answer_selection(selected_answer)
                    if answer_validation["is_valid"]:
                        quiz.submit_answer(selected_answer)
                        st.rerun()
                    else:
                        st.error(answer_validation["message"])
        
        else:
            # Show results and explanation
            user_answer = st.session_state.user_answers[-1]
            correct_answer = current_question["correct"]
            
            # Display user's answer
            if user_answer["is_correct"]:
                st.success(f"🎉 Correct! You selected: {chr(65+user_answer['selected'])}. {current_question['options'][user_answer['selected']]}")
            else:
                st.error(f"❌ Incorrect! You selected: {chr(65+user_answer['selected'])}. {current_question['options'][user_answer['selected']]}")
                st.info(f"✅ Correct answer: {chr(65+correct_answer)}. {current_question['options'][correct_answer]}")
            
            # Show explanation
            if st.session_state.show_explanation:
                st.markdown("### 💡 Explanation")
                st.markdown(f"*{current_question['explanation']}*")
            
            # Next question button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                next_text = "🏁 Finish Quiz" if current_q_index == len(st.session_state.quiz_questions) - 1 else "➡️ Next Question"
                if st.button(next_text, type="primary", use_container_width=True):
                    quiz.next_question()
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.quiz_completed:
        # Quiz results screen
        total_questions = len(st.session_state.quiz_questions)
        final_score = st.session_state.score
        percentage = (final_score / total_questions) * 100
        
        # Calculate quiz duration
        duration = st.session_state.end_time - st.session_state.start_time
        duration_seconds = int(duration.total_seconds())
        
        performance = quiz.get_performance_rating(final_score, total_questions)
        
        # Results header
        st.markdown(f"""
        <div class="{performance['class']}">
            <h2>🎊 Quiz Completed!</h2>
            <h3>Congratulations, {st.session_state.player_name}!</h3>
            <h1>{final_score}/{total_questions} ({percentage:.1f}%)</h1>
            <h3>{performance['rating']}</h3>
            <p>{performance['message']}</p>
            <p>⏱️ Time taken: {duration_seconds // 60}m {duration_seconds % 60}s</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed results
        st.markdown("### 📋 Detailed Results")
        
        for i, answer in enumerate(st.session_state.user_answers):
            question = st.session_state.quiz_questions[answer['question_index']]
            
            with st.expander(f"Question {i+1}: {question['question']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Your Answer:**")
                    user_choice = question['options'][answer['selected']]
                    if answer['is_correct']:
                        st.success(f"✅ {chr(65+answer['selected'])}. {user_choice}")
                    else:
                        st.error(f"❌ {chr(65+answer['selected'])}. {user_choice}")
                
                with col2:
                    st.markdown("**Correct Answer:**")
                    correct_choice = question['options'][answer['correct']]
                    st.info(f"✅ {chr(65+answer['correct'])}. {correct_choice}")
                
                st.markdown(f"**Explanation:** {question['explanation']}")
        
        # Action buttons
        st.markdown("### 🎮 What's Next?")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Play Same Category", type="secondary", use_container_width=True):
                quiz.start_quiz(st.session_state.player_name, st.session_state.selected_category)
                st.rerun()
        
        with col2:
            if st.button("🎯 Try Different Category", type="secondary", use_container_width=True):
                quiz.reset_quiz()
                st.rerun()
        
        with col3:
            if st.button("🏠 Back to Home", type="primary", use_container_width=True):
                quiz.reset_quiz()
                st.session_state.player_name = ''
                st.rerun()

if __name__ == "__main__":
    main()