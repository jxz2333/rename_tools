import os
import tkinter as tk
from tkinter import filedialog
from tkinter import Scrollbar

class BatchRenameApp:
    def __init__(self, master):
        self.master = master
        master.title("批量重命名工具")

        # 初始化文件列表
        self.file_list = []

        # 创建控件
        self.label = tk.Label(master, text="选择文件夹:")
        self.label.pack()

        self.browse_button = tk.Button(master, text="浏览", command=self.browse_folder)
        self.browse_button.pack()

        self.listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, width=40, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = Scrollbar(master, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.sort_button = tk.Button(master, text="排序文件", command=self.sort_files)
        self.sort_button.pack()

        self.prefix_label = tk.Label(master, text="前缀:")
        self.prefix_label.pack()
        self.prefix_entry = tk.Entry(master)
        self.prefix_entry.pack()

        self.suffix_label = tk.Label(master, text="后缀:")
        self.suffix_label.pack()
        self.suffix_entry = tk.Entry(master)
        self.suffix_entry.pack()

        self.rename_button = tk.Button(master, text="批量重命名", command=self.batch_rename)
        self.rename_button.pack()

        self.quit_button = tk.Button(master, text="退出", command=master.quit)
        self.quit_button.pack()

        # 绑定拖放事件
        self.listbox.bind('<Button-1>', self.on_click)
        self.listbox.bind('<B1-Motion>', self.on_drag)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.file_list = [os.path.join(folder_selected, file) for file in os.listdir(folder_selected) if os.path.isfile(os.path.join(folder_selected, file))]
            print("选择的文件夹:", folder_selected)
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file_path in self.file_list:
            self.listbox.insert(tk.END, os.path.basename(file_path))

    def sort_files(self):
        self.file_list.sort()
        self.update_listbox()

    def on_click(self, event):
        # 获取被点击的文件项
        selected_index = self.listbox.nearest(event.y)
        self.drag_data = {'x': event.x, 'y': event.y, 'index': selected_index}

    def on_drag(self, event):
        # 拖动文件项
        x, y, index = event.x, event.y, self.listbox.nearest(event.y)
        self.listbox.yview_scroll(int((self.drag_data['y'] - y) / 15), tk.UNITS)  # 滚动
        self.listbox.after(100, lambda: self.listbox.yview(tk.MOVETO, int((self.drag_data['y'] - y) / 15)))  # 解决滚动卡顿的问题
        self.listbox.yview(tk.SCROLL, int((self.drag_data['y'] - y) / 15), tk.UNITS)  # 更新视图
        self.listbox.delete(self.drag_data['index'])  # 删除之前的位置
        self.listbox.insert(index, os.path.basename(self.file_list[self.drag_data['index']]))  # 插入新的位置
        # 更新文件列表的顺序
        self.file_list.insert(index, self.file_list.pop(self.drag_data['index']))

    def batch_rename(self):
        if not self.file_list:
            print("请先选择文件夹.")
            return

        prefix = self.prefix_entry.get()
        suffix = self.suffix_entry.get()

        for index, file_path in enumerate(self.file_list, 1):
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))
            new_name = f"{prefix}{str(index).zfill(2)}{suffix}{file_extension}"
            new_path = os.path.join(os.path.dirname(file_path), new_name)
            os.rename(file_path, new_path)

        print("批量重命名完成.")
        self.file_list = []  # 清空文件列表
        self.update_listbox()

# 创建主窗口
root = tk.Tk()
app = BatchRenameApp(root)

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置窗口大小为屏幕的一半
window_width = int(screen_width / 2)
window_height = int(screen_height / 2)

# 计算窗口左上角坐标使其居中
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 2)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 运行主循环
root.mainloop()
