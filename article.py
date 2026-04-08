import streamlit as st
import fitz  # PyMuPDF
from groq import Groq
from PIL import Image

# Initialize the Groq client
client = Groq(api_key=st.secrets["Groq_API_KEY"])

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")  # Open PDF from file object
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def summarize_text(text):
    try:
        summary_response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text: {text}"
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return summary_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def ask_question(context, question):
    try:
        answer_response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": f"Context: {context} Question: {question}"
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return answer_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Article Summarizer")
#image = Image.open('ai.jpg')
#st.image(image, use_column_width='always')

# Upload the PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.subheader("Text Extracted from PDF:")
    st.write(pdf_text[:500])  # Display a snippet of the text for review

    # Summarize Text
    summary_button = st.button("Summarize Text")
    if summary_button:
        summary = summarize_text(pdf_text)
        st.subheader("Summary:")
        st.write(summary)

    # Ask a Question
    question = st.text_input("Ask a question about the PDF:")
    if question:
        answer = ask_question(pdf_text, question)
        st.subheader("Answer:")
        st.write(answer)
