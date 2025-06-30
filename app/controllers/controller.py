# controller.py

from tkinter import filedialog, messagebox
from app.models.model import AdSchedulerModel


class AdSchedulerController:
    """
    Controlador que maneja la lógica de negocio y coordinación entre el modelo (datos)
    y la vista (interfaz gráfica) en la aplicación de programación de cuñas radiales.
    """

    def __init__(self):
        # Inicializa el modelo que gestiona los datos
        self.model = AdSchedulerModel()
        # Se establece posteriormente desde la vista
        self.view = None

    def set_view(self, view):
        """
        Asocia la vista al controlador.
        Esto permite que el controlador invoque métodos de actualización en la interfaz.
        """
        self.view = view

    def get_schedule(self):
        """
        Retorna el diccionario completo de horarios y sus cuñas asignadas.
        """
        return self.model.schedule

    def save_data(self):
        """
        Guarda la programación actual en disco y crea un respaldo.
        """
        self.model.save_ad_data()

    def export_data(self):
        """
        Solicita al usuario una ubicación para guardar un archivo de exportación
        con la programación actual en formato .txt o .csv.
        """
        export_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")]
        )
        if export_path:
            self.model.export_schedule(export_path)
            messagebox.showinfo("Exportación", f"Programación exportada a:\n{export_path}")

    def update_ad_in_slot(self, ad_number, hour, add=True):
        """
        Asigna o elimina una cuña específica de un horario determinado.

        :param ad_number: número de la cuña a asignar o quitar
        :param hour: string del horario objetivo (ej: "6:30AM")
        :param add: booleano, True para agregar, False para quitar
        """
        slot_ads = self.model.schedule[hour]
        if add and ad_number not in slot_ads:
            slot_ads.append(ad_number)
        elif not add and ad_number in slot_ads:
            slot_ads.remove(ad_number)

        self.save_data()
        self.view.refresh_slot(hour)
        self.view.update_overlay()

    def delete_ad_globally(self, ad_number):
        """
        Elimina una cuña en todos los horarios donde haya sido previamente asignada.
        Actualiza tanto los datos como la interfaz.
        """
        for hour in self.model.schedule:
            if ad_number in self.model.schedule[hour]:
                self.model.schedule[hour].remove(ad_number)
                self.view.refresh_slot(hour)

        self.save_data()
        self.view.update_overlay()
