import tkinter as tk
from tkinter import ttk
import math
import cmath
from tkinter import messagebox

class AdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Máy tính khoa học nâng cao")
        self.root.geometry("600x500")
        
        # Biến lưu trạng thái
        self.is_radian = tk.BooleanVar(value=True)  # Mặc định sử dụng radian
        self.memory = 0  # Bộ nhớ
        
        # Frame chính
        main_frame = ttk.Frame(root)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Màn hình hiển thị
        self.display = ttk.Entry(main_frame, width=40, justify="right", font=('Arial', 14))
        self.display.grid(row=0, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        # Màn hình phụ hiển thị lịch sử
        self.history_display = tk.Text(main_frame, height=3, width=40, font=('Arial', 10))
        self.history_display.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="ew")
        
        # Frame cho các nút radio và checkbox
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=2, column=0, columnspan=6, pady=5)
        
        # Radio buttons cho Rad/Deg
        ttk.Radiobutton(options_frame, text="Radian", variable=self.is_radian, value=True).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(options_frame, text="Degree", variable=self.is_radian, value=False).pack(side=tk.LEFT, padx=5)
        
        # Các nút chức năng
        buttons = [
            # Hàng 1: Chức năng bộ nhớ và đặc biệt
            ('MC', 3, 0, self.memory_clear), ('MR', 3, 1, self.memory_recall),
            ('M+', 3, 2, self.memory_add), ('M-', 3, 3, self.memory_subtract),
            ('π', 3, 4, lambda: self.add_to_display('3.14159')), ('e', 3, 5, lambda: self.add_to_display('2.71828')),
            
            # Hàng 2: Hàm lượng giác
            ('sin', 4, 0, lambda: self.add_to_display('sin(')), 
            ('cos', 4, 1, lambda: self.add_to_display('cos(')),
            ('tan', 4, 2, lambda: self.add_to_display('tan(')),
            ('asin', 4, 3, lambda: self.add_to_display('asin(')),
            ('acos', 4, 4, lambda: self.add_to_display('acos(')),
            ('atan', 4, 5, lambda: self.add_to_display('atan(')),
            
            # Hàng 3: Các hàm khác
            ('log', 5, 0, lambda: self.add_to_display('log(')),
            ('ln', 5, 1, lambda: self.add_to_display('ln(')),
            ('√', 5, 2, lambda: self.add_to_display('sqrt(')),
            ('x²', 5, 3, lambda: self.add_to_display('^2')),
            ('xʸ', 5, 4, lambda: self.add_to_display('^')),
            ('1/x', 5, 5, self.reciprocal),
            
            # Hàng 4-7: Số và phép tính cơ bản
            ('7', 6, 0), ('8', 6, 1), ('9', 6, 2), ('/', 6, 3), ('(', 6, 4), (')', 6, 5),
            ('4', 7, 0), ('5', 7, 1), ('6', 7, 2), ('*', 7, 3), ('j', 7, 4), ('|x|', 7, 5),
            ('1', 8, 0), ('2', 8, 1), ('3', 8, 2), ('-', 8, 3), ('n!', 8, 4), ('±', 8, 5),
            ('0', 9, 0), ('.', 9, 1), ('=', 9, 2), ('+', 9, 3), ('C', 9, 4), ('⌫', 9, 5),
        ]
        
        # Tạo các nút
        for btn_text, row, col, *args in buttons:
            if args:
                cmd = args[0]
            else:
                cmd = lambda x=btn_text: self.add_to_display(x)
            
            btn = ttk.Button(main_frame, text=btn_text, command=cmd)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Cấu hình grid
        for i in range(10):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            main_frame.grid_columnconfigure(i, weight=1)
    
    def add_to_display(self, value):
        if value == '=':
            self.calculate()
        elif value == 'C':
            self.display.delete(0, tk.END)
            self.history_display.delete(1.0, tk.END)
        elif value == '⌫':
            current = self.display.get()
            self.display.delete(len(current)-1, tk.END)
        else:
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current + str(value))
    
    def calculate(self):
        try:
            expr = self.display.get()
            # Lưu biểu thức vào lịch sử
            self.history_display.insert(tk.END, expr + '\n')
            
            # Xử lý các hàm đặc biệt
            expr = self.preprocess_expression(expr)
            
            # Tính toán
            result = eval(expr)
            
            # Định dạng kết quả
            if isinstance(result, complex):
                formatted_result = f"{result.real:.6g} + {result.imag:.6g}j"
            else:
                formatted_result = f"{result:.6g}"
            
            # Hiển thị kết quả
            self.display.delete(0, tk.END)
            self.display.insert(0, formatted_result)
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
            self.display.delete(0, tk.END)
    
    def preprocess_expression(self, expr):
        # Chuyển đổi độ sang radian nếu cần
        if not self.is_radian.get():
            expr = expr.replace('sin(', 'sin(math.radians(')
            expr = expr.replace('cos(', 'cos(math.radians(')
            expr = expr.replace('tan(', 'tan(math.radians(')
        
        # Thay thế các hàm toán học
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('asin', 'math.asin')
        expr = expr.replace('acos', 'math.acos')
        expr = expr.replace('atan', 'math.atan')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('ln', 'math.log')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('^', '**')
        
        return expr
    
    # Các hàm xử lý bộ nhớ
    def memory_clear(self):
        self.memory = 0
        
    def memory_recall(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, str(self.memory))
        
    def memory_add(self):
        try:
            value = eval(self.display.get())
            self.memory += value
        except:
            messagebox.showerror("Lỗi", "Giá trị không hợp lệ")
            
    def memory_subtract(self):
        try:
            value = eval(self.display.get())
            self.memory -= value
        except:
            messagebox.showerror("Lỗi", "Giá trị không hợp lệ")
    
    def reciprocal(self):
        try:
            value = eval(self.display.get())
            result = 1 / value
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
        except:
            messagebox.showerror("Lỗi", "Không thể tính nghịch đảo")

def main():
    root = tk.Tk()
    app = AdvancedCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()