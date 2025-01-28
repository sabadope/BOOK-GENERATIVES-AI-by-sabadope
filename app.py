from flask import Flask, request, render_template, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)

API_KEY = "AIzaSyDS7qQoeHhjU0ezBIN2cPWmx545Ngi9Xfg"

def initialize_model(api_key):
    try:
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
        }
        return genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
    except Exception as e:
        print(f"Error initializing the model: {e}")
        return None

def generate_book_idea(model, genre, topic):
    prompt = f"""
    Generate a creative book idea in the genre '{genre}' about the topic '{topic}'.
    Include:

    1. Brief Synopsis
    2. Plot
    3. Main Characters
    4. Theme of the story
    5. Possible Plot Twists
    6. Ending of the story
    7. Lesson or Moral of the story
    """
    try:
        response = model.generate_content(prompt)
        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "No content generated."
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    genre = request.form['genre']
    topic = request.form['topic']

    if not genre or not topic:
        return render_template('index.html', error="Both genre and topic are required.")

    model = initialize_model(API_KEY)
    if model:
        book_idea = generate_book_idea(model, genre, topic)
        # Store the generated book idea and genre/topic in session or redirect to another page
        return redirect(url_for('result', book_idea=book_idea, genre=genre, topic=topic))
    else:
        return render_template('index.html', error="Failed to initialize the model.")

@app.route('/result')
def result():
    book_idea = request.args.get('book_idea')
    genre = request.args.get('genre')
    topic = request.args.get('topic')
    return render_template('result.html', book_idea=book_idea, genre=genre, topic=topic)

if __name__ == '__main__':
    app.run(debug=True)