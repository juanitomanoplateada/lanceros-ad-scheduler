# main.py
import tkinter as tk
from controller import AdSchedulerController
from view import AdSchedulerView

if __name__ == "__main__":
    root = tk.Tk()
    controller = AdSchedulerController()
    view = AdSchedulerView(root, controller)
    controller.set_view(view)
    root.mainloop()
