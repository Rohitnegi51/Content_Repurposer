import streamlit as st
import os
from markitdown import MarkItDown
from google import genai

from dotenv import load_dotenv

# ==========================================
# 1. SETUP & AUTHENTICATION
# ==========================================
# Load the secret key from the .env file
load_dotenv()
client = genai.Client()

# ==========================================
# 2. STREAMLIT UI DESIGN
# ==========================================
st.set_page_config(page_title="AI Content Repurposer", page_icon="🚀", layout="centered")
st.title("🚀 AI Marketing Content Repurposer")
st.markdown("Upload a lengthy industry report (PDF, PPTX, DOCX) and instantly generate social media assets to automate your marketing workflow.")

# The file upload widget
uploaded_file = st.file_uploader("Upload your document here:", type=["pdf", "pptx", "docx"])

# ==========================================
# 3. CORE LOGIC (When a file is uploaded)
# ==========================================
if uploaded_file is not None:
    
    # NEW: Create a submit button
    if st.button("✨ Generate Marketing Assets"):
        
        # NEW: Add a loading spinner while the app works!
        with st.spinner("Analyzing document and generating AI content... Please wait."):
            
            # --- A. Save the uploaded file temporarily ---
            temp_file_extension = os.path.splitext(uploaded_file.name)[1]
            temp_file_path = f"temp_document{temp_file_extension}"
            
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # --- B. Extract Text using MarkItDown ---
            try:
                md = MarkItDown()
                extracted_data = md.convert(temp_file_path)
                document_text = extracted_data.text_content
                
                os.remove(temp_file_path)
                
                # --- C. The AI Prompt ---
                prompt = f"""
                You are an expert Social Media Manager and Content Marketer. 
                Read the following document text and generate the following:
                
                1. A short Executive Summary (3-4 sentences outlining the main takeaways).
                2. An engaging LinkedIn Post summarizing the key insights, formatted professionally with line breaks and appropriate emojis.
                3. A catchy Instagram Caption designed to drive engagement, including 5-7 highly relevant hashtags.
                
                Document Text:
                {document_text}
                """
                
                # --- D. Call the Gemini API ---
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                # --- E. Display the Results on the UI ---
                st.success("Done! Here are your assets:")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)