import tkinter as tk
from tkinter import  *
import GuessNumber as GN

class LogIn:
    def __init__(self):
        self.t = tk.Tk()
        self.t.title("Guess Numbers")
        self.tips = StringVar()
        self.tips.set("Welcome to the game, please login")
        self.label = tk.Label(self.t, textvariable=self.tips)
        self.label.grid(row=0, column=0, columnspan=4)

        self.name = tk.Label(self.t, text="Username: ")
        self.passwd = tk.Label(self.t, text="Password: ")
        self.name.grid(row=1, column=0, columnspan=1)
        self.passwd.grid(row=2, column=0, columnspan=1)
        self.getname = tk.Entry(self.t)
        self.getpasswd = tk.Entry(self.t, show="*")
        self.getname.grid(row=1, column=1, columnspan=3)
        self.getpasswd.grid(row=2, column=1, columnspan=3)

        self.create = tk.Button(self.t, text="Create Account", command=Create().t.mainloop())
        self.create.grid(row=3, column=0, columnspan=2)
        self.login = tk.Button(self.t, text="Login", command=self.login)
        self.login.grid(row=3, column=2, columnspan=2)


    def login(self):
        name = self.getname.get()
        passwd = self.getpasswd.get()
        user = GN.GuessNumbers(name)
        check = user.check_user_gui(passwd)
        if check:
            level = tk.Toplevel(self.t)
            lebel = tk.Label(level, text="This game has 4 levels, choose your level:")
            lebel.grid(row=0, column=0, columnspan=2)
            entry = tk.Entry(level, text="choose from 1-4")
            entry.grid(row=1, column=0, columnspan=1)
            button1=tk.Button(level, text="OK", command=level.quit)
            button1.grid(row=1, column=1, columnspan=1)
            level.mainloop()
            print(entry.get())
            g = GuessGui(name,int(entry.get()))
            g.t.mainloop()
            self.t.quit()
            return check
        else:
            if name == "":
                return True
            else:
                wrong = tk.Toplevel(self.t)
                lebel = tk.Label(wrong, text="Wrong Password!")
                lebel.grid(row=0, column=0, columnspan=2)
                button1 = tk.Button(wrong, text="Retry", command=wrong.quit)
                button1.grid(row=1, column=0, columnspan=1)
                button2 = tk.Button(wrong, text="Create New Account", command=Create().t.mainloop())
                button2.grid(row=1, column=1, columnspan=1)
                wrong.mainloop()

class Create:
    def __init__(self):
        self.t = tk.Tk()
        self.t.title("Guess Numbers")
        self.tips = StringVar()
        self.tips.set("Please enter you username and password:")
        self.label = tk.Label(self.t, textvariable=self.tips)
        self.label.grid(row=0, column=0, columnspan=4)

        self.name = tk.Label(self.t, text="Enter Username: ")
        self.passwd = tk.Label(self.t, text="Enter Password: ")
        self.passwd2 = tk.Label(self.t, text="Password again: ")
        self.name.grid(row=1, column=0, columnspan=1)
        self.passwd.grid(row=2, column=0, columnspan=1)
        self.passwd2.grid(row=3, column=0, columnspan=1)
        self.getname = tk.Entry(self.t)
        self.getpasswd = tk.Entry(self.t, show="*")
        self.getpasswd2 = tk.Entry(self.t, show="*")
        self.getname.grid(row=1, column=1, columnspan=3)
        self.getpasswd.grid(row=2, column=1, columnspan=3)
        self.getpasswd2.grid(row=3, column=1, columnspan=3)
        self.createbutton = tk.Button(self.t, text="Create Account", command=self.create)
        self.createbutton.grid(row=3, column=0, columnspan=2)

    def create(self):
        name = self.getname.get()
        while self.getpasswd.get() != self.getpasswd2.get():
            self.tips.set("Two passwd are not the same, enter again")
        passwd = self.getpasswd2.get()
        GN.GuessNumbers(name).create_user_gui(name, passwd)
        g = GuessGui(name, int(entry.get()))
        g.t.mainloop()
        self.t.quit()

class GuessGui:
    def __init__(self, name, h):
        self.t = tk.Tk()
        self.t.title("Guess Numbers")
        self.name = name
        self.h = int(h)+2
        self.nums = GN.num_generator(self.h)
        self.times = 1  # times of play
        self.count = 10
        #self.game = tk.Frame(self.t)
        #self.game.pack()

        self.tips = StringVar()
        self.tips.set("Welcome " + self.name + ", Please enter " + str(self.h) + " numbers!")
        self.tipstext = tk.Label(self.t, textvariable=self.tips)
        self.tipstext.grid(row=0, column=1, columnspan=2)
        self.tipslable = tk.Label(self.t, text="Tips: ")
        self.tipslable.grid(row=0, column=0, columnspan=1)


        vcmd = (self.t.register(self.valid),"%P")
        self.numberbox = tk.Entry(self.t, validate="key", validatecommand=vcmd, invalidcommand=self.invalid)
        self.numberbox.grid(row=1, column=1, columnspan=2)
        self.numtips = tk.Label(self.t, text="Enter: ")
        self.numtips.grid(row=1, column=0, columnspan=1)

        self.guessbutton = tk.Button(self.t, text="Guess", command=self.guess)
        self.guessbutton.grid(row=2, column=0, columnspan=1)
        self.retrybutton = tk.Button(self.t, text="Retry", command=self.retry)
        self.retrybutton.grid(row=2, column=2, columnspan=2)

        self.text = tk.Text(self.t)
        self.text.grid(row=3, column=0, rowspan=5, columnspan=3)

        self.bar = tk.Menu(self.t)
        self.accountm = tk.Menu(self.bar, tearoff=0)
        self.accountm.add_command(label="add", command=self.donothing)
        self.accountm.add_command(label="change", command=self.donothing)
        self.accountm.add_separator()
        self.accountm.add_command(label="exit", command=self.t.quit)
        self.bar.add_cascade(label="account", menu=self.accountm)

        self.t.config(menu=self.bar)

    def donothing(self):
        filewin = tk.Toplevel(self.t)
        button =tk.Button(filewin, text="do nothing button")
        button.pack()

    def valid(self,P):
        in_str = P
        if(len(in_str)>self.h):
            print("too long")
            return  False
        else:
            for tmp in in_str:
                if(tmp in "0123456789"):
                    continue
                else:
                    print("else")
                    return False
            return True

    def invalid(self):
        self.tips.set("Please enter a number: ")


    def guess(self):
        if self.count>0:
            print(self.tips.get())
            in_nums = self.numberbox.get()
            user = GN.GuessNumbers(self.name)
            user.hard = self.h
            result = user.coundown_gui(self.nums, in_nums)
            print(result[0])
            self.text.insert("end", result[0])
            tips = "Chances left: "+str(self.count)
            self.tips.set(tips)
            if result[1] == 1:
                self.count -= 1
        else:
            self.tips.set("Press the retry button to start again!")
            self.text.insert("end", "Press the retry button to start again!\n")

    def retry(self):
        self.count = 10
        self.nums = GN.num_generator(self.h)
        self.tips.set("Game restarted!")




if __name__ == "__main__":
    log = LogIn()
    log.t.mainloop()




