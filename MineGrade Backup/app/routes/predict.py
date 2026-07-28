from flask import Blueprint, render_template, render_template_string, request, redirect, url_for, session
import re
from app.routes.AI import get_giga_steve_response
from app.models.student import get_student_by_user_id
from app.models.prediction import get_student_semesters_for_prediction

predict = Blueprint('predict', __name__)

DEFAULT_GREETING = [
    {"sender": "bot", "text": "Greetings, scholar. I am Giga-Steve. Need help improving your grades or understanding your subject predictions?"}
]

def update_assignment_statuses(semesters):
    """Automatically updates 'status' to completed/pending based on valid score."""
    for semester in semesters:
        for course in semester.get("courses", []):
            for assign in course.get("assignments", []):
                score = str(assign.get("score", "")).strip()
                score_match = re.match(r"^(\d+(\.\d+)?)\s*/\s*100$", score)
                if score_match:
                    assign["status"] = "completed"
                else:
                    assign["status"] = "pending"
    return semesters

def get_asia_uni_grade_info(mark):
    if mark >= 90:
        return {"grade": "A+", "points": 4.00, "percent": 100, "color": "green", "status": "PASS"}
    elif mark >= 85:
        return {"grade": "A",  "points": 3.75, "percent": 88,  "color": "green", "status": "PASS"}
    elif mark >= 80:
        return {"grade": "A-", "points": 3.50, "percent": 82,  "color": "green", "status": "PASS"}
    elif mark >= 75:
        return {"grade": "B+", "points": 3.25, "percent": 77,  "color": "yellow-green", "status": "PASS"}
    elif mark >= 70:
        return {"grade": "B",  "points": 3.00, "percent": 72,  "color": "yellow-green", "status": "PASS"}
    elif mark >= 65:
        return {"grade": "B-", "points": 2.75, "percent": 67,  "color": "yellow", "status": "PASS"}
    elif mark >= 60:
        return {"grade": "C+", "points": 2.50, "percent": 62,  "color": "yellow", "status": "PASS"}
    elif mark >= 55:
        return {"grade": "C",  "points": 2.25, "percent": 57,  "color": "orange", "status": "FAIL"}
    elif mark >= 50:
        return {"grade": "C-", "points": 2.00, "percent": 52,  "color": "orange", "status": "FAIL"}
    else:
        return {"grade": "F",  "points": 0.00, "percent": 15,  "color": "red", "status": "FAIL"}

def get_color_by_gpa(gpa_value):
    if gpa_value >= 3.25:
        return "green"
    elif gpa_value >= 2.50:
        return "yellow-green"
    elif gpa_value >= 2.25:
        return "yellow"
    elif gpa_value >= 2.00:
        return "orange"
    return "red"

def calculate_course_predicted_mark(course):
    completed_weight = 0.0
    earned_points = 0.0
    for assign in course.get("assignments", []):
        if assign.get("status") == "completed" and assign.get("score") != "--/100":
            weight = float(assign["weight"].replace("%", ""))
            score_match = re.match(r"(\d+(\.\d+)?)/100", assign["score"])
            if score_match:
                score = float(score_match.group(1))
                earned_points += (score * (weight / 100.0))
                completed_weight += weight
    if completed_weight > 0:
        return round((earned_points / completed_weight) * 100, 1)
    return 0.0

def calculate_semester_progress(courses):
    if not courses:
        return 0
    total_progress = 0.0
    for c in courses:
        completed_weight = 0.0
        for assign in c.get("assignments", []):
            if assign.get("status") == "completed":
                weight = float(assign.get("weight", "0%").replace("%", ""))
                completed_weight += weight
        total_progress += completed_weight
    return round(total_progress / len(courses))


@predict.route("/embed_chat", methods=["GET", "POST"])
def embed_chat():
    if "chat_history" not in session:
        session["chat_history"] = list(DEFAULT_GREETING)

    is_thinking = session.get("is_thinking", False)

    chat_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="{{ url_for('static', filename='predict.css') }}">
        {% if is_thinking %}
            <meta http-equiv="refresh" content="0;url=/generate_response">
        {% endif %}
        <style>
            html { scroll-behavior: smooth; }
            body { background: transparent; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }
            .chat-body { flex: 1; overflow-y: auto; padding: 10px; display: flex; flex-direction: column; gap: 8px; }
            .chat-footer { display: flex; gap: 6px; padding: 8px; background: #121212; border-top: 2px solid #535353; }
            #chat-input { flex: 1; background: #000; border: 2px solid #535353; color: #fff; padding: 6px; font-family: inherit; }
            .send-btn { background: #535353; border: 2px solid #aaa; color: #fff; padding: 6px 12px; cursor: pointer; font-family: inherit; }
            .send-btn:disabled { opacity: 0.5; cursor: not-allowed; }
            .thinking-bubble {
                font-style: italic;
                color: #888888;
                font-size: 0.9em;
                animation: pulse 1.2s infinite ease-in-out;
            }
            @keyframes pulse {
                0% { opacity: 0.3; }
                50% { opacity: 1.0; }
                100% { opacity: 0.3; }
            }
        </style>
    </head>
    <body>
        <div class="chat-body" id="chat-body">
            {% for msg in chat_history %}
                {% if msg.sender == "thinking" %}
                    <div class="chat-message bot-message thinking-bubble">
                        {{ msg.text }}
                    </div>
                {% else %}
                    <div class="chat-message {{ msg.sender }}-message">
                        {{ msg.text }}
                    </div>
                {% endif %}
            {% endfor %}
            <div id="bottom"></div>
        </div>
        <form class="chat-footer" action="/send_message" method="POST">
            <input type="text" id="chat-input" name="user_query" placeholder="Ask Steve..." required autocomplete="off" {% if is_thinking %}disabled{% endif %}>
            <button type="submit" class="send-btn" {% if is_thinking %}disabled{% endif %}>Send</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(chat_html, chat_history=session.get("chat_history", DEFAULT_GREETING), is_thinking=is_thinking)


@predict.route("/send_message", methods=["POST"])
def send_message():
    action = request.form.get("action")

    if action == "reset":
        session["chat_history"] = list(DEFAULT_GREETING)
        session["is_thinking"] = False
        session.modified = True
        return redirect(url_for("predict.embed_chat") + "#bottom")

    user_query = request.form.get("user_query", "").strip()
    if user_query:
        history = session.get("chat_history", list(DEFAULT_GREETING))
        history.append({"sender": "user", "text": user_query})
        history.append({"sender": "thinking", "text": "Giga-Steve is thinking..."})
        session["last_user_query"] = user_query
        session["chat_history"] = history
        session["is_thinking"] = True
        session.modified = True

    return redirect(url_for("predict.embed_chat") + "#bottom")


@predict.route("/generate_response", methods=["GET"])
def generate_response():
    if session.get("is_thinking"):
        history = session.get("chat_history", [])
        user_query = session.get("last_user_query", "")

        clean_history = [m for m in history if m["sender"] != "thinking"]

        # clean_history đã có sẵn câu hỏi mới nhất ở cuối -> bỏ ra trước khi truyền làm
        # "history", vì get_giga_steve_response tự gửi user_query riêng qua send_message()
        if clean_history and clean_history[-1]["sender"] == "user":
            prior_history = clean_history[:-1]
        else:
            prior_history = clean_history

        steve_reply = get_giga_steve_response(user_query, prior_history)

        if clean_history and clean_history[-1]["sender"] == "user":
            clean_history.append({"sender": "bot", "text": steve_reply})

        session["chat_history"] = clean_history
        session["is_thinking"] = False
        session.modified = True

    return redirect(url_for("predict.embed_chat") + "#bottom")


@predict.route("/predict", methods=["GET"])
def predict_page():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for('auth.login'))

    if "chat_history" not in session:
        session["chat_history"] = list(DEFAULT_GREETING)

    student = get_student_by_user_id(user_id)
    if not student:
        return render_template("predict.html", data=None, error="Student record not found.")

    raw_semesters = get_student_semesters_for_prediction(student["id"])
    if not raw_semesters:
        return render_template("predict.html", data=None, error="No enrollment data found yet.")

    raw_semesters = update_assignment_statuses(raw_semesters)

    total_points = 0.0
    total_percent_sum = 0.0
    total_courses = 0
    processed_semesters = []

    for sem in raw_semesters:
        sem_points = 0.0
        completed_courses_count = 0
        processed_courses = []

        calculated_progress = calculate_semester_progress(sem["courses"])
        sem_status = "completed" if calculated_progress >= 100 else "pending"

        for c in sem["courses"]:
            calculated_mark = calculate_course_predicted_mark(c)
            info = get_asia_uni_grade_info(calculated_mark)

            sem_points += info["points"]
            total_points += info["points"]
            total_percent_sum += info["percent"]
            total_courses += 1

            all_done = all(a.get("status") == "completed" for a in c.get("assignments", []))
            if all_done:
                completed_courses_count += 1

            processed_courses.append({
                "code": c["code"],
                "prediction": info["grade"],
                "progress": info["percent"],
                "color": info["color"],
                "pass_fail": info["status"],
                "assignments": c["assignments"]
            })

        sem_gpa = sem_points / len(sem["courses"]) if sem["courses"] else 0.0
        earned = sum(2.0 for c in processed_courses if c["pass_fail"] == "PASS")

        processed_semesters.append({
            "title": sem["title"],
            "term": sem["term"],
            "status": sem_status,
            "progress_percent": calculated_progress,
            "is_open": sem["is_open"],
            "units": len(sem["courses"]),
            "completed_count": completed_courses_count,
            "earned_credits": earned,
            "total_credits": len(sem["courses"]) * 2.0,
            "gpa": round(sem_gpa, 2),
            "gpa_color": get_color_by_gpa(sem_gpa),
            "course_rows": [processed_courses[i:i + 3] for i in range(0, len(processed_courses), 3)]
        })

    overall_gpa = total_points / total_courses if total_courses else 0.0
    overall_percent = total_percent_sum / total_courses if total_courses else 0.0

    data = {
        "overall_gpa": round(overall_gpa, 2),
        "overall_percent": round(overall_percent, 1),
        "overall_color": get_color_by_gpa(overall_gpa),
        "semesters": processed_semesters,
    }

    return render_template("predict.html", data=data)