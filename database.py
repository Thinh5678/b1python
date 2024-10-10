import psycopg2

# Kết nối tới cơ sở dữ liệu PostgreSQL
def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="student_db",  # Tên cơ sở dữ liệu
        user="postgres",  # Tên người dùng PostgreSQL
        password="1234"  # Mật khẩu người dùng PostgreSQL
    )
    return conn

# Hàm lấy danh sách sinh viên từ PostgreSQL
def fetch_students():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT name, student_id, birth_year FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

# Hàm thêm sinh viên vào PostgreSQL
def insert_student(name, student_id, birth_year):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, student_id, birth_year) VALUES (%s, %s, %s)",
                (name, student_id, birth_year))
    conn.commit()
    conn.close()

# Cập nhật thông tin sinh viên vào PostgreSQL
def update_student(student_id, name, birth_year):
    """Sửa thông tin sinh viên"""
    conn = connect()
    cur = conn.cursor()
    query = "UPDATE students SET name = %s, birth_year = %s WHERE student_id = %s"
    cur.execute(query, (name, birth_year, student_id))
    conn.commit()
    cur.close()
    conn.close()

# Hàm xóa sinh viên từ PostgreSQL
def delete_student(student_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    conn.commit()
    conn.close()
    
# Hàm nhập điểm cho sinh viên
def insert_scores(student_id, math_score, literature_score, english_score):
    conn = connect()
    cursor = conn.cursor()
    
    try:
        # Thêm điểm cho sinh viên
        cursor.execute('''
            INSERT INTO scores (student_id, math_score, literature_score, english_score)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (student_id) DO UPDATE SET
            math_score = EXCLUDED.math_score,
            literature_score = EXCLUDED.literature_score,
            english_score = EXCLUDED.english_score
        ''', (student_id, math_score, literature_score, english_score))
        
        conn.commit()
    except Exception as e:
        print("Lỗi khi nhập điểm:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Hàm lấy danh sách điểm sinh viên
def fetch_all_scores():
    try:
        conn = connect()
        cursor = conn.cursor()

        # Truy vấn lấy tất cả điểm sinh viên
        cursor.execute("SELECT student_id, math_score, literature_score, english_score FROM scores")
        rows = cursor.fetchall()

        scores = {}
        for row in rows:
            student_id = row[0]
            scores[student_id] = {
                'Math': row[1],
                'Literature': row[2],
                'English': row[3]
            }

        cursor.close()
        conn.close()
        return scores
    except Exception as e:
        print(f"Lỗi khi lấy điểm: {e}")
        return {}

# Hàm xuất dữ liệu sinh viên và điểm từ PostgreSQL
def export_data_to_txt(students, scores, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for student in students:
            student_name = student[0]
            student_id = student[1]
            birth_year = student[2]
            score_info = scores.get(student_name, {'Math': 0, 'Literature': 0, 'English': 0})

            file.write(f"Tên: {student_name}, Mã số: {student_id}, Năm sinh: {birth_year}, "
                       f"Điểm Toán: {score_info['Math']}, Điểm Văn: {score_info['Literature']}, "
                       f"Điểm Anh: {score_info['English']}\n")

    print(f"Dữ liệu đã được xuất ra file {filename}.")
