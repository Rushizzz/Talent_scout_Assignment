import streamlit as st
from langchain_groq import ChatGroq
import json
from datetime import datetime

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_question" not in st.session_state:
    st.session_state.current_question = "name"
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "current_tech_question_index" not in st.session_state:
    st.session_state.current_tech_question_index = 0
if "in_tech_assessment" not in st.session_state:
    st.session_state.in_tech_assessment = False

def check_for_exit(user_input):
    exit_prompt = f"""
    Check if this message indicates the user wants to exit or stop the conversation.
    Message: '{user_input}'
    Common exit phrases include: exit, quit, stop, bye, don't want to continue, not interested, etc.
    Respond with only 'exit' or 'continue'
    """
    response = llm.invoke(exit_prompt)
    return response.content.lower().strip() == 'exit'

# Questions and validation criteria
QUESTIONS = {
    "name": {
        "question": "What is your full name?",
        "validation_prompt": "Is this a valid full name? It should contain first and last name, only letters and spaces, no numbers or special characters. Respond with only 'valid' or 'invalid'"
    },
    "email": {
        "question": "What is your email address?",
        "validation_prompt": "Is this a valid email address? It should contain @ and a valid domain. Respond with only 'valid' or 'invalid'"
    },
    "phone": {
        "question": "What is your phone number? Please include your country code (e.g., +91 for India, +1 for USA, +44 for UK)",
        "validation_prompt": "Is this a valid phone number? It should start with + followed by country code and number. Example: +91XXXXXXXXXX. Respond with only 'valid' or 'invalid'"
    },
    "experience": {
        "question": "How many years of experience do you have? (Type 'fresher' if you have no experience)",
        "validation_prompt": "Is this a valid experience? Should be either a number, decimal, or the word 'fresher'. Respond with only 'valid' or 'invalid'"
    },
    "position": {
        "question": "What is your desired position?",
        "validation_prompt": "Is this a valid job position? Should be a reasonable job title in the technology field. Respond with only 'valid' or 'invalid'"
    },
    "location": {
        "question": "What is your current location?",
        "validation_prompt": "Is this a valid location? Should be a city, state, country or combination. Respond with only 'valid' or 'invalid'"
    },
    "tech_stack": {
        "question": "Please list your tech stack (technologies you're proficient in):",
        "validation_prompt": "Is this a valid tech stack? Should contain known programming languages, frameworks, or tools. Respond with only 'valid' or 'invalid'"
    }
}

def validate_input(field, user_input):
    validation_prompt = QUESTIONS[field]["validation_prompt"]
    prompt = f"Input: '{user_input}'\n{validation_prompt}"
    response = llm.invoke(prompt)
    response_text = response.content.lower().strip()
    
    # Check if response starts with 'valid' or 'invalid'
    is_valid = response_text.startswith('valid')
    error_message = response_text.split('invalid:', 1)[1].strip() if 'invalid:' in response_text else ""
    
    return is_valid, error_message

def process_user_input(user_input):
    # Check if user wants to exit
    if check_for_exit(user_input):
        return "Thank you for your time. Feel free to come back when you're ready to continue the application process. Have a great day!"
    
    if st.session_state.in_tech_assessment:
        return process_tech_assessment(user_input)
    else:
        return process_basic_info(user_input)

def process_basic_info(user_input):
    current_q = st.session_state.current_question
    
    # Special handling for experience if input is '0'
    if current_q == "experience" and user_input == "0":
        return "For candidates with no experience, please type 'fresher'. " + QUESTIONS[current_q]["question"]
    
    # Validate input
    is_valid, error_message = validate_input(current_q, user_input)
    
    if not is_valid:
        if current_q == "phone":
            return f"Invalid input: {error_message}\n\nPlease include your country code. Examples:\n- +91 XXXXXXXXXX (India)\n- +1 XXXXXXXXXX (USA)\n- +44 XXXXXXXXXX (UK)\n\nPlease try again."
        return f"Invalid input: {error_message}\n\nPlease answer again: {QUESTIONS[current_q]['question']}"
    
    # Store valid input
    st.session_state.candidate_info[current_q] = user_input
    
    # Move to next question
    questions_list = list(QUESTIONS.keys())
    current_index = questions_list.index(current_q)
    
    if current_index + 1 < len(questions_list):
        st.session_state.current_question = questions_list[current_index + 1]
        return QUESTIONS[questions_list[current_index + 1]]["question"]
    else:
        tech_stack = st.session_state.candidate_info["tech_stack"]
        st.session_state.tech_questions = generate_tech_questions(tech_stack)
        st.session_state.in_tech_assessment = True
        st.session_state.current_tech_question_index = 0
        return f"Great! Now I'll ask you a few technical questions based on your tech stack.\n\n{st.session_state.tech_questions[0]}"

def generate_tech_questions(tech_stack):
    prompt = f"""Generate 5 technical interview questions based on these technologies: {tech_stack}. 
    Questions should be:
    1. Specific to the mentioned technologies
    2. Mix of basic and intermediate level
    3. Focus on practical knowledge
    4. One question at a time
    
    For example, if tech_stack includes "Python", ask about generators, decorators, etc.
    If it includes "React", ask about hooks, virtual DOM, etc.
    
    Return exactly 5 questions separated by ||"""
    
    response = llm.invoke(prompt)
    questions = response.content.strip().split("||")
    return [q.strip() for q in questions if q.strip()]

def save_to_file(candidate_info):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"candidate_{timestamp}.txt"
    with open(filename, "w") as f:
        json.dump(candidate_info, f, indent=4)
    return filename

def process_tech_assessment(user_input):
    if check_for_exit(user_input):
        return "Thank you for your time. Feel free to come back when you're ready to continue the application process. Have a great day!"
        
    # Store the answer
    if "technical_answers" not in st.session_state.candidate_info:
        st.session_state.candidate_info["technical_answers"] = {}
    
    current_question = st.session_state.tech_questions[st.session_state.current_tech_question_index]
    st.session_state.candidate_info["technical_answers"][current_question] = user_input
    
    # Move to next question or finish
    st.session_state.current_tech_question_index += 1
    if st.session_state.current_tech_question_index < len(st.session_state.tech_questions):
        return st.session_state.tech_questions[st.session_state.current_tech_question_index]
    else:
        filename = save_to_file(st.session_state.candidate_info)
        return f"Thank you for completing the technical assessment! Your details and answers have been saved to {filename}. Our recruitment team will review your profile and get back to you soon."

st.title("TalentScout Hiring Assistant")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initial greeting (only show if no messages exist)
if len(st.session_state.messages) == 0:
    greeting = "Hello! I'm the TalentScout Hiring Assistant. I'll help you submit your application by asking a few questions. " + QUESTIONS["name"]["question"]
    with st.chat_message("assistant"):
        st.markdown(greeting)
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# React to user input
if prompt := st.chat_input("Enter your response"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get and display assistant response
    assistant_response = process_user_input(prompt)
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # If the response indicates exit, reset the session state
    if "thank you for your time" in assistant_response.lower():
        for key in list(st.session_state.keys()):
            del st.session_state[key]