import tkinter as tk
from tkinter import messagebox
import random









class guessingGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.resizable(False, False)


        container = tk.Frame(self)
        container.pack(padx=20, pady=20)

        self.min_val = tk.StringVar(value=1)
        self.max_val = tk.StringVar(value=100)

        self.max_attempts_check_button = tk.BooleanVar(value=False)
        self.hint_check_button = tk.BooleanVar(value=False)


        self.max_attempts_number = tk.StringVar()
        self.frames = {} # This is a dictionary not a list
        for F in (mainMenu, playScreen, maxAttemptsScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        

        self.show("mainMenu")
        self.after(0, self.center_window)





    def show(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
        
        if hasattr(frame, "on_show"):
            frame.on_show()





    def center_window(self) -> None:
        self.update_idletasks() #Ensure size info is correct

        window_width = self.winfo_width()
        window_height = self.winfo_height()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 150

        self.geometry(f"+{x}+{y}")











class mainMenu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.bind("<Button-1>", lambda e: self.focus_set())

        welcomeLabel = tk.Label(self, text="Welcome to the Number Guessing Game!", font=('Arial', 24), justify="center")
        welcomeLabel.pack(padx=70, pady=20)

        welcomeLabel2 = tk.Label(self, text="Your goal is to guess the number the computer is thinking off!", font=('Arial', 14), justify="center")
        welcomeLabel2.pack(padx=70)

        playButton = tk.Button(self, text="Play", font=('Arial', 24), padx=20, command=lambda: self._play_button_logic(app)) #WRITE IN command=self.play_game()
        playButton.pack(pady=40)

        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Frame for the settings buttons
        switchesFrame = tk.Frame(self)
        switchesFrame.pack(pady=10)

        maxAttemptsSwitchCheckbutton = tk.Checkbutton(switchesFrame, text="Max Attempts", font=('Arial', 14), variable=app.max_attempts_check_button) #Can make it so it says Maximum Attempts On and On is Green but if it is off make it say Maximum Attempts Off and Off is red
        maxAttemptsSwitchCheckbutton.pack(side="left", padx=10)
        ToolTip(maxAttemptsSwitchCheckbutton, "Limits the number of guesses you can make before the game ends. You will choose how many guesses once you press play.")

        hintSwitchCheckbutton = tk.Checkbutton(switchesFrame, text="Hints", font=('Arial', 14), variable=app.hint_check_button) #Can make it so it says Maximum Attempts On and On is Green but if it is off make it say Maximum Attempts Off and Off is red
        hintSwitchCheckbutton.pack(side="left", padx=10)
        ToolTip(hintSwitchCheckbutton, "Enables hints after incorrect guesses. Example: \"too high\" or \"too low\"")

        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Frame for the two numeric scrolling input boxes
        inputsFrame = tk.Frame(self)
        inputsFrame.pack(pady=10)


        # Variables to hold the numeric values
        self.min_val = app.min_val
        self.max_val = app.max_val


        vcmd = (self.register(self._is_valid_int), "%P")


        min_label = tk.Label(inputsFrame, text="Min:", font=('Arial', 14), padx=16)
        min_label.grid(row=0, column=0, pady=5, sticky="e")
        ToolTip(min_label, "Pick the lowest number the computer can pick from")
        self.min_entry = tk.Entry(inputsFrame, textvariable=self.min_val, width=8, font=('Arial', 14), validate="key", validatecommand=vcmd)
        self.min_entry.grid(row=0, column=1, padx=0, pady=5)
        ToolTip(self.min_entry, "Pick the lowest number the computer can pick from")

        min_btns = tk.Frame(inputsFrame)
        min_btns.grid(row=0, column=2, padx=(0, 16))
        tk.Button(min_btns, text="▲", width=2, command=lambda: self._step("min", +1), font=('Arial', 6)).pack()
        tk.Button(min_btns, text="▼", width=2, command=lambda: self._step("min", -1), font=('Arial', 6)).pack()
        ToolTip(min_btns, "Pick the lowest number the computer can pick from")


        max_label = tk.Label(inputsFrame, text="Max:", font=('Arial', 14), padx=16)
        max_label.grid(row=0, column=3, pady=5, sticky="e")
        ToolTip(max_label, "Pick the highest number the computer can pick from")
        self.max_entry = tk.Entry(inputsFrame, textvariable=self.max_val, width=8, font=('Arial', 14), validate="key", validatecommand=vcmd)
        self.max_entry.grid(row=0, column=4, padx=0, pady=5)
        ToolTip(self.max_entry, "Pick the highest number the computer can pick from")

        max_btns = tk.Frame(inputsFrame)
        max_btns.grid(row=0, column=5)
        tk.Button(max_btns, text="▲", width=2, command=lambda: self._step("max", +1), font=('Arial', 6)).pack()
        tk.Button(max_btns, text="▼", width=2, command=lambda: self._step("max", -1), font=('Arial', 6)).pack()
        ToolTip(max_btns, "Pick the highest number the computer can pick from")





    def _step(self, which: str, delta: int) -> None:
        var = self.min_val if which == "min" else self.max_val
        other = self.max_val if which == "max" else self.min_val

        # If the current box is blank/"-", decide a sensible starting point
        try:
            v = int(var.get())
        except ValueError:
            # Start from the other value if available, else 0
            try:
                v = int(other.get())
            except ValueError:
                v = 0
        
        v += delta

        # Optional hard clamp to your overall bounds
        v = max(-999999999, min(999999999, v))

        # Avoid -0
        if v == 0:
            var.set("0")
        else:
            var.set(str(v))





    def _is_valid_int(self, proposed: str) -> bool:
        # Allow temporary typing states
        if proposed in ("", "-"):
            return True
        
        # Disallow "-0" explicitly
        if proposed == "-0":
            return False
        
        # Handle optional minus
        if proposed.startswith("-"):
            num = proposed[1:]
        else:
            num = proposed
        
        # Must be digits
        if not num.isdigit():
            return False
        
        # No leading zeros unless exactly 0
        if len(num) > 1 and num.startswith("0"):
            return False
        
        if int(num) < -9999999 or int(num) > 9999999:
            return False
        
        return True





    def _play_button_logic(self, app) -> None:
        min_val = self.min_val.get()
        max_val = self.max_val.get()
        if min_val in ("", "-") or max_val in ("", "-"):
            messagebox.showinfo(title="Message", message="Invalid entry to play")

        min_val = int(min_val)
        max_val = int(max_val)
        if not (min_val <= max_val):
            messagebox.showinfo(title="Message", message="Min has to be less than or equal to Max")
        else:
            if app.max_attempts_check_button.get():
                app.show("maxAttemptsScreen")
            else:
                app.show("playScreen")










class playScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        vcmd = (self.register(self._is_valid_int), "%P")


        mewFrame = tk.Frame(self)
        mewFrame.pack()

        newFrame = tk.Frame(mewFrame)
        newFrame.grid(row=0, column=1)

        computerNumberLabel = tk.Label(newFrame, text="Computer Number: ?", font=('Arial', 20))
        computerNumberLabel.pack(padx=70, pady=20)
        ToolTip(computerNumberLabel, "The number of question marks does not denote the number of digits the computer number has")



        inputsFrame = tk.Frame(newFrame)
        inputsFrame.pack(pady=(88, 20))
        self.user_number = tk.StringVar()
        self.user_number_entry = tk.Entry(inputsFrame, textvariable=self.user_number, width=8, font=('Arial', 20), validate="key", validatecommand=vcmd)
        self.user_number_entry.grid(row=0, column=0, padx=16)

        self.submit_button = tk.Button(inputsFrame, text="Submit", command=lambda: self.submit(), font=('Arial', 14))
        self.submit_button.grid(row=0, column=1)


        self.remaining_guesses_string = tk.StringVar()
        self.remaining_guesses_label = tk.Label(newFrame, textvariable=self.remaining_guesses_string, font=('Arial', 14))
        self.remaining_guesses_label.pack()        


        self.hint = tk.StringVar()
        self.hint_label = tk.Label(newFrame, textvariable=self.hint, font=('Arial', 14))
        self.hint_label.pack(pady=(10,0))


        self.previous_guess = tk.StringVar()
        self.previous_guess_label = tk.Label(newFrame, textvariable=self.previous_guess, font=('Arial', 18), wraplength=250, height=2)
        self.previous_guess_label.pack(pady=60)



        history_outer = tk.Frame(mewFrame)
        history_outer.grid(row=0, column=0)

        tk.Label(history_outer, text="Guess History", font=('Arial', 14)).pack(anchor="w")

        list_frame = tk.Frame(history_outer)
        list_frame.pack(pady=5, anchor="w")

        self.guess_listbox = tk.Listbox(list_frame, height=8, width=15, font=('Arial', 12))
        self.guess_listbox.pack(side="left", fill="y")

        scroll = tk.Scrollbar(list_frame, orient="vertical", command=self.guess_listbox.yview)
        scroll.pack(side="left", fill="y")

        self.guess_listbox.config(yscrollcommand=scroll.set)

        lookup_frame = tk.Frame(history_outer)
        lookup_frame.pack()

        lookup_row = tk.Frame(lookup_frame)
        lookup_row.pack()

        self.lookup_var = tk.StringVar()
        self.lookup_entry = tk.Entry(lookup_row, textvariable=self.lookup_var, font=('Arial', 12), width=12)
        self.lookup_entry.pack(side="left")

        self.lookup_btn = tk.Button(lookup_row, text="Find", font=('Arial', 12), command=self.find_guess)
        self.lookup_btn.pack(side="left", padx=8)

        self.lookup_status = tk.StringVar(value="")
        tk.Label(lookup_frame, textvariable=self.lookup_status, font=('Arial', 9)).pack(anchor="w")
        
        """computerNumberLabel = tk.Label(self, text="Computer Number: ?", font=('Arial', 20))
        computerNumberLabel.pack(padx=70, pady=20)
        ToolTip(computerNumberLabel, "The number of question marks does not denote the number of digits the computer number has")



        inputsFrame = tk.Frame(self)
        inputsFrame.pack(pady=(88, 20))
        self.user_number = tk.StringVar()
        self.user_number_entry = tk.Entry(inputsFrame, textvariable=self.user_number, width=8, font=('Arial', 20), validate="key", validatecommand=vcmd)
        self.user_number_entry.grid(row=0, column=0, padx=16)

        self.submit_button = tk.Button(inputsFrame, text="Submit", command=lambda: self.submit(), font=('Arial', 14))
        self.submit_button.grid(row=0, column=1)


        self.remaining_guesses_string = tk.StringVar()
        self.remaining_guesses_label = tk.Label(self, textvariable=self.remaining_guesses_string, font=('Arial', 14))
        self.remaining_guesses_label.pack()        


        self.hint = tk.StringVar()
        self.hint_label = tk.Label(self, textvariable=self.hint, font=('Arial', 14))
        self.hint_label.pack(pady=(10,0))


        self.previous_guess = tk.StringVar()
        self.previous_guess_label = tk.Label(self, textvariable=self.previous_guess, font=('Arial', 18))
        self.previous_guess_label.pack(pady=60)



        history_outer = tk.Frame(self)
        history_outer.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        tk.Label(history_outer, text="Guess History", font=('Arial', 14)).pack(anchor="w")

        list_frame = tk.Frame(history_outer)
        list_frame.pack(pady=5, anchor="w")

        self.guess_listbox = tk.Listbox(list_frame, height=8, width=15, font=('Arial', 12))
        self.guess_listbox.pack(side="left", fill="y")

        scroll = tk.Scrollbar(list_frame, orient="vertical", command=self.guess_listbox.yview)
        scroll.pack(side="left", fill="y")

        self.guess_listbox.config(yscrollcommand=scroll.set)

        lookup_frame = tk.Frame(history_outer)
        lookup_frame.pack(fill="x")

        self.lookup_var = tk.StringVar()
        self.lookup_entry = tk.Entry(lookup_frame, textvariable=self.lookup_var, font=('Arial', 12), width=12)
        self.lookup_entry.pack(side="left")

        self.lookup_btn = tk.Button(lookup_frame, text="Find", font=('Arial', 12), command=self.find_guess)
        self.lookup_btn.pack(side="left", padx=8)

        self.lookup_status = tk.StringVar(value="")
        tk.Label(lookup_frame, textvariable=self.lookup_status, font=('Arial', 11)).pack(side="left", padx=8)"""
        





    def on_show(self):
        self.start_game()

        if self.app.max_attempts_check_button.get() == False:
            self.remaining_guesses_string.set(f"Number of Guesses Remaining: Infinite")
        else:
            self.remaining_guesses_string.set(f"Number of Guesses Remaining: {self.app.max_attempts_number.get()}")


    
    
    
    
    
    def start_game(self):
        min_v = int(self.app.min_val.get())
        max_v = int(self.app.max_val.get())

        self.computerNumber = random.randint(min_v, max_v)
        print(self.computerNumber)
    
    



    def _is_valid_int(self, proposed: str) -> bool:
        # Allow temporary typing states
        if proposed in ("", "-"):
            return True
        
        # Disallow "-0" explicitly
        if proposed == "-0":
            return False
        
        # Handle optional minus
        if proposed.startswith("-"):
            num = proposed[1:]
        else:
            num = proposed
        
        # Must be digits
        if not num.isdigit():
            return False
        
        # No leading zeros unless exactly 0
        if len(num) > 1 and num.startswith("0"):
            return False
        
        if int(num) < -9999999 or int(num) > 9999999:
            return False
        
        return True
    




    def submit(self):
        user_number = self.user_number.get()
        if user_number in ("", "-"):
            messagebox.showinfo(title="Message", message="Invalid submission")
            return
        
        user_number = int(user_number)

        if user_number != self.computerNumber:
            if self.app.max_attempts_check_button.get() == True:
                self.app.max_attempts_number.set(str(int(self.app.max_attempts_number.get()) - 1))
                self.remaining_guesses_string.set(f"Number of Guesses Remaining: {self.app.max_attempts_number.get()}")
            self.previous_guess.set(f"You're previous guess of {user_number} was incorrect")
            

            if self.app.hint_check_button.get() == True:
                if user_number > self.computerNumber:
                    result = "too high"
                    self.hint.set("Hint: Your guess was too high")
                else:
                    result = "too low"
                    self.hint.set("Hint: Your guess was too low")
                self.guess_listbox.insert("end", f"{user_number} ({result})")
                self.guess_listbox.see("end")
            else:
                self.guess_listbox.insert("end", f"{user_number}")
                self.guess_listbox.see("end")

            

        if user_number == self.computerNumber:
            print("You did it")


        


    def find_guess(self):
        target = self.lookup_var.get().strip()
        if target in ("", "-"):
            self.lookup_status.set("Enter a number to search.")
            return
        
        try:
            target_int = int(target)
        except ValueError:
            self.lookup_status("Not a valid number.")
            return
        
        items = self.guess_listbox.get(0, "end")
        for i, item in enumerate(items):
            if str(target_int) in item:
                self.guess_listbox.selection_clear(0, "end")
                self.guess_listbox.selection_set(i)
                self.guess_listbox.activate(i)
                self.guess_listbox.see(i)
                self.lookup_status.set("")
                return
            
        self.lookup_status.set("Not found.")
        









class maxAttemptsScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        tk.Label(self, text="How many attempts would you like to guess the computer number?", font=('Arial', 24), justify="center", wraplength=500).pack(padx=70, pady=20)

        vcmd = (self.register(self._is_valid_int), "%P")

        self.max_attempts_number = app.max_attempts_number
        
        inputsFrame = tk.Frame(self)
        inputsFrame.pack(pady=128)
        self.max_attempts_number_entry = tk.Entry(inputsFrame, textvariable=self.max_attempts_number, width=8, font=('Arial', 20), validate="key", validatecommand=vcmd)
        self.max_attempts_number_entry.grid(row=0, column=0, padx=16)

        self.submit_button = tk.Button(inputsFrame, text="Submit", command=lambda: self.submit(app), font=('Arial', 14))
        self.submit_button.grid(row=0, column=1)





    def _is_valid_int(self, proposed: str) -> bool:
        # Allow temporary typing states
        if proposed in "":
            return True
        
        num = proposed
        
        # Must be digits
        if not num.isdigit():
            return False
        
        # No leading zeros unless exactly 0
        if len(num) > 1 and num.startswith("0"):
            return False
        
        if int(num) < -9999999 or int(num) > 9999999:
            return False
        
        return True





    def submit(self, app):
        if self.max_attempts_number.get() in "":
            if messagebox.askyesno(title="Default Guesss Amount", message="Would you like to manually choosing the guessing amount? (If no then the guessing amount will default to 3)"):
                pass
            else:
                self.max_attempts_number.set("3")
                app.show("playScreen")
        else:
            app.show("playScreen")





class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True) # No window decorations
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 10))
        label.pack(ipadx=6, ipady=4)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None










if __name__ == "__main__":
    guessingGameGUI().mainloop()