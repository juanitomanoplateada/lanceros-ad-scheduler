# main.py

# Importa Tkinter para la GUI
import tkinter as tk

# Importa el controlador y la vista del programador de cuñas
from app.controllers.controller import AdSchedulerController
from app.services.periodic_backup_service import PeriodicBackupService
from app.views.view import AdSchedulerView

# Importa la función que lanza el servidor Flask para mostrar la canción actual
from app.services.song_service import start_song_server

# Importa threading para ejecutar el servidor web en paralelo a la GUI
import threading

if __name__ == "__main__":
    # ============================
    # INICIO DEL SERVIDOR FLASK
    # ============================
    # Ejecuta el servidor de metadatos de canción en un hilo separado
    # Esto permite que la GUI y el servidor web corran simultáneamente
    flask_thread = threading.Thread(target=start_song_server, daemon=True)
    flask_thread.start()

    # Ruta del archivo original y la copia de seguridad
    original_file = r"C:\OtsLabs\Data\OtsAVDJ.oml"
    backup_file = r"C:\OtsLabs\Data\Backup\OtsAVDJ.oml"

    # Iniciar servicio de backup cada 30 minutos
    backup_service = PeriodicBackupService(original_file, backup_file, interval_minutes=30)
    backup_service.start()

    # ============================
    # INICIO DE LA INTERFAZ GRÁFICA
    # ============================
    # Crea la ventana principal de la aplicación con Tkinter
    root = tk.Tk()

    # Instancia el controlador y la vista
    controller = AdSchedulerController()
    view = AdSchedulerView(root, controller)

    # Establece la conexión entre el controlador y la vista
    controller.set_view(view)

    # Inicia el bucle principal de la interfaz gráfica
    root.mainloop()
