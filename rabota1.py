import os
import zipfile
import tkinter as tk
from tkinter import scrolledtext
import yaml
import sys

class ShellEmulator:
    def __init__(self, config_file):
        # Загрузка конфигурации
        self.load_config(config_file)
        # Инициализация виртуальной файловой системы
        self.init_filesystem(self.config['filesystem'])
        self.history = []

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
        self.username = self.config['username']
        self.hostname = self.config['hostname']
    
    def init_filesystem(self, zip_path):
        self.fs = {}
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('/tmp/virtual_fs')
        self.current_dir = '/tmp/virtual_fs'
    
    def run_command(self, command):
        self.history.append(command)
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0]
        
        if cmd == 'ls':
            return self.ls_command()
        elif cmd == 'cd':
            return self.cd_command(parts[1] if len(parts) > 1 else None)
        elif cmd == 'exit':
            return "exit"  # Специальное значение для выхода
        elif cmd == 'head':
            return self.head_command(parts[1] if len(parts) > 1 else None)
        elif cmd == 'history':
            return self.history_command()
        else:
            return f"Command not found: {cmd}"

    def ls_command(self):
        return '\n'.join(os.listdir(self.current_dir))

    def cd_command(self, path):
        if not path:
            return "No directory specified."
        new_path = os.path.join(self.current_dir, path)
        if os.path.isdir(new_path):
            self.current_dir = new_path
            return f"Changed directory to {new_path}"
        else:
            return f"Directory not found: {path}"

    def head_command(self, filename):
        if not filename:
            return "No file specified."
        file_path = os.path.join(self.current_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return ''.join(file.readlines()[:10])
        else:
            return f"File not found: {filename}"

    def history_command(self):
        return '\n'.join(self.history)

class ShellGUI:
    def __init__(self, root, emulator):
        self.root = root
        self.root.title("Shell Emulator")
        self.emulator = emulator
        
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.output_area.pack(pady=10)
        
        self.input_field = tk.Entry(self.root, width=80)
        self.input_field.pack()
        self.input_field.bind("<Return>", self.enter_command)

        self.prompt = f"{self.emulator.username}@{self.emulator.hostname}:~$ "
        self.update_output(self.prompt)

    def enter_command(self, event):
        command = self.input_field.get()
        self.input_field.delete(0, tk.END)
        
        output = self.emulator.run_command(command)
        
        # Проверка на команду 'exit' для завершения работы
        if output == "exit":
            self.root.destroy()  # Закрытие окна и завершение программы
        else:
            self.update_output(f"{command}\n{output}\n{self.prompt}")

    def update_output(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    emulator = ShellEmulator('config.yaml')
    gui = ShellGUI(root, emulator)
    root.mainloop()
