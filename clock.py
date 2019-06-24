import tkinter as tk
import math

class Clock(tk.Frame):

    def __init__(self,master,initial_message):

        tk.Frame.__init__(self, master)

        self.canvas = tk.Canvas(self,width=100,height=100)

        self.hplus = tk.Button(self,command=self.advance_hour,text="h+")

        self.hminus = tk.Button(self,command=self.reverse_hour,text="h-")

        self.mplus = tk.Button(self,command=self.advance_minute,text='m+')

        self.mminus = tk.Button(self,command=self.reverse_minute,text='m-')

        self.textdisplay = tk.Label(self, text=initial_message)

        self.timedisplay = tk.Label(self, text="time input")

        self.hour = 0

        self.minute = 15

        self.pm = False

        self.hplus.grid(row=0,column=0)

        self.hminus.grid(row=0,column=1)

        self.mplus.grid(row=1,column=0)

        self.mminus.grid(row=1,column=1)

        self.canvas.grid(row=2,columnspan=2)

        self.textdisplay.grid(row=3)

        self.timedisplay.grid(row=4)

        self.__circlet = self.canvas.create_oval(1,1,99,99)

        self.hourhand = self.canvas.create_line(50,50,50,20,fill='red')

        self.minutehand = self.canvas.create_line(50,50,100,50,fill='blue')


    def draw_hourhand(self):

        self.canvas.delete(self.hourhand)

        hour = self.hour

        degrees = ((hour - 3) * 30) % 360

        radians = math.radians(degrees)

        x = (30 * math.cos(radians)) + 50

        y = (30 * math.sin(radians)) + 50

        self.hourhand = self.canvas.create_line(50,50,x,y,fill='red')

    def advance_hour(self):
        self.hour += 1
        if self.hour > 12:
            self.hour -= 12
            self.pm = not self.pm
        self.draw_hourhand()
        self.update_displaytime()

    def reverse_hour(self):
        self.hour -= 1
        if self.hour < 0:
            self.hour += 12
            self.pm = not self.pm
        self.draw_hourhand()
        self.update_displaytime()

    def draw_minutehand(self):

        self.canvas.delete(self.minutehand)

        minute = self.minute

        degrees = ((minute - 15) * 6) % 360

        radians = math.radians(degrees)

        x = (50 * math.cos(radians)) + 50

        y = (50 * math.sin(radians)) + 50

        self.minutehand = self.canvas.create_line(50, 50, x, y, fill='blue')

    def advance_minute(self):
        self.minute += 1
        if self.minute > 60:
            self.minute -= 60
        self.draw_minutehand()
        self.update_displaytime()

    def reverse_minute(self):
        self.minute -= 1
        if self.minute < 0:
            self.minute += 60
        self.draw_minutehand()
        self.update_displaytime()

    def totxt(self):
        return "{}:{} {}".format(self.hour,self.minute,"PM" if self.pm else "AM")

    def update_displaytime(self):

        self.timedisplay.config(text=self.totxt())

    @property
    def time(self):
        return self.hour,self.minute,"PM" if self.pm else "AM"
    




if __name__ == '__main__':

    root = tk.Tk()

    c = Clock(root, "Start time ZT")

    c.pack()
