# main.py
import tkinter as tk
from controller import AdSchedulerController
from view import AdSchedulerView
from song_service import start_song_server
import threading

if __name__ == "__main__":
    # Iniciar servidor Flask en hilo separado
    flask_thread = threading.Thread(target=start_song_server, daemon=True)
    flask_thread.start()

    # Iniciar interfaz gráfica
    root = tk.Tk()
    controller = AdSchedulerController()
    view = AdSchedulerView(root, controller)
    controller.set_view(view)
    root.mainloop()
