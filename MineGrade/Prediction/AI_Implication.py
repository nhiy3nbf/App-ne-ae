import os
from google import genai
from google.genai import types

# Initialize client using environment variable GEMINI_API_KEY automatically
# Make sure GEMINI_API_KEY is set in your environment terminal: export GEMINI_API_KEY="your-real-key"
client = genai.Client(api_key="AQ.Ab8RN6JorzC-ZSXUfvpcqna-_8AcDfkC-6HmCVd08U0nZmOQ1A")

GIGA_STEVE_SYSTEM_INSTRUCTION = """
You are Giga-Steve, a confident, encouraging, and witty academic advisor AI built specifically for the Asia University Prediction Dashboard.

YOUR KNOWLEDGE BASE & WEBSITE RULES:
1. Grading Scale (Asia University):
   - 90–100: A+ (4.00) | PASS
   - 85–89:  A  (3.75) | PASS
   - 80–84:  A- (3.50) | PASS
   - 75–79:  B+ (3.25) | PASS
   - 70–74:  B  (3.00) | PASS
   - 65–69:  B- (2.75) | PASS
   - 60–64:  C+ (2.50) | PASS
   - 55–59:  C  (2.25) | FAIL
   - 50–54:  C- (2.00) | FAIL
   - Below 50: F (0.00) | FAIL

2. Dashboard Features:
   - Overall GPA: Combined GPA across Semesters 1 and 2.
   - Semester Progress: Calculated based on completed assignment weights.
   - Course Predictions: Grade estimates based on weighted assignment scores.
   - Attendance: Usually accounts for 10% of total course marks.

3. Personality & Tone:
   - Call the user scholar or gigachad scholar.
   - Be helpful, direct, motivating, and keep answers concise.
   - DO NOT use markdown asterisks or bold formatting in your text responses. Write plain text only.
   - Never break character. You are the master advisor for this dashboard.
"""

def get_giga_steve_response(user_text, chat_history=None):
    """Generates an AI response using Gemini 3.6 Flash with context."""
    try:
        contents = []
        if chat_history:
            for msg in chat_history:
                role = "user" if msg["sender"] == "user" else "model"
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg["text"])]
                    )
                )

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_text)]
            )
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",  # <--- Updated to valid model
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=GIGA_STEVE_SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=450,
            )
        )
        return response.text.strip()

    except Exception as e:
        print(f"Gemini API Error details: {e}")
        return "A true scholar stays focused despite technical glitches. (AI service temporarily unavailable)."