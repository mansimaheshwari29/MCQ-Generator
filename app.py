from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="MCQ Generator", page_icon=":books:", layout="wide")

# CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        margin: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    h1 {
        color: #4A90E2;
        text-align: center;
    }
    h2 {
        color: #333;
        text-align: center;
    }
    p {
        font-size: 18px;
        text-align: left;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #000000;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subheader {
        font-size: 1.5em;
        color: #333;
        margin-bottom: 1em;
    }
    .question {
        font-weight: bold;
        margin-top: 1em;
           
    }
    .answer {
        color: #007BFF;
        margin-bottom: 0.5em;
           
    }
    .sidebar .sidebar-content {
        text-align: center;
    }
    .sidebar .sidebar-content img {
        max-width: 80%;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Configure Gem AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question, num_questions):
    question_prompt = f"{question} mcq (Generate {num_questions} questions)"
    response = chat.send_message(question_prompt, stream=True)
    return response

# Initialize Streamlit app


st.markdown('<div class="title">MCQ Generator</div>', unsafe_allow_html=True)
# st.title("MCQ Generator using Large Language Model")
st.markdown(
    """
    <div class="main">
        <h1>Generate Multiple Choice Questions</h1>
        <p>Welcome to MCQ Generator using Large Language Model (LLM). Enter your question below and select the difficulty level 
        to generate multiple choice questions. You can specify the number of questions you want to generate.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for additional features
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    image_path = r"D:\major\logo.jpg"
    st.image(image_path,caption=" MCQ Generator")
    # st.image("logo.png", caption="AI MCQ Generator")
    st.write("Use this app to generate multiple-choice questions (MCQs) based on your input.")
    st.write("Powered by MBM University.")
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


# Input field for user question
input_question = st.text_input("Input: ", key="input")

# Slider for number of questions
num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)

# Button to ask the question
submit_button = st.button("Generate questions")

# Process user input and display response
if submit_button and input_question:
    response = get_gemini_response(input_question, num_questions)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_question))
    st.markdown('<div class="subheader">The Response is:</div>', unsafe_allow_html=True)
    # Concatenate lines of the response into a single block of text
    response_text = "\n".join(chunk.text for chunk in response)
    st.write(response_text)
    st.session_state['chat_history'].append(("Bot", response_text))
    