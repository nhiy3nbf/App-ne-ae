import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Tính đường dẫn .env tuyệt đối theo vị trí thật của file này,
# không phụ thuộc vào thư mục đang đứng khi chạy lệnh
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # app/models
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))      # lên 2 cấp -> gốc project
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6Kc8-BJcQQk_tWKZpEJ2frEd6Qbl-OD9DnP6WIQb8dN0w"))

MODEL_NAME = "gemini-3.6-flash"
# ... phần còn lại giữ nguyên y hệt bản trước, không đổi gì thêm

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
    """
    chat_history: các lượt hội thoại TRƯỚC ĐÓ, KHÔNG bao gồm user_text hiện tại.
    """
    try:
        history = [
            types.Content(
                role="user" if msg["sender"] == "user" else "model",
                parts=[types.Part.from_text(text=msg["text"])]
            )
            for msg in (chat_history or [])
        ]

        chat = client.chats.create(
            model=MODEL_NAME,
            history=history,
            config=types.GenerateContentConfig(
                system_instruction=GIGA_STEVE_SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=600,
            )
        )

        response = chat.send_message(user_text)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini API Error details: {e}")
        return "A true scholar stays focused despite technical glitches. (AI service temporarily unavailable)."