import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import sys

class PyToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Python to EXE Converter")
        self.root.geometry("600x400")
        
        # Variables
        self.file_path = tk.StringVar()
        self.onefile = tk.BooleanVar(value=True)
        self.console = tk.BooleanVar(value=False)
        self.icon_path = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # File selection
        tk.Label(self.root, text="Выберите Python файл:").pack(pady=5)
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=5, fill='x', padx=10)
        
        tk.Entry(file_frame, textvariable=self.file_path, width=50).pack(side='left', fill='x', expand=True)
        tk.Button(file_frame, text="Обзор", command=self.browse_file).pack(side='right', padx=5)
        
        # Options
        options_frame = tk.LabelFrame(self.root, text="Опции")
        options_frame.pack(pady=10, fill='x', padx=10)
        
        tk.Checkbutton(options_frame, text="Один файл", variable=self.onefile).pack(anchor='w', padx=5, pady=2)
        tk.Checkbutton(options_frame, text="Показывать консоль", variable=self.console).pack(anchor='w', padx=5, pady=2)
        
        # Icon selection
        icon_frame = tk.Frame(options_frame)
        icon_frame.pack(fill='x', pady=5)
        tk.Label(icon_frame, text="Иконка:").pack(side='left')
        tk.Entry(icon_frame, textvariable=self.icon_path, width=40).pack(side='left', fill='x', expand=True, padx=5)
        tk.Button(icon_frame, text="Выбрать", command=self.browse_icon).pack(side='right')
        
        # Convert button
        tk.Button(self.root, text="Конвертировать в EXE", command=self.convert, bg='green', fg='white').pack(pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill='x', padx=10, pady=5)
        
        # Log output
        self.log = tk.Text(self.root, height=10)
        self.log.pack(fill='both', expand=True, padx=10, pady=5)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if filename:
            self.file_path.set(filename)
    
    def browse_icon(self):
        filename = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if filename:
            self.icon_path.set(filename)
    
    def convert(self):
        if not self.file_path.get():
            messagebox.showerror("Ошибка", "Выберите Python файл!")
            return
        
        cmd = [
            'pyinstaller',
            '--onefile' if self.onefile.get() else '',
            '--console' if self.console.get() else '--noconsole',
            f'--icon={self.icon_path.get()}' if self.icon_path.get() else '',
            '--clean',
            self.file_path.get()
        ]
        
        # Remove empty arguments
        cmd = [arg for arg in cmd if arg]
        
        try:
            self.progress.start()
            self.log.delete(1.0, tk.END)
            self.log.insert(tk.END, f"Выполнение команды: {' '.join(cmd)}\n")
            self.root.update()
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=sys.stdout.encoding
            )
            
            for line in process.stdout:
                self.log.insert(tk.END, line)
                self.log.see(tk.END)
                self.root.update()
            
            process.wait()
            self.progress.stop()
            
            if process.returncode == 0:
                messagebox.showinfo("Успех", "Конвертация завершена успешно!")
            else:
                messagebox.showerror("Ошибка", "Произошла ошибка при конвертации")
                
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Ошибка", f"Исключение: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyToExeConverter(root)
    root.mainloop()