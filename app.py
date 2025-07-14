from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import random
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Load questions from CSV
def load_questions():
    try:
        return pd.read_csv('data/questions.csv')
    except:
        # Return empty DataFrame with correct columns if file doesn't exist yet
        return pd.DataFrame(columns=['id', 'topic', 'difficulty', 'question', 'answer'])

# Filter questions based on topic and difficulty
def filter_questions(df, topic, difficulty, num_questions):
    # Handle linked list subtypes
    if topic in ['Singly Linked List', 'Doubly Linked List', 'Circular Linked List']:
        filtered = df[(df['topic'] == topic) & (df['difficulty'] == difficulty)]
    else:
        filtered = df[(df['topic'] == topic) & (df['difficulty'] == difficulty)]
    
    if len(filtered) < num_questions:
        return filtered.to_dict('records')
    return random.sample(filtered.to_dict('records'), num_questions)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_questions', methods=['POST'])
def get_questions():
    data = request.get_json()
    topic = data.get('topic')
    difficulty = int(data.get('difficulty'))
    num_questions = int(data.get('num_questions'))
    
    questions_df = load_questions()
    filtered_questions = filter_questions(questions_df, topic, difficulty, num_questions)
    
    # Generate random values for each question
    for question in filtered_questions:
        question['values'] = generate_random_values(question['topic'])
    
    return jsonify(filtered_questions)

def generate_random_values(topic):
    """Generate random values based on the data structure type"""
    if topic == 'Array':
        # Generate a random array of 5-10 integers between 1-99
        return [random.randint(1, 99) for _ in range(random.randint(5, 10))]
    
    elif topic in ['Singly Linked List', 'Doubly Linked List', 'Circular Linked List']:
        # Generate a random linked list of 5-8 nodes
        return [random.randint(1, 99) for _ in range(random.randint(5, 8))]
    
    elif topic == 'Tree':
        # Generate a random binary tree with 7-15 nodes
        # For simplicity, we'll just generate an array that will be converted to a tree on the frontend
        return [random.randint(1, 99) for _ in range(random.randint(7, 15))]
    
    return []

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Create sample questions CSV if it doesn't exist
    if not os.path.exists('data/questions.csv'):
        from utils.generate_sample_questions import generate_sample_questions
        generate_sample_questions()
        
    app.run(debug=True)