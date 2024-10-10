from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import database
from database import *

# Khởi tạo cửa sổ
win = Tk()
win.title("Quản Lý Sinh Viên")

# Tạo Notebook để chứa các tab
notebook = ttk.Notebook(win)
notebook.pack(pady=10, expand=True)

# Tạo tab chính
main_tab = Frame(notebook)
notebook.add(main_tab, text="Quản Lý Sinh Viên")

# Tạo tab mới
new_tab = Frame(notebook)
notebook.add(new_tab, text="Quản Lý Điểm")

# biến rõng lưu dũ liệu sinh viên
students = []#bao gồm tên, mssv, năm sinh
scores = {}# bao gôm tên sinh viên và điểm của sinh viên đó

# Hàm thêm sinh viên
def add_student():
    student_name = name_entry.get()
    student_id = id_entry.get()
    birth_year = birth_year_entry.get()
    
    if student_name and student_id and birth_year:
        # Thêm sinh viên vào PostgreSQL
        database.insert_student(student_name, student_id, birth_year)
        
        # Cập nhật danh sách hiển thị
        students = database.fetch_students()  # Lấy lại dữ liệu sau khi thêm
        update_student_list(students)
        
        name_entry.delete(0, END)
        id_entry.delete(0, END)
        birth_year_entry.delete(0, END)
    else:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")

# Hàm sửa sinh viên
def edit_student():
    selected_index = listbox.curselection()
    if selected_index:
        student_info = listbox.get(selected_index[0])
        student_id = student_info.split(' - ')[1]  # Lấy student_id từ danh sách đã hiển thị
        
        student_name = name_entry.get()
        birth_year = birth_year_entry.get()
        
        if student_name and student_id and birth_year:
            # Sửa thông tin sinh viên trong PostgreSQL
            database.update_student(student_id, student_name, birth_year)
            students = database.fetch_students()  # Lấy lại dữ liệu sau khi sửa
            update_student_list(students)
            name_entry.delete(0, END)
            id_entry.delete(0, END)
            birth_year_entry.delete(0, END)
        else:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để sửa")

# Hàm xóa sinh viên
def delete_student():
    selected_index = listbox.curselection()
    if selected_index:
        student_info = listbox.get(selected_index[0])
        student_id = student_info.split(' - ')[1]
        
        # Xóa sinh viên khỏi PostgreSQL
        database.delete_student(student_id)
        students = database.fetch_students()  # Lấy lại dữ liệu sau khi xóa
        update_student_list(students)
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để xóa")

# Hàm cập nhật danh sách sinh viên trong tab sinh viên
def update_student_list(students):
    listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox
    for student in students:
        student_info = f"{student[0]} - {student[1]} - {student[2]}"
        listbox.insert(END, student_info)
        
    student_listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox Điểm
    for student in students:
        student_info = f"{student[0]} - {student[1]} - {student[2]}"
        student_listbox.insert(END, student_info)

# Hàm nhập điểm cho sinh viên
def enter_scores():
    students = database.fetch_students()
    selected_index = student_listbox.curselection()
    
    if selected_index:
        student_index = selected_index[0]
        if student_index >= len(students):  # Kiểm tra chỉ số có hợp lệ không
            messagebox.showwarning("Thông báo", "Chỉ số sinh viên không hợp lệ.")
            return
        
        student_name = students[selected_index[0]][0]  # Lấy tên sinh viên
        student_id = students[selected_index[0]][1]    # Lấy mã số sinh viên
        math_score = math_entry.get()
        literature_score = literature_entry.get()
        english_score = english_entry.get()

        # Kiểm tra xem điểm có hợp lệ không
        try:
            math_score = float(math_score)
            literature_score = float(literature_score)
            english_score = float(english_score)
        except ValueError:
            messagebox.showwarning("Thông báo", "Vui lòng nhập điểm hợp lệ.")
            return

        # Nhập điểm vào cơ sở dữ liệu
        database.insert_scores(student_id, math_score, literature_score, english_score)

        # Cập nhật danh sách điểm trong Listbox
        update_student_scores_listbox()

        messagebox.showinfo("Thông báo", f"Điểm đã được nhập cho {student_name}!\nĐiểm: Toán: {math_score}, Văn: {literature_score}, Anh: {english_score}")
        # Xóa nội dung trong các Entry sau khi nhập điểm
        math_entry.delete(0, END)
        literature_entry.delete(0, END)
        english_entry.delete(0, END)
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để nhập điểm")

# Hàm cập nhật danh sách sinh viên và điểm của họ trong Listbox
def update_student_scores_listbox():
    # student_listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox
    for student in students:
        student_name = student[0]
        score_info = scores.get(student_name, {'Math': 0, 'Literature': 0, 'English': 0})
        total_score = sum(score_info.values())
        
        # Hiển thị tổng điểm và điểm từng môn
        student_listbox.insert(END, f"{student_name} - Tổng điểm: {total_score} - Toán: {score_info['Math']}, Văn: {score_info['Literature']}, Anh: {score_info['English']}")

def sort_by_scores():
    # Lấy điểm của tất cả sinh viên từ cơ sở dữ liệu
    scores_from_db = database.fetch_all_scores()  # Hàm này cần được viết trong file database.py

    # Sắp xếp sinh viên theo tổng điểm giảm dần
    sorted_students = sorted(scores_from_db.items(), key=lambda x: sum(x[1].values()), reverse=True)
    
    student_listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox
    for student in sorted_students:
        student_id = student[0]
        score_info = student[1]
        total_score = sum(score_info.values())
        student_listbox.insert(END, f"{student_id} - Tổng điểm: {total_score} - Toán: {score_info['Math']}, Văn: {score_info['Literature']}, Anh: {score_info['English']}")

def highest_score_by_subject():
    try:
        # Lấy dữ liệu điểm từ database
        scores_from_db = database.fetch_all_scores()

        # Tạo dictionary để lưu điểm cao nhất cho mỗi môn
        highest_scores = {
            'Math': None,
            'Literature': None,
            'English': None
        }

        # Lọc ra sinh viên có điểm cao nhất theo từng môn
        for student_name, score_info in scores_from_db.items():
            for subject, value in score_info.items():
                if subject in highest_scores:
                    if highest_scores[subject] is None or value > highest_scores[subject][1]:
                        highest_scores[subject] = (student_name, value)

        # Xóa nội dung trong Listbox trước khi hiển thị kết quả mới
        student_listbox.delete(0, END)

        # Hiển thị kết quả vào Listbox
        for subject, info in highest_scores.items():
            if info:
                student_listbox.insert(END, f"{subject}: {info[0]} - Điểm: {info[1]}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lấy dữ liệu: {e}")


def export_data():
    filename = "students_data.txt"  # Tên file xuất ra
    database.export_data_to_txt(students, scores, filename)

# Tạo Label tiêu đề cho tab quản lý sinh viên
title_label = Label(main_tab, text="ỨNG DỤNG QUẢN LÝ SINH VIÊN", fg="red", font="helvetica", width=30)
title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Tạo Listbox để hiển thị danh sách sinh viên
listbox = Listbox(main_tab, width=50, height=10)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Tạo Entry để nhập tên sinh viên
name_label = Label(main_tab, text="Nhập tên Sinh Viên:")
name_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

name_entry = Entry(main_tab, width=40)
name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Tạo Entry để nhập mã số sinh viên
id_label = Label(main_tab, text="Nhập mã số Sinh Viên:")
id_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

id_entry = Entry(main_tab, width=40)
id_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Tạo Entry để nhập năm sinh sinh viên
birth_year_label = Label(main_tab, text="Nhập năm sinh Sinh Viên:")
birth_year_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

birth_year_entry = Entry(main_tab, width=40)
birth_year_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Tạo các Button nằm ngang nhau trên cùng một dòng và có kích thước đồng đều
button_frame = Frame(main_tab)
button_frame.grid(row=5, column=0, columnspan=3, pady=10)

add_button = Button(button_frame, text="Thêm", command=add_student, width=10)
add_button.grid(row=0, column=0, padx=5)

edit_button = Button(button_frame, text="Sửa", command=edit_student, width=10)
edit_button.grid(row=0, column=1, padx=5)

delete_button = Button(button_frame, text="Xóa", command=delete_student, width=10)
delete_button.grid(row=0, column=2, padx=5)

# Cấu hình lưới để giãn nở Listbox
main_tab.grid_rowconfigure(1, weight=1)
main_tab.grid_columnconfigure(1, weight=1)

# Tab quản lý điểm
scores_title_label = Label(new_tab, text="QUẢN LÝ ĐIỂM SINH VIÊN", fg="blue", font="helvetica", width=30)
scores_title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

student_listbox = Listbox(new_tab, width=60, height=10)
student_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Tạo Label và Entry cho các môn học
math_label = Label(new_tab, text="Nhập điểm Toán:")
math_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

math_entry = Entry(new_tab, width=20)
math_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

literature_label = Label(new_tab, text="Nhập điểm Văn:")
literature_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

literature_entry = Entry(new_tab, width=20)
literature_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

english_label = Label(new_tab, text="Nhập điểm Anh:")
english_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

english_entry = Entry(new_tab, width=20)
english_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Tạo các Button nằm ngang nhau trên cùng một dòng và có kích thước đồng đều cho tab điểm
scores_button_frame = Frame(new_tab)
scores_button_frame.grid(row=5, column=0, columnspan=3, pady=10)

enter_scores_button = Button(scores_button_frame, text="Nhập Điểm", command=enter_scores, width=10)
enter_scores_button.grid(row=0, column=0, padx=5)

sort_scores_button = Button(scores_button_frame, text="Sắp Xếp Điểm", command=sort_by_scores, width=10)
sort_scores_button.grid(row=0, column=1, padx=5)

highest_score_button = Button(scores_button_frame, text="Điểm Cao Nhất", command=highest_score_by_subject, width=10)
highest_score_button.grid(row=0, column=2, padx=5)

export_button = Button(scores_button_frame, text="Xuất Dữ Liệu", command=export_data, width=20)
export_button.grid(row=0, column=3, padx=5)

# Cấu hình lưới để giãn nở Listbox
new_tab.grid_rowconfigure(1, weight=1)
new_tab.grid_columnconfigure(1, weight=1)

# Chạy ứng dụng
win.mainloop()
