import customtkinter as ctk
import math
import time

# --- Konfigurasi Styling (Futuristik Neon Dark Mode) ---
BG_COLOR = "#0A0A0A"        
DISPLAY_BG = "#1A1A1A"      
ACCENT_COLOR = "#00FFC0"    
BUTTON_DEFAULT_COLOR = "#222222" 
BUTTON_OPERATOR_COLOR = "#331133" 
BUTTON_EQUAL_COLOR = "#007A5A"    
TEXT_COLOR = "#FFFFFF"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NeonInteractiveCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Kalkulator Sederhana")
        self.geometry("380x580")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)

        self.expression = "0"
        self.input_text = ctk.StringVar(value="0")
        self.clear_on_next_input = True 
        self.button_widgets = {} 
        
        self.create_widgets()

    def create_widgets(self):
        # --- 1. Display (Output) ---
        display_frame = ctk.CTkFrame(self, fg_color=DISPLAY_BG)
        display_frame.pack(fill='x', padx=0, pady=0)
        
        # Area display utama (dengan font futuristik)
        self.input_label = ctk.CTkLabel(
            display_frame, 
            textvariable=self.input_text, 
            font=("Consolas", 48, "bold"), 
            text_color=TEXT_COLOR,
            anchor='e',
            padx=15,
            height=100
        )
        self.input_label.pack(fill='x', expand=True, pady=(20, 5))

        # --- 2. Tombol Memori dan Mode (Dipertahankan seperti contoh Windows) ---
        top_utility_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        top_utility_frame.pack(fill='x', padx=0, pady=(5, 0))
        top_utility_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        utility_buttons = ["MC", "MR", "M+", "M-", "MS", "Mv"]
        for i, text in enumerate(utility_buttons):
             btn = ctk.CTkButton(top_utility_frame, text=text, command=lambda t=text: self.mem_utility_click(t),
                                fg_color="transparent", hover_color="#1A1A1A", text_color="#555555", font=("Segoe UI", 12), height=30)
             btn.grid(row=0, column=i, sticky="nsew", padx=0, pady=0)


        # --- 3. Grid Tombol Utama ---
        buttons_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        buttons_frame.pack(fill='both', expand=True, padx=0, pady=0)
        buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        buttons_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Definisi Tombol (Baris, Kolom, Teks, Tipe)
        buttons_layout = [
            (0, 0, "%", 'utility'), (0, 1, "CE", 'utility'), (0, 2, "C", 'utility'), (0, 3, "⌫", 'utility'),
            (1, 0, "1/x", 'utility'), (1, 1, "x²", 'utility'), (1, 2, "²√x", 'utility'), (1, 3, "÷", 'operator'),
            (2, 0, "7", 'number'), (2, 1, "8", 'number'), (2, 2, "9", 'number'), (2, 3, "×", 'operator'),
            (3, 0, "4", 'number'), (3, 1, "5", 'number'), (3, 2, "6", 'number'), (3, 3, "-", 'operator'),
            (4, 0, "1", 'number'), (4, 1, "2", 'number'), (4, 2, "3", 'number'), (4, 3, "+", 'operator'),
            (5, 0, "±", 'utility'), (5, 1, "0", 'number'), (5, 2, ".", 'number'), (5, 3, "=", 'equal')
        ]
        
        for r, c, text, btn_type in buttons_layout:
            
            fg, hover = self.get_button_colors(btn_type)
            
            btn = ctk.CTkButton(
                buttons_frame, 
                text=text, 
                command=lambda t=text, b_w=fg, h_w=hover: self.animate_button_click(t, b_w, h_w), 
                height=65, 
                font=("Segoe UI", 16, "bold"),
                fg_color=fg,
                hover_color=hover,
                text_color=TEXT_COLOR,
                corner_radius=0
            )
            btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
            self.button_widgets[text] = (btn, fg, hover) 


    # --- Styling dan Animasi ---

    def get_button_colors(self, type_key):
        # Skema Warna Futuristik
        if type_key == 'number':
            return BUTTON_DEFAULT_COLOR, "#3A3A3A"
        elif type_key == 'operator':
            return BUTTON_OPERATOR_COLOR, "#4A224A"
        elif type_key == 'utility':
            return BUTTON_DEFAULT_COLOR, "#3A3A3A"
        elif type_key == 'equal':
            return BUTTON_EQUAL_COLOR, "#008F6B"
        return BUTTON_DEFAULT_COLOR, "#3A3A3A"

    def animate_button_click(self, text, original_fg, original_hover):
        btn_data = self.button_widgets.get(text)
        if not btn_data: return

        btn, _, _ = btn_data
        
        # 1. Efek 'Glow' Saat Diklik
        glow_color = ACCENT_COLOR if text != "=" else "#FFFFFF"
        
        # Simpan warna asli sebelum diubah
        btn.configure(fg_color=glow_color, text_color=BG_COLOR) 
        
        # Jalankan aksi yang sebenarnya
        self.button_click(text)
        
        # 2. Kembalikan warna setelah jeda (Animasi)
        self.after(100, lambda: btn.configure(fg_color=original_fg, text_color=TEXT_COLOR)) 


    # --- Fungsi Kalkulator (Inti Logika) ---
    
    def update_display(self):
        self.input_text.set(self.expression)

    def handle_number_input(self, key):
        if "Error" in self.expression:
            self.expression = "0"
            
        if self.expression == "0" or self.clear_on_next_input:
            if key == '.':
                self.expression = "0."
            else:
                self.expression = key
            self.clear_on_next_input = False
        elif key == '.':
            # Hindari dua titik dalam satu angka
            if '.' not in self.expression.split(' ')[-1]:
                self.expression += key
        else:
            self.expression += key
            
    def handle_operator(self, key):
        if self.clear_on_next_input and len(self.expression) > 0 and self.expression != "Error":
             self.clear_on_next_input = False
             self.expression = self.expression.split(' ')[-1] 
             self.expression += f" {key} "
        elif self.expression[-1].isdigit() or self.expression.endswith(('.', ')')):
            self.expression += f" {key} "
        elif self.expression[-2:] in ("+ ", "- ", "× ", "÷ "):
            # Ganti operator sebelumnya
            self.expression = self.expression[:-3] + f" {key} "
        
    def backspace(self):
        if self.expression in ("0", "Error") or self.clear_on_next_input:
            return
            
        if self.expression.endswith(" "): 
            self.expression = self.expression[:-3]
        else:
            self.expression = self.expression[:-1]
            
        if not self.expression or self.expression == " ":
            self.expression = "0"
            self.clear_on_next_input = True

    def clear_all(self):
        self.expression = "0"
        self.clear_on_next_input = True
        
    def change_sign(self):
        if self.expression == "0" or "Error" in self.expression:
            return
        
        try:
            parts = self.expression.split()
            last_val = float(parts[-1])
            parts[-1] = str(-last_val)
            self.expression = " ".join(parts)
        except ValueError:
            pass 

    def calculate_result(self):
        if self.clear_on_next_input or "Error" in self.expression:
            return
            
        try:
            safe_exp = self.expression.replace('×', '*').replace('÷', '/')
            result = eval(safe_exp)
            
            if result == int(result):
                result = int(result)
            
            self.expression = str(result)
            self.clear_on_next_input = True
            
        except ZeroDivisionError:
            self.expression = "Tidak bisa membagi dengan nol"
            self.clear_on_next_input = True
        except Exception:
            self.expression = "Error Sintaks"
            self.clear_on_next_input = True

    def handle_single_arg_func(self, func):
        if self.clear_on_next_input or "Error" in self.expression:
            return
            
        try:
            # Ambil nilai terakhir (setelah operator terakhir)
            val = float(self.expression.split()[-1])
            
            if func == "x²":
                result = val ** 2
            elif func == "²√x":
                if val < 0:
                     self.expression = "Input tidak valid (Akar Negatif)"
                     self.clear_on_next_input = True
                     return
                result = math.sqrt(val)
            elif func == "1/x":
                if val == 0:
                    self.expression = "Tidak bisa membagi dengan nol"
                    self.clear_on_next_input = True
                    return
                result = 1 / val
            elif func == "%":
                # Operasi persen (dibagi 100)
                result = val / 100
            else:
                return

            if result == int(result):
                result = int(result)
                
            # Ganti nilai terakhir dalam ekspresi
            parts = self.expression.split()[:-1]
            self.expression = " ".join(parts + [str(result)])

            self.clear_on_next_input = False
            
        except Exception:
            self.expression = "Error"
            self.clear_on_next_input = True

    # Fungsi dummy untuk tombol memori
    def mem_utility_click(self, key):
         self.expression = f"'{key}' belum diimplementasikan"
         self.update_display()
         self.clear_on_next_input = True
         
    # Fungsi penghubung untuk aksi tombol
    def button_click(self, key):
        if key.isdigit() or key == '.':
            self.handle_number_input(key)
        elif key in ("+", "-", "×", "÷"):
            self.handle_operator(key)
        elif key == "=":
            self.calculate_result()
        elif key == "C" or key == "CE": 
            self.clear_all()
        elif key == "⌫": 
            self.backspace()
        elif key == "±": 
            self.change_sign()
        elif key in ("1/x", "x²", "²√x", "%"):
            self.handle_single_arg_func(key)
            
        self.update_display()


if __name__ == "__main__":
    app = NeonInteractiveCalculator()
    app.mainloop()