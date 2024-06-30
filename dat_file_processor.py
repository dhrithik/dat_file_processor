import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from pathlib import Path


class DataProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAT FILE PROCESSOR")
        self.root.geometry("750x500")

        # Set custom icon (change 'icon.ico' to your icon file name)
        icon_path = os.path.join(os.path.dirname(__file__), 'data_analysis_icon_179855.ico')
        self.root.iconbitmap(icon_path)

        # Heading and subheading
        self.heading_label = tk.Label(self.root, text=".DAT FILE PROCESSOR", font=("Helvetica", 16, "bold"))
        self.heading_label.pack(pady=(20, 10))

        self.subheading_label = tk.Label(self.root, text="DUPLICATE ROW DELETER", font=("Helvetica", 16))
        self.subheading_label.pack(pady=(0, 20))

        # Frame for buttons and textboxes
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.frame.pack_propagate(0)  # Prevents the frame from resizing

        # Load folder widgets
        self.load_label = tk.Label(self.frame, text="Load a folder with .dat files:", font=("Helvetica", 12))
        self.load_label.grid(row=0, column=0, padx=10, pady=5)

        self.load_path_var = tk.StringVar()
        self.load_path_entry = tk.Entry(self.frame, textvariable=self.load_path_var, width=40, font=("Helvetica", 12))
        self.load_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.load_button = tk.Button(self.frame, text="Load Folder", command=self.load_folder, font=("Helvetica", 12))
        self.load_button.grid(row=0, column=2, padx=10, pady=5)

        # Save folder widgets
        self.save_label = tk.Label(self.frame, text="Save processed files to:", font=("Helvetica", 12))
        self.save_label.grid(row=1, column=0, padx=10, pady=5)

        self.save_path_var = tk.StringVar()
        self.save_path_entry = tk.Entry(self.frame, textvariable=self.save_path_var, width=40, font=("Helvetica", 12))
        self.save_path_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.save_button = tk.Button(self.frame, text="Select Folder", command=self.select_save_folder,
                                     font=("Helvetica", 12))
        self.save_button.grid(row=1, column=2, padx=10, pady=5)

        # Watermark label
        self.watermark_label = tk.Label(self.root, text="Made by Dhrithik Raj", font=("Helvetica", 10, "italic"))
        self.watermark_label.pack(side=tk.BOTTOM, anchor=tk.SW, padx=10, pady=(0, 10))

        # Update the window to calculate its dimensions
        self.root.update_idletasks()

        self.data = None

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_path_var.set(folder_path)
            self.process_files_in_folder(folder_path)

    def process_files_in_folder(self, folder_path):
        try:
            files = Path(folder_path).glob("*.dat")
            output_folder = self.save_path_var.get()
            if not output_folder:
                messagebox.showerror("Error", "Please select a folder to save processed files.")
                return

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for file_path in files:
                try:
                    self.data = pd.read_csv(file_path, delimiter=';')  # Adjust delimiter if necessary
                    self.data.drop_duplicates(inplace=True)

                    # Save processed file
                    save_file_name = f"processed_{file_path.name}"
                    save_path = os.path.join(output_folder, save_file_name)
                    self.data.to_csv(save_path, sep=';', index=False)  # Adjust delimiter if necessary
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process {file_path.name}: {e}")

            messagebox.showinfo("Success", "All files processed and saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process files: {e}")

    def select_save_folder(self):
        save_folder = filedialog.askdirectory()
        if save_folder:
            self.save_path_var.set(save_folder)

    def save_file(self):
        pass  # No need for individual file save, handled in process_files_in_folder


if __name__ == "__main__":
    root = tk.Tk()
    app = DataProcessorApp(root)
    root.mainloop()
