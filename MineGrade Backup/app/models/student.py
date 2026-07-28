from app.models.set_up import get_connection


def get_student_by_user_id(user_id):
    """Lấy thông tin students (không kèm email), dùng cho dashboard."""
    conn = get_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return student


def get_student_profile_by_user_id(user_id):
    """Lấy thông tin students KÈM email (join users), dùng riêng cho trang Profile."""
    conn = get_connection()
    student = conn.execute("""
        SELECT s.*, u.email
        FROM students s
        JOIN users u ON s.user_id = u.id
        WHERE s.user_id = ?
    """, (user_id,)).fetchone()
    conn.close()
    return student


def update_student_avt(user_id, fullname=None, skin_name=None):
    """Cập nhật tên + avatar Minecraft skin (dùng ở dashboard modal Customize)."""
    conn = get_connection()
    if fullname:
        conn.execute("UPDATE students SET fullname = ? WHERE user_id = ?", (fullname, user_id))
    if skin_name:
        avatar_url = f"https://mc-heads.net/avatar/{skin_name}"
        conn.execute("UPDATE students SET avatar = ? WHERE user_id = ?", (avatar_url, user_id))
    conn.commit()
    conn.close()


def update_student_info(user_id, data):
    """Cập nhật toàn bộ thông tin cá nhân ở trang Profile."""
    conn = get_connection()

    conn.execute("""
        UPDATE students SET
            fullname = ?,
            student_id = ?,
            date_of_birth = ?,
            national_id = ?,
            gender = ?,
            nationality = ?,
            phone_number = ?,
            address = ?
        WHERE user_id = ?
    """, (
        data.get('fullname'),
        data.get('student_id'),
        data.get('date_of_birth'),
        data.get('national_id'),
        data.get('gender'),
        data.get('nationality'),
        data.get('phone_number'),
        data.get('address'),
        user_id
    ))

    if data.get('email'):
        conn.execute(
            "UPDATE users SET email = ? WHERE id = ?",
            (data.get('email'), user_id)
        )

    conn.commit()
    conn.close()
