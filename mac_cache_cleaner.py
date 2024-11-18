import tkinter as tk
from tkinter import messagebox
import os
import shutil
from pathlib import Path
import webbrowser
import subprocess

class SystemCleaner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MacOS Caches Cleaner ver1.00")

        window_width = 400
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True)

        self.cleanup_button = tk.Button(
            button_frame,
            text="キャッシュを全て削除",
            command=self.confirm_cleanup,
            width=20,
            height=2,
            bg='red',
            fg='white'
        )
        self.cleanup_button.pack(pady=10)

        # self.github_button = tk.Button(
        #     button_frame,
        #     text="GitHub",
        #     command=self.open_github,
        #     width=20,
        #     height=2,
        #     bg='#333333',
        #     fg='white'
        # )
        # self.github_button.pack(pady=10)

    def open_github(self):
        webbrowser.open('https://github.com')

    def confirm_cleanup(self):
        result = messagebox.askokcancel("警告", 
            "重要な警告\n\n"
            "システムのキャッシュとログを削除しようとしています。\n"
            "この操作は取り消すことができません！\n\n"
            "続行しますか？",
            icon='warning')
        
        if result:
            self.cleanup_system()

    def restart_mac(self):
        subprocess.call(['osascript', '-e', 'tell app "System Events" to restart'])

    def cleanup_system(self):
        home = str(Path.home())
        cleanup_paths = [
            f"{home}/Library/Caches/",
            f"{home}/Library/Containers/",
            f"{home}/Library/Logs/",
            f"{home}/Library/Cookies/"
        ]

        cleaned = 0
        errors = 0

        for path in cleanup_paths:
            if os.path.exists(path):
                try:
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        try:
                            if os.path.isfile(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            cleaned += 1
                        except (PermissionError, OSError):
                            errors += 1
                except (PermissionError, OSError):
                    errors += 1

        message = f"クリーンアップ完了 \n\n削除されたアイテム: {cleaned}"
        if errors > 0:
            message += f"\n スキップされたアイテム: {errors}"
        
        messagebox.showinfo("完了", message, icon='warning')

        if messagebox.askyesno("再起動の確認",
            "クリーンアップが完了しました。\n"
            "変更を適用するためにMacを再起動しますか？",
            icon='warning'):
            self.restart_mac()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SystemCleaner()
    app.run()