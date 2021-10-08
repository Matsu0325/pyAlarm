import tkinter as tk
from tkinter import messagebox as msgbox
import os
import datetime
import sys
import jpholiday


#終了処理
def endloop():
    sys.exit()


#画面中央表示
def set_Center(r):
    ww = r.winfo_screenwidth()
    wh = r.winfo_screenheight()
    lw = r.winfo_width()
    lh = r.winfo_height()
    r.geometry("300x180"+"+"+str(int(ww/2-lw/2))+"+"+str(int(wh/2-lh/2)))


#充電日通知
def msg_schedule(day, file):
    root = tk.Tk()
    root.geometry('300x180')
    root.configure(bg='snow')
    root.title('PYアラーム') 

    if day == 'today':
        canvas = tk.Canvas(root, width=50, height=50, bg='snow', highlightthickness=0)
        canvas.create_oval(5, 5, 45, 45, fill='gold', outline='gold')
        canvas.create_text(25,27,text='❕', font=('メイリオ',18))
        canvas.place(relx=0.5,rely=0.2, anchor=tk.CENTER)
        txt_main = tk.Label(root, text='予定日です', bg='snow', font=('メイリオ', 14))
        txt_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    elif day == 'tomorrow':
        canvas = tk.Canvas(root, width=50, height=50, bg='snow', highlightthickness=0)
        canvas.create_oval(5, 5, 45, 45, fill='gold', outline='gold')
        canvas.create_text(25,27,text='❕', font=('メイリオ',18))
        canvas.place(relx=0.5,rely=0.2, anchor=tk.CENTER)
        txt_main = tk.Label(root, text='次回予定日は明日です', bg='snow', font=('メイリオ', 14))
        txt_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    elif day == 'next_week':
        color_info = 'Royal Blue2'
        canvas = tk.Canvas(root, width=50, height=50, bg='snow', highlightthickness=0)
        canvas.create_oval(5, 5, 45, 45, fill=color_info, outline=color_info)
        canvas.create_text(25,27,text='i', font=('メイリオ',18, 'bold'), fill='snow')
        canvas.place(relx=0.5,rely=0.2, anchor=tk.CENTER)
        txt_main = tk.Label(root, text='次回予定日は1週間後です', bg='snow', font=('メイリオ', 14))
        txt_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    elif day == 'passed':
        canvas = tk.Canvas(root, width=50, height=50, bg='snow', highlightthickness=0)
        canvas.create_oval(5, 5, 45, 45, fill='gold', outline='gold')
        canvas.create_text(25,27,text='❕', font=('メイリオ',18))
        canvas.place(relx=0.5,rely=0.2, anchor=tk.CENTER)
        txt_main = tk.Label(root, text='予定日を過ぎています\n再設定してください', bg='snow', font=('メイリオ', 14))
        txt_main.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    else:
        sys.exit()

    btn_reset = tk.Button(root, text='再設定', width=14, bg='white smoke', relief='groove', command=lambda:[root.destroy(), setting_day(file), endloop()])
    btn_reset.pack(padx=20,pady=10,anchor=tk.S, side='right')

    btn_OK = tk.Button(root, text='了解', width=14, bg='white smoke', relief='groove', command=endloop)
    btn_OK.pack(padx=20, pady=10, anchor=tk.S, side='left')

    root.mainloop()


#充電日設定
def setting_day(file):
    root_set = tk.Tk()
    root_set.geometry('300x180')
    root_set.configure(bg='snow')
    root_set.title('予定日設定')

    t = tk.Entry(root_set, width=18)
    t.place(relx=0.4, rely=0.4, anchor=tk.CENTER)
    t.insert(tk.END,datetime.date.today().strftime("%Y/%m/%d"))

    btn_30day = tk.Button(root_set, text='30日後に設定', width=12, bg='white smoke', relief='groove', command=lambda:[set_ok(True, file, ""), endloop()])
    btn_30day.place(relx=0.3, rely=0.8, anchor=tk.CENTER)

    btn_set = tk.Button(root_set, text='設定', width=8, bg='white smoke', relief='groove', command=lambda:[set_ok(False, file, t.get())])
    btn_set.place(relx=0.8, rely=0.4, anchor=tk.CENTER)

    btn_cancel = tk.Button(root_set, text='キャンセル', width=12, bg='white smoke', relief='groove', command=endloop)
    btn_cancel.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

    root_set.mainloop()
    

#設定確認ダイアログ
def set_ok(flg_simple, file, t):
    if flg_simple:
        ask = msgbox.askokcancel("予定日設定","30日後に設定します\nよろしいですか？")
        if ask:
            simple_month(file)  
    else:
        day = datetime.datetime.strptime(t, "%Y/%m/%d").date()
        if not checkDate(t):
            msgbox.showwarning("予定日設定","フォーマットエラー\n例："+t)
        elif datetime.date.today() >= day:
            msgbox.showwarning("予定日設定","今日より前の日付になっています")
        elif day.weekday()>4 or jpholiday.is_holiday(day):
            ask = msgbox.askokcancel("予定日設定",t+"は休日です\nよろしいですか？")
            if ask:
                set_next(file, t)
        else:
            ask = msgbox.askokcancel("予定日設定",t+"に設定します\nよろしいですか？")
            if ask:
                set_next(file, t)    

#日付フォーマットチェック
def checkDate(t):
    try:
        datetime.datetime.strptime(t, "%Y/%m/%d")
        return True
    except ValueError:
        return False

#指定日でファイルに書き込む
def set_next(file, t):
    f = open (file, 'w')
    f.writelines(t)
    f.close()
    msgbox.showinfo("設定完了", t+"に設定しました")
    endloop()

#30日後の設定でファイルに書き込む
def simple_month(file):
    nextday = after_holiday(datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y/%m/%d")
    f = open (file, 'w')
    f.writelines(nextday)
    f.close()
    msgbox.showinfo("設定完了", nextday+"に設定しました")
    endloop()
    
#休日を飛ばす処理
def after_holiday(day):
    if day.weekday() == 5:
        return after_holiday(day + datetime.timedelta(days=2))
    elif day.weekday() == 6:
        return after_holiday(day + datetime.timedelta(days=1))
    elif jpholiday.is_holiday(day):
        return after_holiday(day + datetime.timedelta(days=1))
    else:
        return day

#予定日との日にち差を計算する
def next_day(nextday, file):
    today = datetime.date.today()
    if nextday == today:
        msg_schedule('today', file)
    elif nextday == today + datetime.timedelta(days=1):
        msg_schedule('tomorrow', file)
    elif nextday == today + datetime.timedelta(days=7):
        msg_schedule('next_week', file)
    elif nextday < today:
        msg_schedule('passed', file)

#ファイルを探す
def file_search():
    here = os.getcwd()
    filename = here + "/pyAlarm_day.txt"
    if os.path.isfile(filename):
        t = open(filename, 'r').readline()
        next_day(datetime.datetime.strptime(t, "%Y/%m/%d").date(), filename)
    else:
        root_search=tk.Tk()
        root_search.withdraw()
        ask = msgbox.askyesno('PYアラーム','予定日が設定されていません\n設定しますか？')
        if ask:
            setting_day(filename)

#テスト用
#msg_schedule("t")
#setting_day(os.getcwd()+"/pyAlarm_day.txt")

file_search()