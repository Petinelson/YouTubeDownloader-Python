import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry("450x250")
        self.root.resizable(False, False)

        self.title_label = tk.Label(root, text="Youtube - Download", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.link_frame = tk.Frame(root)
        self.link_frame.pack(pady=5, anchor="w", padx=20)

        self.link_label = tk.Label(self.link_frame, text="Link:", font=("Helvetica", 12))
        self.link_label.pack(side=tk.LEFT, padx=5)

        self.link_entry = tk.Entry(self.link_frame, width=50)
        self.link_entry.pack(side=tk.LEFT, padx=5)

        self.option_frame = tk.Frame(root)
        self.option_frame.pack(pady=5, anchor="w", padx=20)

        self.option_label = tk.Label(self.option_frame, text="Selecione a opção:", font=("Helvetica", 12))
        self.option_label.pack(side=tk.LEFT, padx=5)

        self.option_var = tk.StringVar()
        self.option_menu = ttk.OptionMenu(self.option_frame, self.option_var, "Audio mp3", "Audio mp3", "Video mp4")
        self.option_menu.pack(side=tk.LEFT, padx=5)

        self.folder_frame = tk.Frame(root)
        self.folder_frame.pack(pady=5, anchor="w", padx=20)

        self.folder_button = tk.Button(self.folder_frame, text="Escolher", command=self.choose_folder)
        self.folder_button.pack(side=tk.LEFT, padx=5)

        self.folder_path = tk.StringVar()
        self.folder_path.set("Pasta de Download")

        self.folder_label = tk.Label(self.folder_frame, textvariable=self.folder_path, font=("Helvetica", 10))
        self.folder_label.pack(side=tk.LEFT, padx=5)

        self.download_button = tk.Button(root, text="BAIXAR", command=self.download, bg="#add8e6", fg="black",
                                         font=("Helvetica", 12), relief="flat")
        self.download_button.pack(pady=20)
        self.download_button.config(width=15, height=2)

    def choose_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)

    def download(self):
        link = self.link_entry.get()
        option = self.option_var.get()
        folder = self.folder_path.get()

        if not link:
            self.show_message("Insira um link válido!")
            return

        if not os.path.exists(folder):
            self.show_message("Selecione uma pasta de download válida!")
            return

        try:
            yt = YouTube(link)
            if option == "Audio mp3":
                stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
                filename = stream.download(folder)
                os.rename(filename, filename[:-4] + ".mp3")
            else:
                stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
                filename = stream.download(folder)

            self.show_message(f"Download completo: {filename}")
        except Exception as e:
            self.show_message(f"Erro ao fazer o download: {str(e)}")

    def show_message(self, message):
        messagebox.showinfo("Mensagem", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
