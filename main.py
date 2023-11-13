import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileSorterRenamer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('File Sorter and Renamer')
        self.geometry('600x450')

        self.create_widgets()

    def create_widgets(self):
        # Directory Frame
        self.dir_frame = ttk.Frame(self)
        self.dir_frame.pack(pady=20)

        self.dir_label = ttk.Label(self.dir_frame, text='Select Directory:')
        self.dir_label.pack(side='left', padx=(0, 10))

        self.dir_entry = ttk.Entry(self.dir_frame, width=50)
        self.dir_entry.pack(side='left')

        self.dir_button = ttk.Button(self.dir_frame, text='Browse', command=self.browse_directory)
        self.dir_button.pack(side='left')

        # Listbox Frame
        self.listbox_frame = ttk.Frame(self)
        self.listbox_frame.pack()

        self.listbox = tk.Listbox(self.listbox_frame, width=50, height=15, selectmode='extended')
        self.listbox.pack(side='left', padx=(0, 10))

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient='vertical', command=self.listbox.yview)
        self.scrollbar.pack(side='left', fill='y')

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Sort Buttons Frame
        self.sort_buttons_frame = ttk.Frame(self)
        self.sort_buttons_frame.pack(pady=10)

        self.up_button = ttk.Button(self.sort_buttons_frame, text='Move Up', command=self.move_up)
        self.up_button.pack(side='left', padx=(0, 10))

        self.down_button = ttk.Button(self.sort_buttons_frame, text='Move Down', command=self.move_down)
        self.down_button.pack(side='left')

        # Rename Frame
        self.rename_frame = ttk.Frame(self)
        self.rename_frame.pack(pady=20)

        self.prefix_label = ttk.Label(self.rename_frame, text='Prefix:')
        self.prefix_label.grid(row=0, column=0, sticky='e')

        self.prefix_entry = ttk.Entry(self.rename_frame)
        self.prefix_entry.grid(row=0, column=1)

        self.suffix_label = ttk.Label(self.rename_frame, text='Suffix:')
        self.suffix_label.grid(row=1, column=0, sticky='e')

        self.suffix_entry = ttk.Entry(self.rename_frame)
        self.suffix_entry.grid(row=1, column=1)

        self.startnum_label = ttk.Label(self.rename_frame, text='Start Number:')
        self.startnum_label.grid(row=2, column=0, sticky='e')

        self.startnum_entry = ttk.Entry(self.rename_frame)
        self.startnum_entry.grid(row=2, column=1)

        self.rename_button = ttk.Button(self.rename_frame, text='Rename Files', command=self.rename_files)
        self.rename_button.grid(row=3, column=0, columnspan=2)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
            self.populate_listbox(directory)

    def populate_listbox(self, directory):
        self.listbox.delete(0, tk.END)
        try:
            for filename in sorted(os.listdir(directory), key=str.lower):
                self.listbox.insert(tk.END, filename)
        except FileNotFoundError:
            messagebox.showerror('Error', 'Directory not found.')

    def move_up(self):
        selected_indices = self.listbox.curselection()
        for i in selected_indices:
            if i > 0:
                self.listbox.insert(i - 1, self.listbox.get(i))
                self.listbox.delete(i + 1)
                self.listbox.selection_set(i - 1)

    def move_down(self):
        selected_indices = self.listbox.curselection()
        for i in reversed(selected_indices):
            if i < self.listbox.size() - 1:
                self.listbox.insert(i + 2, self.listbox.get(i))
                self.listbox.delete(i)
                self.listbox.selection_set(i + 1)

    def rename_files(self):
        directory = self.dir_entry.get()
        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()
        try:
            start_num = int(self.startnum_entry.get())
        except ValueError:
            messagebox.showerror('Error', 'Start Number must be an integer.')
            return

        for i in range(self.listbox.size()):
            old_name = self.listbox.get(i)
            name, ext = os.path.splitext(old_name)
            new_name = f"{prefix}{start_num + i:02d}{suffix}{ext}"

            try:
                os.rename(os.path.join(directory, old_name), os.path.join(directory, new_name))
                self.listbox.delete(i)
                self.listbox.insert(i, new_name)
            except FileNotFoundError:
                messagebox.showerror('Error', f'File not found: {old_name}')
            except FileExistsError:
                messagebox.showerror('Error', f'File already exists: {new_name}')

        messagebox.showinfo('Success', 'Files have been renamed.')

if __name__ == "__main__":
    app = FileSorterRenamer()
    app.mainloop()
