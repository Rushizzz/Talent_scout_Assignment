# TalentScout Hiring Assistant

## Project Overview
TalentScout is a multilingual hiring assistant chatbot built with Streamlit and Groq LLM. It automates the initial candidate screening process by conducting structured interviews in multiple languages and evaluating technical skills based on candidates' tech stacks.

## Installation Instructions
1. Install required dependencies:
```bash
pip install streamlit langchain-groq deep-translator
```

2. Set environment variables:
```bash
export GROQ_API_KEY=your_api_key
```

3. Run the application:
```bash
streamlit run app.py
```

## Docker Installation
1. Build image:
```bash
docker build -t talentscout .
```

2. Run the container:
```bash
docker run -p 8501:8501 -e GROQ_API_KEY=your_api_key talentscout
```


## Usage Guide
1. Select preferred interview language from the sidebar
2. Answer basic questions about:
   - Personal information (name, email, phone)
   - Professional details (experience, position, location)
   - Technical skills
3. Complete technical assessment based on provided tech stack
4. Responses are saved automatically in txt format

## Technical Details

### Libraries Used
- Streamlit: Web interface and session management
- Langchain-Groq: LLM integration using Llama-3.3-70b
- Deep-Translator: Multi-language support
- txt: Data persistence
- Datetime: Timestamp generation

### Architecture
- Session-based state management for conversation flow
- Two-phase interview process:
  1. Basic information gathering
  2. Dynamic technical assessment
- Input validation using LLM
- Real-time language translation
- File-based data storage

### Model Details
- Model: Llama-3.3-70b-versatile
- Temperature: 0.7 (balanced creativity and consistency)
- Validation and question generation handled by LLM

## Prompt Design
1. Input Validation:
   - Structured prompts with clear validation criteria
   - Binary valid/invalid responses
   - Error message generation

2. Technical Question Generation:
   - Tech stack-based dynamic prompts
   - Difficulty level distribution
   - Focus on practical knowledge

## Challenges & Solutions

1. HTTPS Certificate Implementation:
   - Challenge: Secure domain setup required for production
   - Solution: Implemented SSL certificate
   - Impact: Enhanced security for candidate data

2. Multi-language Support:
   - Challenge: Maintaining context across translations
   - Solution: Implemented bidirectional translation with English as base
   - Built-in fallback to English for failed translations

3. State Management:
   - Challenge: Maintaining conversation flow across translations
   - Solution: Streamlit session state with structured progression
   - Separate states for basic info and technical assessment

4. Error Handling:
   - Challenge: Graceful handling of invalid inputs
   - Solution: LLM-based validation with specific error messages
   - Translation of error messages to user's preferred language