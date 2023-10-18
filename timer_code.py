from tkinter import *
from tkinter import messagebox
from time import sleep
from datetime import timedelta
from threading import Thread
import os
import re

class Timer():

    def __init__(self):
        self.root = Tk()
        self.root['bg'] = "#fafafa"
        self.root.title("Timer")
        self.root.geometry('250x200')
        self.root.resizable(width=False, height=False) 

        self.title = Label(self.root, text='Введите время', bg='gray', font=40)
        self.title.pack()

        self.timer_label = Label(self.root, text='00:00:00', bg='#ababab', font=40)
        self.timer_label.pack()

        self.time_entry_string = StringVar()
        self.time_entry_string_last_valid = [u"00:00:00"]
        self.timeInput = Entry(self.root, bg='white', textvariable=self.time_entry_string)
        self.timeInput.pack()

        self.btn_start = Button(self.root, text='Поставить таймер', bg='yellow', command=self.make_thread)
        self.btn_start.pack() 

        self.btn_stop = Button(self.root, text='Сбросить таймер', bg='red', command=self.stop_timer)
        self.btn_stop.pack()


        self.reset = False
        self.has_timer = False


    def entry_mask_check(self, text: StringVar, valid: str, entry: Entry):
        time = re.findall("^\d{0,2}\:\d{0,2}\:\d{0,2}$",text.get())
        if len(time) != 1:
            text.set(valid[0])
        if time:
            valid[0] = time[0]
            #jump next on 2 digits
            cursor_position = entry.index("insert")
            index = time[0][:cursor_position].rfind(u":")
            if cursor_position - index == 3:
                entry.icursor(cursor_position+1)


    def run(self):    
        self.time_entry_string.trace("w", lambda *args: self.entry_mask_check(self.time_entry_string,\
        self.time_entry_string_last_valid, self.timeInput))
        self.time_entry_string.set("")
        self.timeInput.focus()
        self.root.mainloop()


    def stop_timer(self):
        self.reset = True
        self.timer_label['text'] = "00:00:00"

    def make_thread(self):
        if self.has_timer:
            messagebox.showerror(message="Timer has already started. Please, stop the previous one first")
            return 
        self.t_thr = Thread(target=self.start_timer)
        self.t_thr.daemon = True
        self.t_thr.start()
    


    def start_timer(self):
        # Starting a timer
        time = self.timeInput.get()

        if len(time.split(':')) != 3 or not all(i.isdigit() for i in time.split(':')):
            messagebox.showerror(message="Entered time doesn't match HH:MM:SS format. Please, enter the correct time")
            return
        
        self.has_timer = True
        
        hours, minutes, seconds = map(int, time.split(':'))

        self.timer = timedelta(days=0, hours=hours, minutes=minutes, seconds=seconds)

        while self.timer.seconds > 0 and not self.reset:
            self.timer -= timedelta(seconds=1)
            print(self.timer.seconds)
            sleep(1)
            self.timer_label['text'] = f"{self.timer.seconds // 3600:02d}:{self.timer.seconds // 60 % 60:02d}:{self.timer.seconds % 60:02d}"
        self.timer_label['text'] = "00:00:00"

        if not self.reset:
            os.system('shutdown -s')
        self.reset = False
        self.has_timer = False
        


if __name__ == '__main__':
    timer = Timer()
    timer.run()
    