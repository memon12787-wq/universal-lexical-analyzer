import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import re

# ---------- SAFE IMPORT ----------
try:
    from lexer import tokenize
except:
    def tokenize(code):
        return [("ID", word) for word in code.split()]

# ---------- MAIN WINDOW ----------
window = tk.Tk()
window.title("Lexical Analyzer IDE")
window.geometry("820x600")

# ---------- THEME ----------
current_theme = "dark"

def apply_theme():
    if current_theme == "dark":
        bg = "#1e1e2f"
        editor_bg = "#2d2d44"
        fg = "white"
    else:
        bg = "#ffffff"
        editor_bg = "#f5f5f5"
        fg = "black"

    window.configure(bg=bg)
    main_frame.configure(bg=bg)
    editor_frame.configure(bg=bg)
    btn_frame.configure(bg=bg)
    toolbar.configure(bg=bg)

    code_input.configure(bg=editor_bg, fg=fg, insertbackground=fg)
    token_output.configure(bg=editor_bg, fg=fg)
    line_numbers.configure(bg="#cccccc" if current_theme=="light" else "#2b2b3c",
                           fg="black" if current_theme=="light" else "#aaaaaa")

# ---------- TOOLBAR ----------
toolbar = tk.Frame(window, height=40)
toolbar.pack(fill="x")

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as f:
            code_input.delete("1.0", tk.END)
            code_input.insert(tk.END, f.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(code_input.get("1.0", tk.END))
        messagebox.showinfo("Saved", "File saved successfully!")

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()

tk.Button(toolbar, text="Open", command=open_file, width=8).pack(side="left", padx=2, pady=2)
tk.Button(toolbar, text="Save File", command=save_file, width=10).pack(side="left", padx=2)
tk.Button(toolbar, text="Analyze", command=lambda: analyze_code(), width=10).pack(side="left", padx=2)
tk.Button(toolbar, text="Clear", command=lambda: clear_all(), width=8).pack(side="left", padx=2)
tk.Button(toolbar, text="🌗 Toggle Theme", command=toggle_theme).pack(side="right", padx=5)

# ---------- MAIN FRAME ----------
main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True, padx=10)

# ---------- EDITOR ----------
editor_frame = tk.Frame(main_frame)
editor_frame.pack(fill="both", expand=True)

line_numbers = tk.Text(editor_frame, width=3, state="disabled", font=("Courier", 10))
line_numbers.pack(side="left", fill="y")

code_input = tk.Text(editor_frame, wrap="none", font=("Courier", 10), undo=True)
code_input.pack(side="left", fill="both", expand=True)

y_scroll = tk.Scrollbar(editor_frame, command=code_input.yview)
y_scroll.pack(side="right", fill="y")

x_scroll = tk.Scrollbar(main_frame, orient="horizontal", command=code_input.xview)
x_scroll.pack(fill="x")

code_input.config(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

# ---------- OUTPUT ----------
tk.Label(window, text="Tokens Output").pack()

token_output = scrolledtext.ScrolledText(window, height=8, font=("Courier", 10))
token_output.pack(fill="x", padx=10, pady=3)

# ---------- TOKEN COLORS ----------
token_output.tag_config("KEYWORD", foreground="blue")
token_output.tag_config("ID", foreground="black")
token_output.tag_config("NUMBER", foreground="green")
token_output.tag_config("STRING", foreground="orange")
token_output.tag_config("OP", foreground="red")
token_output.tag_config("SYMBOL", foreground="purple")
token_output.tag_config("UNKNOWN", foreground="brown")

# ---------- SYNTAX HIGHLIGHT ----------
keywords = ["if", "else", "for", "while", "int", "float", "return"]

def highlight_syntax():
    code = code_input.get("1.0", tk.END)

    code_input.tag_remove("kw", "1.0", tk.END)

    for kw in keywords:
        start = "1.0"
        while True:
            start = code_input.search(r'\b' + kw + r'\b', start, tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(kw)}c"
            code_input.tag_add("kw", start, end)
            start = end

code_input.tag_config("kw", foreground="blue")

# ---------- LINE NUMBERS ----------
def update_line_numbers():
    lines = code_input.get("1.0", "end-1c").split("\n")
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", tk.END)
    for i in range(1, len(lines) + 1):
        line_numbers.insert(tk.END, f"{i}\n")
    line_numbers.config(state="disabled")

def on_key_release(event=None):
    highlight_syntax()
    update_line_numbers()

code_input.bind("<KeyRelease>", on_key_release)

# ---------- FUNCTIONS ----------
def analyze_code():
    code = code_input.get("1.0", tk.END).rstrip()
    tokens = tokenize(code)
    token_output.delete("1.0", tk.END)

    for kind, value in tokens:
        token_output.insert(tk.END, f"{kind:10} : {value}\n", kind)

def clear_all():
    code_input.delete("1.0", tk.END)
    token_output.delete("1.0", tk.END)

# ---------- INIT ----------
btn_frame = tk.Frame(window)
btn_frame.pack()  # (kept minimal, toolbar is main control)

apply_theme()
update_line_numbers()

# ---------- RUN ----------
window.mainloop()