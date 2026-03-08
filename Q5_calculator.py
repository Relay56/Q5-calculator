import tkinter as tk
import math
import random
from fractions import Fraction

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Q5 calculator")  # Изменено название
        self.root.resizable(True, True)
        self.root.minsize(500, 550)

        # Иконка (если есть)
        try:
            self.icon = tk.PhotoImage(file="Q5calc.png")
            self.root.iconphoto(False, self.icon)
        except:
            pass

        # Состояния
        self.dark_mode = False
        self.animating = False
        self.current_operator = ""
        self.first_number = None
        self.new_number = True
        self.memory = None
        self.history = []
        self.buttons = []

        # Поле ввода
        self.display = tk.Entry(
            self.root, font=("Arial", 24), justify="right",
            bd=10, width=25
        )
        self.display.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)

        # --- Строка 1: основные тригонометрические и корни ---
        row1 = [('sin', self.func_sin), ('cos', self.func_cos), ('tan', self.func_tan),
                ('√', self.func_sqrt), ('x²', self.func_square)]
        self._add_row(row1, 1)

        # --- Строка 2: обратные тригонометрические, константы, дроби ---
        row2 = [('asin', self.func_asin), ('acos', self.func_acos), ('atan', self.func_atan),
                ('π', self.const_pi), ('e', self.const_e), ('Frac', self.func_frac)]
        self._add_row(row2, 2)

        # --- Строка 3: новые математические функции ---
        row3 = [('log', self.func_log), ('ln', self.func_ln), ('x^y', self.func_pow),
                ('n!', self.func_fact), ('|x|', self.func_abs), ('mod', self.func_mod)]
        self._add_row(row3, 3)

        # --- Строка 4: цифры 1,2,3 и оператор '-' ---
        row4 = [('1', self.digit), ('2', self.digit), ('3', self.digit), ('-', self.operator)]
        self._add_row(row4, 4)

        # --- Строка 5: цифры 4,5,6 и оператор '*' ---
        row5 = [('4', self.digit), ('5', self.digit), ('6', self.digit), ('*', self.operator)]
        self._add_row(row5, 5)

        # --- Строка 6: цифры 7,8,9 и оператор '/' ---
        row6 = [('7', self.digit), ('8', self.digit), ('9', self.digit), ('/', self.operator)]
        self._add_row(row6, 6)

        # --- Строка 7: цифра 0, точка, C и оператор '+' ---
        row7 = [('0', self.digit), ('.', self.point), ('C', self.clear), ('+', self.operator)]
        self._add_row(row7, 7)

        # --- Строка 8: память и история ---
        row8 = [('MS', self.memory_store), ('MR', self.memory_recall),
                ('M+', self.memory_add), ('MC', self.memory_clear),
                ('Hist', self.show_history), ('Rand', self.func_rand)]
        self._add_row(row8, 8)

        # --- Строка 9: равно (5 колонок) и переключатель темы (1 колонка) ---
        self.equal_btn = tk.Button(self.root, text="=", font=("Arial", 14, "bold"),
                                   command=self.calculate)
        self.equal_btn.grid(row=9, column=0, columnspan=5, sticky="nsew", padx=1, pady=1)
        self.buttons.append(self.equal_btn)

        self.theme_btn = tk.Button(self.root, text="🌙 Тёмная", font=("Arial", 10),
                                   width=8, command=self.toggle_theme)
        self.theme_btn.grid(row=9, column=5, columnspan=1, sticky="nsew", padx=1, pady=1)
        self.buttons.append(self.theme_btn)

        # Настройка весов
        for i in range(6):
            self.root.columnconfigure(i, weight=1)
        for i in range(1, 10):
            self.root.rowconfigure(i, weight=1)

        # Цветовые темы
        self.light_theme = {
            'bg': "#f0f0f0", 'fg': "#000000", 'btn_bg': "#d9d9d9", 'btn_fg': "#000000",
            'entry_bg': "#ffffff", 'entry_fg': "#000000", 'theme_text': "🌙 Тёмная"
        }
        self.dark_theme = {
            'bg': "#2b2b2b", 'fg': "#ffffff", 'btn_bg': "#3c3c3c", 'btn_fg': "#ffffff",
            'entry_bg': "#1e1e1e", 'entry_fg': "#00ff00", 'theme_text': "☀️ Светлая"
        }

        self.apply_theme_instant(self.light_theme)

    def _add_row(self, buttons_data, row):
        for col, (text, cmd) in enumerate(buttons_data):
            btn = tk.Button(self.root, text=text, font=("Arial", 12),
                            command=lambda t=text, c=cmd: self.button_click(t, c))
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            self.buttons.append(btn)

    # ---------- Обработка нажатий (без звука) ----------
    def button_click(self, text, cmd):
        # Звук удалён по просьбе пользователя
        if cmd == self.digit:
            self.digit(text)
        elif cmd == self.operator:
            self.operator(text)
        elif cmd == self.point:
            self.point()
        elif cmd == self.clear:
            self.clear()
        elif cmd == self.calculate:
            self.calculate()
        else:
            cmd()

    # ---------- Работа с дисплеем ----------
    def get_display_value(self):
        text = self.display.get()
        try:
            if '/' in text:
                a, b = text.split('/')
                return float(a) / float(b)
            return float(text)
        except:
            raise ValueError

    def set_display(self, value):
        self.display.delete(0, tk.END)
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        self.display.insert(0, str(value))

    def digit(self, d):
        if self.new_number:
            self.display.delete(0, tk.END)
            self.new_number = False
        self.display.insert(tk.END, d)

    def point(self):
        if self.new_number:
            self.display.delete(0, tk.END)
            self.new_number = False
        if '.' not in self.display.get():
            self.display.insert(tk.END, '.')

    def clear(self):
        self.display.delete(0, tk.END)
        self.first_number = None
        self.current_operator = ""
        self.new_number = True

    # ---------- Бинарные операторы ----------
    def operator(self, op):
        try:
            self.first_number = self.get_display_value()
            self.current_operator = op
            self.new_number = True
        except:
            self.clear()

    def calculate(self):
        if self.first_number is None or self.current_operator == "":
            return
        try:
            second = self.get_display_value()
            res = None
            if self.current_operator == '+':
                res = self.first_number + second
            elif self.current_operator == '-':
                res = self.first_number - second
            elif self.current_operator == '*':
                res = self.first_number * second
            elif self.current_operator == '/':
                res = self.first_number / second if second != 0 else "Ошибка"
            elif self.current_operator == '^':
                res = self.first_number ** second
            elif self.current_operator == 'mod':
                res = self.first_number % second if second != 0 else "Ошибка"
            else:
                res = "Ошибка"

            self.set_display(res)
            expr = f"{self._format_number(self.first_number)} {self.current_operator} {self._format_number(second)} = {self.display.get()}"
            self.history.append(expr)
            if len(self.history) > 20:
                self.history.pop(0)

            self.first_number = None
            self.current_operator = ""
            self.new_number = True
        except:
            self.set_display("Ошибка")
            self.first_number = None
            self.current_operator = ""
            self.new_number = True

    def _format_number(self, num):
        if isinstance(num, float) and num.is_integer():
            return str(int(num))
        return str(num)

    # ---------- Унарные функции ----------
    def apply_unary(self, func, err="Ошибка"):
        try:
            val = self.get_display_value()
            res = func(val)
            self.set_display(res)
            self.first_number = None
            self.current_operator = ""
            self.new_number = True
        except:
            self.set_display(err)
            self.first_number = None
            self.current_operator = ""
            self.new_number = True

    def func_sin(self): self.apply_unary(math.sin)
    def func_cos(self): self.apply_unary(math.cos)
    def func_tan(self): self.apply_unary(math.tan)
    def func_asin(self): self.apply_unary(math.asin, "Ошибка (вне диапазона)")
    def func_acos(self): self.apply_unary(math.acos, "Ошибка (вне диапазона)")
    def func_atan(self): self.apply_unary(math.atan)
    def func_sqrt(self): self.apply_unary(math.sqrt, "Ошибка (отрицательное)")
    def func_square(self): self.apply_unary(lambda x: x**2)
    def func_log(self): self.apply_unary(math.log10, "Ошибка (<=0)")
    def func_ln(self): self.apply_unary(math.log, "Ошибка (<=0)")
    def func_pow(self):
        try:
            self.first_number = self.get_display_value()
            self.current_operator = '^'
            self.new_number = True
        except:
            self.clear()

    def func_fact(self):
        try:
            val = self.get_display_value()
            if val < 0 or not val.is_integer():
                self.set_display("Ошибка")
                return
            res = math.factorial(int(val))
            self.set_display(res)
            self.first_number = None
            self.current_operator = ""
            self.new_number = True
        except:
            self.set_display("Ошибка")
            self.first_number = None
            self.current_operator = ""
            self.new_number = True

    def func_abs(self): self.apply_unary(abs)
    def func_mod(self):
        try:
            self.first_number = self.get_display_value()
            self.current_operator = 'mod'
            self.new_number = True
        except:
            self.clear()

    def func_rand(self):
        self.set_display(random.random())
        self.new_number = True

    # Константы
    def const_pi(self):
        self.set_display(math.pi)
        self.new_number = True

    def const_e(self):
        self.set_display(math.e)
        self.new_number = True

    # Дроби
    def func_frac(self):
        try:
            val = self.get_display_value()
            frac = Fraction(val).limit_denominator(1000)
            self.display.delete(0, tk.END)
            self.display.insert(0, f"{frac.numerator}/{frac.denominator}")
            self.first_number = None
            self.current_operator = ""
            self.new_number = True
        except:
            self.set_display("Ошибка")
            self.first_number = None
            self.current_operator = ""
            self.new_number = True

    # ---------- Память ----------
    def memory_store(self):
        try:
            self.memory = self.get_display_value()
        except:
            pass

    def memory_recall(self):
        if self.memory is not None:
            self.set_display(self.memory)
            self.new_number = True

    def memory_add(self):
        try:
            self.memory = (self.memory or 0) + self.get_display_value()
        except:
            pass

    def memory_clear(self):
        self.memory = None

    # ---------- История ----------
    def show_history(self):
        """Открывает окно с историей вычислений"""
        hist_win = tk.Toplevel(self.root)
        hist_win.title("История")
        hist_win.geometry("300x400")
        hist_win.resizable(True, True)

        listbox = tk.Listbox(hist_win, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        for item in self.history:
            listbox.insert(tk.END, item)

        def on_double_click(event):
            selection = listbox.curselection()
            if selection:
                line = listbox.get(selection[0])
                if '=' in line:
                    result = line.split('=')[1].strip()
                    self.display.delete(0, tk.END)
                    self.display.insert(0, result)
                    self.new_number = True
                    hist_win.destroy()

        listbox.bind("<Double-Button-1>", on_double_click)

        clear_btn = tk.Button(hist_win, text="Очистить историю",
                              command=lambda: self.clear_history(listbox))
        clear_btn.pack(pady=5)

    def clear_history(self, listbox):
        self.history.clear()
        listbox.delete(0, tk.END)

    # ---------- Переключение темы (с анимацией) ----------
    def toggle_theme(self):
        if self.animating:
            return
        self.dark_mode = not self.dark_mode
        target = self.dark_theme if self.dark_mode else self.light_theme
        self.animate_theme(target, steps=10, interval=30)

    def animate_theme(self, target, steps, interval):
        self.animating = True
        start_bg = self.root.cget('bg')
        start_btn_bg = self.buttons[0].cget('bg')
        start_btn_fg = self.buttons[0].cget('fg')
        start_entry_bg = self.display.cget('bg')
        start_entry_fg = self.display.cget('fg')

        def interpolate(c1, c2, factor):
            r1, g1, b1 = int(c1[1:3],16), int(c1[3:5],16), int(c1[5:7],16)
            r2, g2, b2 = int(c2[1:3],16), int(c2[3:5],16), int(c2[5:7],16)
            r = int(r1 + (r2 - r1)*factor)
            g = int(g1 + (g2 - g1)*factor)
            b = int(b1 + (b2 - b1)*factor)
            return f"#{r:02x}{g:02x}{b:02x}"

        def step(s):
            if s > steps:
                self.apply_theme_instant(target)
                self.animating = False
                return
            f = s / steps
            bg = interpolate(start_bg, target['bg'], f)
            btn_bg = interpolate(start_btn_bg, target['btn_bg'], f)
            btn_fg = interpolate(start_btn_fg, target['btn_fg'], f)
            entry_bg = interpolate(start_entry_bg, target['entry_bg'], f)
            entry_fg = interpolate(start_entry_fg, target['entry_fg'], f)

            self.root.configure(bg=bg)
            for btn in self.buttons:
                btn.configure(bg=btn_bg, fg=btn_fg, activebackground=btn_bg, activeforeground=btn_fg)
            self.display.configure(bg=entry_bg, fg=entry_fg, insertbackground=target['fg'])

            self.root.after(interval, lambda: step(s+1))

        step(1)

    def apply_theme_instant(self, theme):
        self.root.configure(bg=theme['bg'])
        for btn in self.buttons:
            btn.configure(bg=theme['btn_bg'], fg=theme['btn_fg'],
                          activebackground=theme['btn_bg'], activeforeground=theme['btn_fg'])
        self.display.configure(bg=theme['entry_bg'], fg=theme['entry_fg'],
                               insertbackground=theme['fg'])
        self.theme_btn.config(text=theme['theme_text'])

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()