import keyboard
import coordinateCapture as CC
import tkinter as tk
from tkinter import ttk
import threading

class InputField(tk.Frame):
    def __init__(self, parent, name="Input", callback=None):
        super().__init__(parent, borderwidth=1, relief="solid", bg="white")
        
        # Configure grid layout (3 columns)
        self.columnconfigure(0, weight=1, uniform="col")
        self.columnconfigure(1, weight=2, uniform="col")
        self.columnconfigure(2, weight=1, uniform="col")

        # Label (Left 1/3)
        self.lbl_name = tk.Label(self, text=name, bg="white")
        self.lbl_name.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

        # Coordinate Entry Fields (Middle 1/3)
        self.ent_dist = tk.Entry(self, width=10, justify="center")
        self.ent_azim = tk.Entry(self, width=10, justify="center")
        self.ent_dist.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.ent_azim.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")

        # Button (Right 1/3)
        self.btn_set = tk.Button(self, text="+", command=lambda: self.on_click(callback))
        self.btn_set.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=5, pady=5)

    def on_click(self, callback):
        if callback:
            callback(self)


class Rangefinder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rangefinder v0.1")
        self.geometry("600x400")
        self.minsize(600,400)

        ash_blue = "#a4bfdb"
        topline = 0.05
        midline = 0.4

        self.current_Input = None
    
        self.lbl_state = tk.Label(self, text="READY")
        self.lbl_state.pack()

        self.frm_inputCoords = tk.Frame(self, borderwidth=2, relief="solid", bg="white")
        self.frm_inputCoords.place(relx=0, rely=topline, relwidth=midline, relheight=1)

        self.frm_shipVisual = tk.Frame(self, borderwidth=2, relief="solid", bg=ash_blue)
        self.frm_shipVisual.place(relx=midline, rely=topline, relwidth=1-midline, relheight=.6)

        self.frm_extraStats = tk.Frame(self, borderwidth=2, relief="solid", bg="white")
        self.frm_extraStats.place(relx=midline, rely=.6, relwidth=1-midline, relheight=1)

        self.input_target = InputField(self.frm_inputCoords, "Target", self.update_state)
        self.input_source1 = InputField(self.frm_inputCoords, "Source 1", self.update_state)
        self.input_source2 = InputField(self.frm_inputCoords, "Source 2", self.update_state)
        self.input_source3 = InputField(self.frm_inputCoords, "Source 3", self.update_state)
        self.input_target.pack(pady=10, padx=10, fill="x")
        self.input_source1.pack(pady=10, padx=10, fill="x")
        self.input_source2.pack(pady=10, padx=10, fill="x")
        self.input_source3.pack(pady=10, padx=10, fill="x")

        threading.Thread(target=self.listen_hotkeys, daemon=True).start()

    def update_state(self, input):
        self.current_Input = input
        # print(self.current_Input)

        stateText = f"[{self.current_Input.lbl_name.cget("text")}] LISTENING FOR INPUT".upper()
        self.lbl_state.config(text=stateText, fg="black")

    def capture_coordinates(self):
        if not self.current_Input:
            self.lbl_state.config(text="NO INPUT FIELD SELECTED!", fg="red")
            return
        
        distance, azimuth = CC.captureScreenshot()

        print(distance, azimuth)

        if distance:
            self.current_Input.ent_dist.delete(0, tk.END)
            self.current_Input.ent_dist.insert(0, distance)

        if azimuth:
            self.current_Input.ent_azim.delete(0, tk.END)
            self.current_Input.ent_azim.insert(0, azimuth)

        stateText = f"[{self.current_Input.lbl_name.cget("text")}] COORDINATES UPDATED"
        if not distance or not azimuth:
            stateText += " (ERROR)"
        self.lbl_state.config(text=stateText, fg="black")

    def listen_hotkeys(self):
        keyboard.add_hotkey('c', self.capture_coordinates)
        keyboard.wait()


def main():
    # keyboard.add_hotkey('p', app.capture_coordinates())
    # keyboard.wait('esc')

    # coordinates = CC.readScreenshot()
    # print(coordinates)

    app = Rangefinder()
    app.mainloop()


# prevents main from running when imported as a library
if __name__ == "__main__":
    main()