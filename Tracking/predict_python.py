from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def prediction():
    # Chunking the courses into groups of 3 to match the UI row design
    student_data = {
        "grade": "A+",
        "time": "12:33",
        "course_rows": [
            # Row 1: Max 3 items
            [
                {"code": "COD-3341", "prediction": "A+", "progress": 90, "status": "enchanted"},
                {"code": "COD-358", "prediction": "A+", "progress": 85, "status": "normal"},
                {"code": "COD-376", "prediction": "D", "progress": 25, "status": "normal"}
            ],
            # Row 2: Remaining items
            [
                {"code": "COD-437", "prediction": "A", "progress": 75, "status": "enchanted"},
                {"code": "COD-494", "prediction": "C", "progress": 50, "status": "normal"}
            ]
        ]
    }

    return render_template(
        "predict_html.html",
        data=student_data
    )

if __name__ == "__main__":
    app.run(debug=True)