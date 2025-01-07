import streamlit as st
from langchain_groq import ChatGroq
import json
from datetime import datetime
from deep_translator import GoogleTranslator

# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7
)

# Language options (add more as needed)
LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh-cn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Arabic': 'ar',
    'Russian': 'ru'
}

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
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

def translate_text(text, dest_lang):
    if dest_lang == 'en':
        return text
    try:
        translator = GoogleTranslator(source='en', target=dest_lang)
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

# Replace the translate_to_english function with:
def translate_to_english(text, src_lang):
    if src_lang == 'en':
        return text
    try:
        translator = GoogleTranslator(source=src_lang, target='en')
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text
        
def check_for_exit(user_input):
    exit_prompt = f"""
    Check if this message indicates the user wants to exit or stop the conversation.
    Message: '{user_input}'
    Common exit phrases include: exit, quit, stop, bye, don't want to continue, not interested, etc.
    Respond with only 'exit' or 'continue'
    """
    response = llm.invoke(exit_prompt)
    if response.content.lower().strip() == 'exit':
        exit_message = "Thank you for your time. Feel free to come back when you're ready to continue the application process. Have a great day!"
        return True, translate_text(exit_message, LANGUAGES[st.session_state.selected_language])
    return False, ""

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
    # Translate user input to English for validation
    eng_input = translate_to_english(
        user_input, 
        LANGUAGES[st.session_state.selected_language]
    )
    
    validation_prompt = QUESTIONS[field]["validation_prompt"]
    prompt = f"Input: '{eng_input}'\n{validation_prompt}"
    response = llm.invoke(prompt)
    response_text = response.content.lower().strip()
    
    is_valid = response_text.startswith('valid')
    error_message = response_text.split('invalid:', 1)[1].strip() if 'invalid:' in response_text else ""
    
    # Translate error message if validation fails
    if not is_valid:
        error_message = translate_text(
            error_message, 
            LANGUAGES[st.session_state.selected_language]
        )
    
    return is_valid, error_message


def process_user_input(user_input):
    # Check if user wants to exit
    is_exit, exit_message = check_for_exit(user_input)
    if is_exit:
        return exit_message
    
    if st.session_state.in_tech_assessment:
        return process_tech_assessment(user_input)
    else:
        return process_basic_info(user_input)

def process_basic_info(user_input):
    current_q = st.session_state.current_question
    
    if current_q == "experience" and user_input == "0":
        return translate_text(
            "For candidates with no experience, please type 'fresher'. " + 
            QUESTIONS[current_q]["question"],
            LANGUAGES[st.session_state.selected_language]
        )
    
    is_valid, error_message = validate_input(current_q, user_input)
    
    if not is_valid:
        error_response = f"Invalid input: {error_message}\n\nPlease answer again: {QUESTIONS[current_q]['question']}"
        return translate_text(
            error_response,
            LANGUAGES[st.session_state.selected_language]
        )
    
    st.session_state.candidate_info[current_q] = user_input
    
    questions_list = list(QUESTIONS.keys())
    current_index = questions_list.index(current_q)
    
    if current_index + 1 < len(questions_list):
        st.session_state.current_question = questions_list[current_index + 1]
        next_question = QUESTIONS[questions_list[current_index + 1]]["question"]
        return translate_text(
            next_question,
            LANGUAGES[st.session_state.selected_language]
        )
    else:
        tech_stack = st.session_state.candidate_info["tech_stack"]
        st.session_state.tech_questions = generate_tech_questions(tech_stack)
        st.session_state.in_tech_assessment = True
        st.session_state.current_tech_question_index = 0
        
        intro_text = "Great! Now I'll ask you a few technical questions based on your tech stack.\n\n"
        first_question = st.session_state.tech_questions[0]
        
        return translate_text(
            intro_text + first_question,
            LANGUAGES[st.session_state.selected_language]
        )

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
        exit_message = "Thank you for your time. Feel free to come back when you're ready to continue the application process. Have a great day!"
        return translate_text(
            exit_message,
            LANGUAGES[st.session_state.selected_language]
        )
    
    if "technical_answers" not in st.session_state.candidate_info:
        st.session_state.candidate_info["technical_answers"] = {}
    
    current_question = st.session_state.tech_questions[st.session_state.current_tech_question_index]
    st.session_state.candidate_info["technical_answers"][current_question] = user_input
    
    st.session_state.current_tech_question_index += 1
    if st.session_state.current_tech_question_index < len(st.session_state.tech_questions):
        next_question = st.session_state.tech_questions[st.session_state.current_tech_question_index]
        return translate_text(
            next_question,
            LANGUAGES[st.session_state.selected_language]
        )
    else:
        filename = save_to_file(st.session_state.candidate_info)
        completion_message = f"Thank you for completing the technical assessment! Your details and answers have been saved to {filename}. Our recruitment team will review your profile and get back to you soon."
        return translate_text(
            completion_message,
            LANGUAGES[st.session_state.selected_language]
        )


# Streamlit UI
st.title("TalentScout Hiring Assistant")

# Language selector
st.sidebar.title("Language Settings")
selected_language = st.sidebar.selectbox(
    "Select Interview Language",
    options=list(LANGUAGES.keys()),
    index=list(LANGUAGES.keys()).index(st.session_state.selected_language)
)

# Update selected language in session state
if selected_language != st.session_state.selected_language:
    st.session_state.selected_language = selected_language
    st.experimental_rerun()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initial greeting (only show if no messages exist)
if len(st.session_state.messages) == 0:
    greeting = "Hello! I'm the TalentScout Hiring Assistant. I'll help you submit your application by asking a few questions. " + QUESTIONS["name"]["question"]
    translated_greeting = translate_text(
        greeting,
        LANGUAGES[st.session_state.selected_language]
    )
    with st.chat_message("assistant"):
        st.markdown(translated_greeting)
    st.session_state.messages.append({"role": "assistant", "content": translated_greeting})

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