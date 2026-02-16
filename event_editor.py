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
