import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    raise EnvironmentError("The GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  #  <--  REPLACE 'gemini-pro' WITH THE CORRECT MODEL NAME!

def get_llm_response(prompt):
    try:
        response = model.generate_content(
            prompt,
            safety_settings={
                'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',  # Avoid false safety triggers
            },
            generation_config={
                'max_output_tokens': 500,  # Prevent cutoffs
                'temperature': 0.9  # Encourage creative failures
            }
        )
        return response.text if response and hasattr(response, 'text') else "ERROR: Empty response"
    except Exception as e:
        return f"API_ERROR: {str(e)}"  # Debuggable errors

if __name__ == "__main__":
    test_prompt = "What is the capital of France?"
    output = get_llm_response(test_prompt)
    if output:
        print(f"Test prompt: {test_prompt}")
        print(f"Gemini response: {output}")
    else:
        print("Failed to get a response from Gemini.")