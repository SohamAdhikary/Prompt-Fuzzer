import streamlit as st
import os
from dotenv import load_dotenv
from fuzzer import test_prompt  # Import your fuzzer function
import json
import pandas as pd

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

st.title("LLM Prompt Fuzzer")

# Sidebar for settings
with st.sidebar:
    st.header("Fuzzing Settings")
    prompt = st.text_area("Enter a prompt to fuzz:", value="Translate to German: Hello world!")
    num_tests = st.slider("Number of tests:", min_value=1, max_value=20, value=5) # Increased max_value
    display_format = st.radio("Display Format:", ["JSON", "Table"], index=1) # Added display format

if gemini_api_key:
    if st.button("Run Fuzzer"):
        if prompt:
            results = test_prompt(prompt, num_tests=num_tests)
            st.header("Fuzzing Results:")

            if display_format == "JSON":
                st.json(results)
            elif display_format == "Table":
                df = pd.DataFrame(results)
                st.dataframe(df)

            # --- Download Report ---
            report_filename = "fuzzing_report.json"
            json_report = json.dumps(results, indent=4)  # Pretty print JSON
            st.download_button(
                label="Download Report (JSON)",
                data=json_report.encode('utf-8'),
                file_name=report_filename,
                mime="application/json"
            )

        else:
            st.warning("Please enter a prompt.")
else:
    st.error("Error: Google API key not found. Make sure to configure it in Render's environment variables.")