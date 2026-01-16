import tkinter as tk
from tkinter import messagebox









class guessingGameGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.resizable(False, False)


        container = tk.Frame(self)
        container.pack(padx=20, pady=20)

        self.frames = {} # This is a dictionary not a list
        for F in (mainMenu, playScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show("mainMenu")

    def show(self, name: str):
        self.frames[name].tkraise()
        
        self.center_window()

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

        welcomeLabel = tk.Label(self, text="Welcome to the Number Guessing Game!", font=('Arial', 24), justify="center")
        welcomeLabel.pack(padx=70, pady=20)

        welcomeLabel2 = tk.Label(self, text="Your goal is to guess the number the computer is thinking off!", font=('Arial', 14), justify="center")
        welcomeLabel2.pack(padx=70)

        playButton = tk.Button(self, text="Play", font=('Arial', 24), padx=20, command=lambda: app.show("playScreen")) #WRITE IN command=self.play_game()
        playButton.pack(pady=40)

        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Frame for the settings buttons
        switchesFrame = tk.Frame(self)
        switchesFrame.pack(pady=10)

        maxAttemptsSwitchCheckbutton = tk.Checkbutton(switchesFrame, text="Max Attempts", font=('Arial', 14)) #Can make it so it says Maximum Attempts On and On is Green but if it is off make it say Maximum Attempts Off and Off is red
        maxAttemptsSwitchCheckbutton.pack(side="left", padx=10)
        ToolTip(maxAttemptsSwitchCheckbutton, "Limits the number of guesses you can make before the game ends. You will choose how many guesses once you press play.")

        hintSwitchCheckbutton = tk.Checkbutton(switchesFrame, text="Hints", font=('Arial', 14)) #Can make it so it says Maximum Attempts On and On is Green but if it is off make it say Maximum Attempts Off and Off is red
        hintSwitchCheckbutton.pack(side="left", padx=10)
        ToolTip(hintSwitchCheckbutton, "Enables hints after incorrect guesses. Example: too high or too low")

        # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Frame for the two numeric scrolling input boxes
        inputsFrame = tk.Frame(self)
        inputsFrame.pack(pady=10)


        # Variables to hold the numeric values
        self.min_val = tk.StringVar(value=1)
        self.max_val = tk.StringVar(value=100)


        min_vcmd = (self.register(self._validate_min), "%P")
        max_vcmd = (self.register(self._validate_max), "%P")


        tk.Label(inputsFrame, text="Min:", font=('Arial', 14)).grid(row=0, column=0, padx=8, pady=5, sticky="e")
        self.min_entry = tk.Entry(inputsFrame, textvariable=self.min_val, width=8, font=('Arial', 14), validate="key", validatecommand=min_vcmd)
        self.min_entry.grid(row=0, column=1, padx=8, pady=5)

        min_btns = tk.Frame(inputsFrame)
        min_btns.grid(row=0, column=2, padx=(0, 10))
        tk.Button(min_btns, text="▲", width=2, command=lambda: self._step("min", +1)).pack()
        tk.Button(min_btns, text="▼", width=2, command=lambda: self._step("min", -1)).pack()

        tk.Label(inputsFrame, text="Max:", font=('Arial', 14)).grid(row=0, column=3, padx=8, pady=5, sticky="e")
        self.max_entry = tk.Entry(inputsFrame, textvariable=self.max_val, width=8, font=('Arial', 14), validate="key", validatecommand=max_vcmd)
        self.max_entry.grid(row=0, column=4, padx=8, pady=5)

        max_btns = tk.Frame(inputsFrame)
        max_btns.grid(row=0, column=5)
        tk.Button(max_btns, text="▲", width=2, command=lambda: self._step("max", +1)).pack()
        tk.Button(max_btns, text="▼", width=2, command=lambda: self._step("max", -1)).pack()

        ##self.min_val.trace_add("write", lambda *args: self._enforce_after_change("min"))
        ##self.max_val.trace_add("write", lambda *args: self._enforce_after_change("max"))



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
        
        return True
        
    
    def _validate_min(self, proposed: str) -> bool:
        print("VALIDATE MIN called with:", repr(proposed))
        # Proposed is what the entry would become after the keystroke
        return self._is_valid_int(proposed)
        """
        if not self._is_valid_int(proposed):
            return False
        
        try:
            max_v = int(self.max_val.get())
        except ValueError:
            if proposed in ("", "-") or int(proposed) >= -9999999:
                return True
            else:
                return False

        return proposed in ("", "-") or (int(proposed) <= max_v and int(proposed) >= -9999999)
        """
        
    

    def _validate_max(self, proposed: str) -> bool:
        print("VALIDATE MAX called with:", repr(proposed))
        # Proposed is what the entry would become after the keystroke
        return self._is_valid_int(proposed)
        """
        if not self._is_valid_int(proposed):
            return False

        try:
            min_v = int(self.min_val.get())
        except ValueError:
            if proposed in ("", "-") or int(proposed) <= 9999999:
                return True
            else:
                return False

        return proposed in ("", "-") or (int(proposed) >= min_v and int(proposed) <= 9999999)
        """




    def _enforce_after_change(self, which: str) -> None:
        if getattr(self, "_enforcing", False):
            return
        self._enforcing = True
        try:
            if which == "min":
                try:
                    min_v = int(self.min_val.get())
                except ValueError:
                    self.max_spin.config(from_=-9999999)
                    return
                self.max_spin.config(from_=min_v)
            else:
                try:
                    max_v = int(self.max_val.get())
                except ValueError:
                    self.min_spin.config(to=9999999)
                    return
                self.min_spin.config(to_=max_v)
        finally:
            self._enforcing = False











class playScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        computerNumberLabel = tk.Label(self, text="Computer Number: ???", font=('Arial', 20))
        computerNumberLabel.pack(padx=70, pady=20)



        



        



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