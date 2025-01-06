import streamlit as st
from langchain_groq import ChatGroq
import magic
import pdfplumber
import docx2txt
import markdown
import os

# Set up the Streamlit app
st.title("Resume Parser and Chatbot")

# Initialize Groq API key
# st.secrets["GROQ_API_KEY"] = st.text_input("Enter your Groq API Key", type="password")

# File uploader component
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

# Initialize the LangChain Groq model
llm = ChatGroq(   model_name="llama-3.3-70b-versatile",   temperature=0.7 )

# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    file_type = magic.from_buffer(uploaded_file.read(1024), mime=True)
    uploaded_file.seek(0)  # Reset file pointer
    
    if file_type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = " ".join([page.extract_text() for page in pdf.pages])
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = docx2txt.process(uploaded_file)
    else:
        st.error("Unsupported file type")
        return None
    
    return resume_text

# Function to extract resume information
def extract_resume_info(resume_text):
    prompt = f"""
    Extract the following structured information from the resume:
    - Name
    - Address
    - Skills (as a list)
    - Work Experience (detailed)
    - Education (detailed)

    Resume Text:
    {resume_text}
    """
    
    response = llm.invoke(prompt)
    return response.content

# Main application logic
if uploaded_file is not None:
    # Extract text from uploaded file
    resume_text = extract_text_from_file(uploaded_file)
    
    if resume_text:
        # Extract resume information
        extracted_info = extract_resume_info(resume_text)
        
        # Display extracted information
        st.markdown("## Extracted Resume Information")
        st.write(extracted_info)
        
        # Chat input component
        chat_input = st.text_input("Chat about your resume")
        
        if chat_input:
            # Chat functionality
            chat_prompt = f"""
            Context: {extracted_info}
            
            User Query: {chat_input}
            
            Provide a helpful and professional response related to the resume or job search.
            """
            
            chat_response = llm.invoke(chat_prompt)
            st.write("**Model Response:**", chat_response.content)
        
        # Download button
        if st.button("Download Extracted Information"):
            # Create markdown file
            md_content = f"""# Resume Information

{extracted_info}
"""
            st.download_button(
                label="Download Resume Info",
                data=md_content,
                file_name="resume_info.md",
                mime="text/markdown"
            )

# Add some styling and instructions
st.sidebar.markdown("""
### Instructions
1. Upload a PDF or DOCX resume
3. View extracted resume information
4. Chat about your resume
5. Download extracted info if needed
""")
