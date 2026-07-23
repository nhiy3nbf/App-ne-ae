from flask import Flask, render_template

app = Flask(__name__)


def get_asia_uni_grade_info(mark):
    """
    Converts a numerical grade (0-100) to Asia University's scale.
    """
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
        # Range 0 - 49
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

@app.route("/predict")
@app.route("/predict")
def predict():
    raw_semesters = [
        {
            "title": "Semester 1",
            "term": "FALL 2025",
            "status": "completed",
            "progress_percent": 100,
            "is_open": False,
            "courses": [
                {
                    "code": "Course 1", "mark": 90,
                    "assignments": [
                        {"title": "Assignment 1", "score": "30/100", "weight": "30%", "status": "completed"},
                        {"title": "Midterm Exam", "score": "25/100", "weight": "35%", "status": "completed"},
                        {"title": "Final Project", "score": "35/100", "weight": "35%", "status": "completed"}
                    ]
                },
                {
                    "code": "Course 2", "mark": 65,
                    "assignments": [
                        {"title": "Quiz 1", "score": "20/100", "weight": "20%", "status": "completed"},
                        {"title": "Midterm Exam", "score": "35/100", "weight": "40%", "status": "completed"},
                        {"title": "Final Exam", "score": "30/100", "weight": "40%", "status": "completed"}
                    ]
                },
                {
                    "code": "Course 3", "mark": 60,
                    "assignments": [
                        {"title": "Lab 1", "score": "40/100", "weight": "30%", "status": "completed"},
                        {"title": "Lab 2", "score": "20/100", "weight": "30%", "status": "completed"},
                        {"title": "Final Paper", "score": "30/100", "weight": "40%", "status": "completed"}
                    ]
                },
                {
                    "code": "Course 4", "mark": 50,
                    "assignments": [
                        {"title": "Quiz 1", "score": "85/100", "weight": "20%", "status": "completed"},
                        {"title": "Midterm Exam", "score": "78/100", "weight": "40%", "status": "completed"},
                        {"title": "Final Project", "score": "80/100", "weight": "40%", "status": "completed"}
                    ]
                },
                {
                    "code": "Course 5", "mark": 55,
                    "assignments": [
                        {"title": "Assignment 1", "score": "75/100", "weight": "30%", "status": "completed"},
                        {"title": "Assignment 2", "score": "68/100", "weight": "30%", "status": "completed"},
                        {"title": "Final Exam", "score": "70/100", "weight": "40%", "status": "completed"}
                    ]
                },
                {
                    "code": "Course 6", "mark": 10,
                    "assignments": [
                        {"title": "Project Phase 1", "score": "80/100", "weight": "30%", "status": "completed"},
                        {"title": "Project Phase 2", "score": "75/100", "weight": "30%", "status": "completed"},
                        {"title": "Final Presentation", "score": "80/100", "weight": "40%", "status": "completed"}
                    ]
                }
            ]
        },
        {
            "title": "Semester 2",
            "term": "SPRING 2026",
            "status": "pending",
            "progress_percent": 45,
            "is_open": False,
            "courses": [
                {
                    "code": "Course 1", "mark": 76,
                    "assignments": [
                        {"title": "Assignment 1", "score": "80/100", "weight": "25%", "status": "completed"},
                        {"title": "Midterm Exam", "score": "75/100", "weight": "35%", "status": "completed"},
                        {"title": "Final Project", "score": "--/100", "weight": "40%", "status": "pending"}
                    ]
                },
                {
                    "code": "Course 2", "mark": 90,
                    "assignments": [
                        {"title": "Quiz 1", "score": "95/100", "weight": "20%", "status": "completed"},
                        {"title": "Midterm Exam", "score": "88/100", "weight": "40%", "status": "completed"},
                        {"title": "Final Exam", "score": "--/100", "weight": "40%", "status": "pending"}
                    ]
                },
                {
                    "code": "Course 3", "mark": 90,
                    "assignments": [
                        {"title": "Lab 1", "score": "92/100", "weight": "30%", "status": "completed"},
                        {"title": "Lab 2", "score": "--/100", "weight": "30%", "status": "pending"},
                        {"title": "Final Paper", "score": "--/100", "weight": "40%", "status": "pending"}
                    ]
                },
                {
                    "code": "Course 4", "mark": 90,
                    "assignments": [
                        {"title": "Quiz 1", "score": "90/100", "weight": "20%", "status": "completed"},
                        {"title": "Midterm Exam", "score": "91/100", "weight": "40%", "status": "completed"},
                        {"title": "Final Project", "score": "--/100", "weight": "40%", "status": "pending"}
                    ]
                },
                {
                    "code": "Course 5", "mark": 97,
                    "assignments": [
                        {"title": "Assignment 1", "score": "98/100", "weight": "30%", "status": "completed"},
                        {"title": "Assignment 2", "score": "96/100", "weight": "30%", "status": "completed"},
                        {"title": "Final Exam", "score": "--/100", "weight": "40%", "status": "pending"}
                    ]
                },
                {
                    "code": "Course 6", "mark": 67,
                    "assignments": [
                        {"title": "Project Phase 1", "score": "70/100", "weight": "30%", "status": "completed"},
                        {"title": "Project Phase 2", "score": "--/100", "weight": "30%", "status": "pending"},
                        {"title": "Final Presentation", "score": "--/100", "weight": "40%", "status": "pending"}
                    ]
                }
            ]
        }
    ]

    total_points = 0
    total_courses = 0
    processed_semesters = []

    for sem in raw_semesters:
        sem_points = 0
        processed_courses = []

        for c in sem["courses"]:
            info = get_asia_uni_grade_info(c["mark"])
            
            sem_points += info["points"]
            total_points += info["points"]
            total_courses += 1

            processed_courses.append({
                "code": c["code"],
                "prediction": info["grade"].strip(),
                "progress": info["percent"],
                "color": info["color"],
                "pass_fail": info["status"],
                "assignments": c["assignments"] # Pass assignments through
            })

        sem_gpa = sem_points / len(sem["courses"]) if sem["courses"] else 0.0
        earned = sum(2.0 for c in processed_courses if c["pass_fail"] == "PASS")
        
        processed_semesters.append({
            "title": sem["title"],
            "term": sem["term"],
            "status": sem["status"],
            "progress_percent": sem["progress_percent"],
            "is_open": sem["is_open"],
            "units": len(sem["courses"]),
            "completed_count": len(sem["courses"]) if sem["status"] == "completed" else 2,
            "earned_credits": earned,
            "total_credits": len(sem["courses"]) * 2.0,
            "gpa": round(sem_gpa, 2),
            "gpa_color": get_color_by_gpa(sem_gpa),
            "course_rows": [processed_courses[i:i + 3] for i in range(0, len(processed_courses), 3)]
        })

    overall_gpa = total_points / total_courses if total_courses else 0.0
    overall_percent = (overall_gpa / 4.0) * 100

    data = {
        "overall_gpa": round(overall_gpa, 2),
        "overall_percent": round(overall_percent, 1),
        "overall_color": get_color_by_gpa(overall_gpa),
        "semesters": processed_semesters
    }

    return render_template("predict.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)