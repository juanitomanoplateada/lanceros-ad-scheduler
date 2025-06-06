# model.py

import json
import os
from datetime import datetime, timedelta

# Ruta del archivo principal de datos
DATA_FILE = "data/ads_data.json"

# Carpeta para respaldos automáticos diarios
BACKUP_DIR = "data/backups"


class AdSchedulerModel:
    """
    Modelo encargado de gestionar la lógica de almacenamiento de la programación
    de cuñas para la emisora Lanceros Stereo 94.1 FM.
    """

    def __init__(self):
        # Carga la programación desde archivo o genera una nueva estructura vacía
        self.schedule = self.load_ad_data()

    def load_ad_data(self):
        """
        Carga los datos de programación desde el archivo JSON.
        Si el archivo no existe, se genera una estructura de horarios desde 5:30AM a 8:30PM en intervalos de 30 minutos.
        """
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Genera estructura por defecto si no hay archivo previo
            start_time = datetime.strptime("5:30AM", "%I:%M%p")
            end_time = datetime.strptime("8:30PM", "%I:%M%p")
            schedule = {}
            current_time = start_time

            while current_time <= end_time:
                label = current_time.strftime("%I:%M%p").lstrip("0")  # Ej: "5:30AM"
                schedule[label] = []  # Lista vacía de cuñas para cada horario
                current_time += timedelta(minutes=30)

            return schedule

    def save_ad_data(self):
        """
        Guarda el contenido actual de la programación tanto en el archivo principal como en una copia de respaldo.
        El respaldo diario se almacena con la fecha en el nombre del archivo.
        """
        # Guardado principal
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.schedule, f, indent=2)

        # Respaldo diario
        os.makedirs(BACKUP_DIR, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        backup_path = os.path.join(BACKUP_DIR, f"{today}_ads_backup.json")
        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(self.schedule, f, indent=2)

    def export_schedule(self, export_path):
        """
        Exporta la programación actual a un archivo de texto plano.
        Cada línea representa un horario y su lista de cuñas.
        """
        with open(export_path, "w", encoding="utf-8") as f:
            for slot, ads in self.schedule.items():
                f.write(f"{slot}: {', '.join(map(str, sorted(ads)))}\n")
