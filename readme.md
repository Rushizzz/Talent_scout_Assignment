# TalentScout Hiring Assistant

This project is a web application designed to assist organizations in streamlining their hiring process by conducting automated interviews and gathering essential candidate information.

## Features
- **Multilingual Support**: Conduct interviews in various languages, including English, Hindi, Spanish, and more.
- **Automated Validation**: Validate user inputs like names, emails, phone numbers, and more using an LLM (Large Language Model).
- **Technical Assessment**: Generate and present technical questions based on the candidate's tech stack.
- **Session Persistence**: Maintain user session state for a seamless conversational flow.
- **File Saving**: Save candidate information and responses for future review.

## Tech Stack
- **Backend**: Streamlit
- **AI Model**: Groq LLM (using the `groq-gradio` library)
- **Translation**: Deep Translator (powered by Google Translator API)

## File Structure
1. **app.py**: The main application file containing the Streamlit interface, logic for input validation, and integration with the LLM and translator.
2. **Dockerfile**: Docker configuration for containerizing the application.
3. **requirements.txt**: List of Python dependencies required to run the application.

## Setup and Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies**:
   Make sure you have Python 3.7 or higher installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Execute the following command to start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. **Using Docker** (Optional):
   - Build the Docker image:
     ```bash
     docker build -t talentscout-app:v1.0 .
     ```
   - Run the container:
     ```bash
     docker run -e GROQ_API_KEY='your-api-key' -p 8501:8501 talentscout-app:v1.0 
     ```

## How It Works
1. The application starts by greeting the candidate and asking for their preferred language.
2. It collects basic information such as name, email, phone number, and tech stack, with real-time validation.
3. Based on the provided tech stack, the app generates five technical questions for assessment.
4. Candidate responses and information are saved to a timestamped file for further review.

## Dependencies
- **Streamlit**: For creating the interactive web application.
- **groq-gradio**: For integrating Groq LLM.
- **deep_translator**: For language translation.

## Environment Variables
To integrate this application into your environment, ensure you set the following variables:
- **API_KEY**: For the Groq LLM service.

## Contribution
Feel free to fork the repository, submit issues, or create pull requests to enhance the application.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

