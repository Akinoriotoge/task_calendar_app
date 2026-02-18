import tkinter as tk
from tkinter import simpledialog
from tkinter import font
from tkcalendar import Calendar
from models import add_task, get_tasks, delete_task
from PIL import Image, ImageTk
import os
import random
from datetime import date
from tkinter import filedialog
from ics_handler import save_ics
from models import get_task_by_id
from PIL import ImageDraw

def create_ui():
    root = tk.Tk()
    root.title("Task Calendar App")
    root.geometry("800x600")
    root.resizable(False, False)

    # ==========================
    # 背景画像ランダム選択
    # ==========================
    base_dir = os.path.dirname(__file__)
    assets_path = os.path.join(base_dir, "assets")

    images = [f for f in os.listdir(assets_path)
              if f.endswith((".png", ".jpg", ".jpeg"))]

    if not images:
        raise FileNotFoundError("assetsフォルダに画像がありません")

    selected_image = random.choice(images)
    bg_path = os.path.join(assets_path, selected_image)

    bg_image = Image.open(bg_path)
    bg_image = bg_image.resize((800, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo
    
    # ==========================
    # カレンダー
    # ==========================
    cal = Calendar(
        root,
        selectmode="day",
        year=2026,
        month=2,
        date_pattern="yyyy-mm-dd",
        font=("x10y12pxDonguriDuel", 18),
        headersfont=("x10y12pxDonguriDuel", 12, "bold"),
        width=28,
        height=12,
        background="#2b2b2b",
        foreground="white",

        weekendforeground="#ff8c8c",
        othermonthforeground="#777777",
        othermonthweforeground="#cc6666",
    )

    cal.place(relx=0.5, rely=0.48, anchor="center")

    import calendar
    from datetime import date

    def go_today():
        today = date.today()
        cal.selection_set(today)
        cal.see(today)

    tk.Button(
        root,
        text="今日へ",
        font=("x12y16pxMaruMonica", 14),
        command=go_today
    ).place(relx=0.9, rely=0.05)

    def open_credit():
        credit_window = tk.Toplevel(root)
        credit_window.title("Credit")
        credit_window.geometry("420x340")
        credit_window.resizable(False, False)
        credit_window.configure(bg="#1e1e1e")

        credit_window.transient(root)
        credit_window.grab_set()

        # タイトル
        tk.Label(
            credit_window,
            text="Credit",
            font=("x10y12pxDonguriDuel", 18),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=(20, 15))

        tk.Label(
            credit_window,
            text="Application Developer\nLusi",
            font=("x10y12pxDonguriDuel", 12),
            fg="#ffffff",
            bg="#1e1e1e",
            justify="center"
        ).pack(pady=5)

        tk.Label(
            credit_window,
            text="Fonts\n"
                 "x10y12pxDonguriDuel\n"
                 "x12y16pxMaruMonica\n"
                 "Author: 患者長ひっく様\n"
                 "https://hicchicc.github.io/00ff/",
            font=("x12y16pxMaruMonica", 10 ,"bold"),
            fg="#cccccc",
            bg="#1e1e1e",
            justify="center"
        ).pack(pady=8)

        tk.Label(
            credit_window,
            text="Background Material\n"
                 "空の背景素材\n"
                 "Author: 優月ねむ様\n"
                 "https://yudukinemu.booth.pm/",
            font=("x12y16pxMaruMonica", 10, "bold"),
            fg="#cccccc",
            bg="#1e1e1e",
            justify="center"
        ).pack(pady=8)

        tk.Button(
            credit_window,
            text="Close",
            command=credit_window.destroy
        ).pack(pady=15)



    def mark_event_days():
        cal.calevent_remove("event")

        tasks = get_tasks()

        for task in tasks:
            start = task[3]
            task_date = start.split(" ")[0]

            y, m, d = map(int, task_date.split("-"))
            cal.calevent_create(date(y, m, d), "●", "event")

        cal.tag_config("event", foreground="green")

    def highlight_today(year, month):
        cal.calevent_remove("today")

        today = date.today()

        if today.year == year and today.month == month:
            cal.calevent_create(today, "Today", "today")

        cal.tag_config("today", background="#4444aa", foreground="white")

    #初回実行部分
    m, y = cal.get_displayed_month()
    highlight_today(y, m)
    mark_event_days()

    # 月変更時にも再実行
    def update_colors(event):
        m, y = cal.get_displayed_month()
        highlight_today(y, m)
        mark_event_days()

    cal.bind("<<CalendarDisplayed>>", update_colors)

    # ==========================
    # タスクリスト
    # ==========================
    list_frame = tk.Frame(root, bg="white")
    list_frame.place(relx=0.5, rely=0.85, anchor="center", width=600, height=120)

    listbox = tk.Listbox(
        list_frame,
        font=("x12y16pxMaruMonica", 12),
        bd=0
    )
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    task_ids = []

    # ==========================
    # 更新処理
    # ==========================
    def refresh():
        listbox.delete(0, tk.END)
        task_ids.clear()
    
        today_str = date.today().strftime("%Y-%m-%d")

        for task in get_tasks():
            task_id = task[0]
            title = task[1]
            start = task[3]
            end = task[4]

            task_date = start.split(" ")[0]

            start_time = start.split(" ")[1]
            end_time = end.split(" ")[1]

            if start_time == "00:00" and end_time == "23:59":
                time_text = "終日"
            else:
                time_text = f"{start_time} - {end_time}"

            text = f"{title} ({time_text})"

            listbox.insert(tk.END, text)
            index = listbox.size() - 1

            # 今日の予定なら赤
            if task_date == today_str:
                listbox.itemconfig(index, fg="red")

            task_ids.append(task_id)

    # ==========================
    # 削除処理
    # ==========================
    def delete_selected():
        selected = listbox.curselection()

        if not selected:
            return

        index = selected[0]
        task_id = task_ids[index]
        delete_task(task_id)
        refresh()

    def export_selected_ics():
        selected = listbox.curselection()

        if not selected:
            return

        index = selected[0]
        task_id = task_ids[index]

        task_row = get_task_by_id(task_id)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".ics",
            filetypes=[("ICS files", "*.ics")],
            initialfile=f"{task_row[1]}.ics"
        )

        if file_path:
            save_ics(task_row, file_path)
    
    # ===== ボタンエリア =====
    button_frame = tk.Frame(root)
    button_frame.place(relx=0.5, rely=0.95, anchor="center")

    delete_button = tk.Button(
        button_frame,
        text="削除",
        font=("x12y16pxMaruMonica", 14),
        command=delete_selected
    )
    delete_button.pack(side="left", padx=10)

    export_button = tk.Button(
        button_frame,
        text="ICS保存",
        font=("x12y16pxMaruMonica", 14),
        command=export_selected_ics
    )
    export_button.pack(side="left", padx=10)

    credit_button = tk.Button(
        button_frame,
        text="Credit",
        font=("x12y16pxMaruMonica", 14),
        command=open_credit
    )
    credit_button.pack(side="left", padx=10)

    def open_event_editor(date):

        editor = tk.Toplevel(root)
        editor.title("予定追加")
        editor.geometry("320x300")

        tk.Label(editor, text=f"{date} の予定").pack(pady=5)

        # タイトル
        tk.Label(editor, text="タイトル").pack()
        title_entry = tk.Entry(editor, width=25)
        title_entry.pack(pady=5)

        # ===== 開始時間 =====
        time_frame_start = tk.Frame(editor)
        time_frame_start.pack(pady=5)

        tk.Label(time_frame_start, text="開始").grid(row=0, column=0)

        start_hour = tk.Spinbox(time_frame_start, from_=0, to=23, width=3)
        start_hour.grid(row=0, column=1)

        tk.Label(time_frame_start, text=":").grid(row=0, column=2)

        start_min = tk.Spinbox(time_frame_start, values=[f"{i:02}" for i in range(0, 60, 5)], width=3)
        start_min.grid(row=0, column=3)

        # デフォルト値
        start_hour.delete(0, tk.END)
        start_hour.insert(0, "10")
        start_min.delete(0, tk.END)
        start_min.insert(0, "00")

        # ===== 終了時間 =====
        time_frame_end = tk.Frame(editor)
        time_frame_end.pack(pady=5)

        tk.Label(time_frame_end, text="終了").grid(row=0, column=0)

        end_hour = tk.Spinbox(time_frame_end, from_=0, to=23, width=3)
        end_hour.grid(row=0, column=1)

        tk.Label(time_frame_end, text=":").grid(row=0, column=2)

        end_min = tk.Spinbox(time_frame_end, values=[f"{i:02}" for i in range(0, 60, 5)], width=3)
        end_min.grid(row=0, column=3)

        end_hour.delete(0, tk.END)
        end_hour.insert(0, "11")
        end_min.delete(0, tk.END)
        end_min.insert(0, "00")

        # ===== 終日チェック =====
        all_day_var = tk.BooleanVar()

        def toggle_time():
            state = "disabled" if all_day_var.get() else "normal"
            start_hour.config(state=state)
            start_min.config(state=state)
            end_hour.config(state=state)
            end_min.config(state=state)

        all_day_check = tk.Checkbutton(
            editor,
            text="終日",
            variable=all_day_var,
            command=toggle_time
        )
        all_day_check.pack(pady=5)

        # ===== 保存処理 =====
        def save_event():
            title = title_entry.get()

            if not title:
                return

            if all_day_var.get():
                start = f"{date} 00:00"
                end = f"{date} 23:59"
            else:
                start = f"{date} {start_hour.get()}:{start_min.get()}"
                end = f"{date} {end_hour.get()}:{end_min.get()}"

            add_task(title, "", start, end)
            refresh()
            editor.destroy()

        tk.Button(editor, text="保存", command=save_event).pack(pady=10)
        tk.Button(editor, text="キャンセル", command=editor.destroy).pack()

    # ==========================
    # カレンダークリック時
    # ==========================
    def add_from_calendar(event):
        date = cal.get_date()
        open_event_editor(date)

    cal.bind("<<CalendarSelected>>", lambda e: open_event_editor(cal.get_date()))

    refresh()

    m, y = cal.get_displayed_month()
    highlight_today(y, m)

    return root
