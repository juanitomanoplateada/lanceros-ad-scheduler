import os
import shutil
import threading
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PeriodicBackupService:
    def __init__(self, source_file: str, backup_file: str, interval_minutes: float = 30):
        """
        Inicializa el servicio de copia de seguridad periódica.

        :param source_file: Ruta completa del archivo a respaldar.
        :param backup_file: Ruta completa del archivo de respaldo (se sobrescribe).
        :param interval_minutes: Tiempo en minutos entre respaldos. Acepta decimales.
        """
        self.source_file = source_file
        self.backup_file = backup_file
        self.interval = interval_minutes * 60  # convertir a segundos
        self.thread = threading.Thread(target=self._run, daemon=True)
        self._stop_event = threading.Event()

    def start(self):
        logging.info("Iniciando servicio de copia de seguridad periódica...")
        self.thread.start()

    def stop(self):
        logging.info("Deteniendo servicio de copia de seguridad.")
        self._stop_event.set()

    def _run(self):
        while not self._stop_event.is_set():
            try:
                if os.path.exists(self.source_file):
                    # Validar permisos
                    if not os.access(self.source_file, os.R_OK):
                        logging.warning(f"No se puede leer el archivo: {self.source_file}")
                    elif not os.access(os.path.dirname(self.backup_file), os.W_OK):
                        logging.warning(f"No se puede escribir en: {os.path.dirname(self.backup_file)}")
                    else:
                        # Crear carpeta de respaldo si no existe
                        os.makedirs(os.path.dirname(self.backup_file), exist_ok=True)

                        # Copiar el archivo (con metadatos)
                        shutil.copy2(self.source_file, self.backup_file)
                        logging.info(f"Copia de seguridad actualizada: {self.backup_file}")
                else:
                    logging.warning(f"Archivo fuente no encontrado: {self.source_file}")
            except Exception as e:
                logging.error(f"Error al copiar archivo: {e}")
            time.sleep(self.interval)
