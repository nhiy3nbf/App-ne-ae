from flask import Flask, render_template
import json

app = Flask(__name__)

def calculate_grade(percent):
    if percent is None:
        return 'N/A', '#888888'
    if percent >= 90:
        return 'A+', '#55ff55'
    elif percent >= 80:
        return 'A', '#55ff55'
    elif percent >= 70:
        return 'B', '#ffff55'
    elif percent >= 60:
        return 'C', '#ffaa00'
    else:
        return 'F', '#ff5555'

def get_grade_color(percent):
    if percent > 80:
        return '#55ff55'  # Green (>80%)
    elif percent > 70:
        return '#99ff33'  # Yellow-Green (>70%)
    elif percent > 60:
        return '#ffff55'  # Yellow (>60%)
    else:
        return '#ff5555'  # Red (<60%)

def get_gpa_color(gpa):
    if gpa > 3.0:
        return '#55ff55'  # Green (>3.0)
    elif gpa < 2.5:
        return '#ff5555'  # Red (<2.5)
    else:
        return '#ffffff'  # Default white (2.5 to 3.0)

@app.route('/')
def courses():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        # 1. Map top scores per course across ALL students in data.json
        course_max_scores = {}
        
        for student_entry in data:
            for student_id, student_info in student_entry.get('student_id', {}).items():
                for sem_key in ['semester 1', 'semester 2']:
                    scores = student_info.get(sem_key, {}).get('score_course', {})
                    for course_code, score_data in scores.items():
                        valid_scores = [v for v in score_data.values() if v is not None]
                        if valid_scores:
                            avg_score = round(sum(valid_scores) / len(valid_scores), 2)
                            if course_code not in course_max_scores or avg_score > course_max_scores[course_code]:
                                course_max_scores[course_code] = avg_score

        # 2. Process active student (1A)
        student_data = data[0]['student_id']['1A']
        
        semesters = {}
        all_percentages = []
        achievements_list = []
        
        sem_meta = {
            'semester 1': {'title': 'Semester 1', 'subtitle': 'FALL 2025'},
            'semester 2': {'title': 'Semester 2', 'subtitle': 'WINTER 2026'}
        }
        
        for sem_key, meta in sem_meta.items():
            if sem_key in student_data:
                sem_courses = []
                scores = student_data[sem_key].get('score_course', {})
                attendance = student_data[sem_key].get('attendance_course', {})
                
                sem_percentages = []
                completed_count = 0
                earned_credits = 0.0
                
                for course_code, score_data in scores.items():
                    valid_scores = [v for k, v in score_data.items() if v is not None]
                    if valid_scores:
                        percent = round(sum(valid_scores) / len(valid_scores), 2)
                        sem_percentages.append(percent)
                        all_percentages.append(percent)
                        completed_count += 1
                        earned_credits += 2.0
                        
                        # Achievement Criteria: Top Scorer AND > 85%
                        highest_score = course_max_scores.get(course_code, 0)
                        if percent > 85 and percent >= highest_score:
                            achievements_list.append({
                                'course': course_code,
                                'score': percent,
                                'title': f"Top Scorer in {course_code}"
                            })
                    else:
                        percent = 0
                    
                    grade_letter, color = calculate_grade(percent if valid_scores else None)
                    course_att = attendance.get(course_code, {})
                    total_sessions = len(course_att)
                    attended = sum(1 for status in course_att.values() if status is True)
                    
                    sem_courses.append({
                        'code': course_code,
                        'percent': percent,
                        'grade': grade_letter,
                        'color': color,
                        'attended': attended,
                        'total_sessions': total_sessions
                    })
                
                sem_avg = sum(sem_percentages) / len(sem_percentages) if sem_percentages else 0
                sem_gpa = round((sem_avg / 100) * 4.0, 2)
                sem_progress = int((completed_count / len(scores)) * 100) if scores else 0
                
                semesters[meta['title']] = {
                    'subtitle': meta['subtitle'],
                    'units': len(scores),
                    'progress': sem_progress,
                    'status_text': f"{sem_progress}% complete" if sem_progress == 100 else f"{sem_progress}% in progress",
                    'status_color': '#55ff55' if sem_progress == 100 else '#ffaa00',
                    'completed': completed_count,
                    'earned_credits': earned_credits,
                    'total_credits': len(scores) * 2.0,
                    'sem_gpa': sem_gpa,
                    'courses': sem_courses
                }
        
        avg_grade = round(sum(all_percentages) / len(all_percentages), 2) if all_percentages else 0
        gpa = round((avg_grade / 100) * 4.0, 2)
        
        results = {
            'avg_grade': avg_grade,
            'avg_grade_color': get_grade_color(avg_grade),
            'gpa': gpa,
            'gpa_color': get_gpa_color(gpa),
            'achievements_count': len(achievements_list),
            'achievements': achievements_list,
            'semesters': semesters
        }
        
        return render_template('course.html', results=results)
        
    except FileNotFoundError:
        return render_template('course.html', error="File data.json not found.")
    except Exception as e:
        return render_template('course.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)