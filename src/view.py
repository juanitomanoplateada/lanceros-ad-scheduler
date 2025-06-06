# view.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Intervalo de guardado automático (60 segundos)
AUTO_SAVE_INTERVAL = 60_000


class AdSchedulerView:
    """
    Clase encargada de manejar la interfaz gráfica (GUI) de la aplicación
    de programación de cuñas para Lanceros Stereo 94.1 FM.
    """

    def __init__(self, master, controller):
        """
        Inicializa la vista principal con todos los elementos de la GUI.
        """
        self.master = master
        self.controller = controller
        self.master.title("Programación Lanceros Stereo 94.1 FM")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        # Diccionarios de referencia para slots
        self.slot_labels = {}
        self.check_vars = {}
        self.checkboxes = {}
        self.current_ad = None

        font_default = ("Helvetica", 9)

        # Entrada y botones superiores
        input_frame = tk.Frame(master)
        input_frame.grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(input_frame, text="CUÑA (0–99):", font=font_default).pack(side="left")
        vcmd = (master.register(self.validate_entry), "%P")
        self.entry_ad_number = tk.Entry(input_frame, width=5, validate="key", validatecommand=vcmd, font=font_default)
        self.entry_ad_number.pack(side="left")
        self.entry_ad_number.bind("<KeyRelease>", self.load_checkboxes_for_ad)

        tk.Button(input_frame, text="Borrar Cuña", font=font_default, command=self.delete_ad_from_all).pack(side="left", padx=10)
        tk.Button(input_frame, text="Exportar", font=font_default, command=self.controller.export_data).pack(side="left", padx=10)

        # Área principal con horarios
        self.slot_frame = tk.Frame(master)
        self.slot_frame.grid(row=1, column=0, columnspan=4)

        for row, hour in enumerate(self.controller.get_schedule().keys()):
            # Etiqueta de la hora
            tk.Label(self.slot_frame, text=hour, width=10, font=("Helvetica", 9, "bold")).grid(row=row, column=0, padx=5, pady=2)

            # Contenedor de cuñas para esa hora
            self.slot_labels[hour] = tk.Label(self.slot_frame, text="", width=40, anchor="w", bg="white", relief="sunken", font=font_default)
            self.slot_labels[hour].grid(row=row, column=1, padx=5)

            # Checkbox para activar/desactivar la cuña seleccionada
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.slot_frame, variable=var, command=lambda h=hour, v=var: self.toggle_ad_assignment(h, v), font=font_default)
            chk.grid(row=row, column=2)
            self.check_vars[hour] = var
            self.checkboxes[hour] = chk
            chk.grid_remove()  # Ocultar por defecto

        # Etiqueta de última modificación
        self.last_updated_label = tk.Label(master, text="Última modificación: ---", font=("Helvetica", 8), fg="gray")
        self.last_updated_label.grid(row=2, column=0, columnspan=4, pady=5)

        # Inicializaciones de interfaz
        self.highlight_upcoming_slot()
        self.create_overlay_widget()
        self.master.after(AUTO_SAVE_INTERVAL, self.auto_save)
        self.refresh_all_slot_labels()

    def refresh_all_slot_labels(self):
        """
        Refresca todas las etiquetas de horarios con las cuñas actuales.
        """
        for hour in self.slot_labels:
            ads = self.controller.get_schedule()[hour]
            self.slot_labels[hour].config(text=", ".join(map(str, sorted(ads))))

    def validate_entry(self, value):
        """
        Valida que la entrada sea un número de cuña entre 0 y 99.
        """
        return value == "" or (value.isdigit() and 0 <= int(value) <= 99)

    def confirm_exit(self):
        """
        Confirma si el usuario realmente quiere cerrar la aplicación.
        """
        if messagebox.askokcancel("Salir", "¿Cerrar la aplicación?"):
            self.master.destroy()

    def refresh_slot(self, hour):
        """
        Refresca visualmente una hora específica en la GUI.
        """
        ads = self.controller.get_schedule()[hour]
        self.slot_labels[hour].config(text=", ".join(map(str, sorted(ads))))

    def load_checkboxes_for_ad(self, event=None):
        """
        Al ingresar una cuña, muestra checkboxes para los horarios donde puede ser asignada.
        """
        value = self.entry_ad_number.get().strip()
        if not value:
            for chk in self.checkboxes.values():
                chk.grid_remove()
            self.current_ad = None
            return

        self.current_ad = int(value)
        for hour in self.controller.get_schedule():
            var = self.check_vars[hour]
            var.set(self.current_ad in self.controller.get_schedule()[hour])
            self.checkboxes[hour].grid()

    def toggle_ad_assignment(self, hour, var):
        """
        Agrega o elimina la cuña actual del horario correspondiente según el checkbox.
        """
        if self.current_ad is None:
            return
        self.controller.update_ad_in_slot(self.current_ad, hour, add=var.get())
        self.last_updated_label.config(text=f"Última modificación: {datetime.now().strftime('%H:%M:%S')}")

    def delete_ad_from_all(self):
        """
        Elimina la cuña actual de todos los horarios.
        """
        if self.current_ad is None:
            return
        if messagebox.askyesno("Eliminar Cuña", f"¿Eliminar la cuña {self.current_ad} de todos los horarios?"):
            self.controller.delete_ad_globally(self.current_ad)
            self.last_updated_label.config(text=f"Última modificación: {datetime.now().strftime('%H:%M:%S')}")

    def highlight_upcoming_slot(self):
        """
        Resalta el horario más próximo según la hora actual.
        """
        now = datetime.now()
        minute = 30 if now.minute < 30 else 0
        hour = now.hour + (1 if now.minute >= 30 else 0)
        upcoming = now.replace(hour=hour % 24, minute=minute, second=0, microsecond=0)
        label = upcoming.strftime("%I:%M%p").lstrip("0")

        for slot, lbl in self.slot_labels.items():
            lbl.config(bg="#FFD700" if slot == label else "white")

        self.master.after(30000, self.highlight_upcoming_slot)

    def create_overlay_widget(self):
        """
        Crea un widget flotante y siempre visible con los próximos 3 bloques programados.
        """
        self.overlay = tk.Toplevel(self.master)
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        self.overlay.attributes("-alpha", 0.75)
        self.overlay.configure(bg="black")
        self.overlay.geometry("+1280+20")

        title = tk.Label(self.overlay, text="PRÓXIMA PROGRAMACIÓN", font=("Helvetica", 14, "bold"), fg="white", bg="black", anchor="center")
        title.pack(padx=10, pady=(5, 10))

        self.hud_labels = []
        for _ in range(3):
            lbl = tk.Label(self.overlay, text="", font=("Helvetica", 12), fg="white", bg="black", anchor="w", width=30)
            lbl.pack(padx=10, pady=2)
            self.hud_labels.append(lbl)

        self.overlay.bind("<ButtonPress-1>", self.start_drag)
        self.overlay.bind("<B1-Motion>", self.perform_drag)
        self.update_overlay()

    def start_drag(self, event):
        """
        Guarda la posición inicial para permitir mover el widget flotante.
        """
        self.overlay._drag_start_x = event.x
        self.overlay._drag_start_y = event.y

    def perform_drag(self, event):
        """
        Permite mover el widget flotante arrastrándolo.
        """
        x = self.overlay.winfo_pointerx() - self.overlay._drag_start_x
        y = self.overlay.winfo_pointery() - self.overlay._drag_start_y
        self.overlay.geometry(f"+{x}+{y}")

    def update_overlay(self):
        """
        Actualiza el contenido del HUD flotante con los próximos 3 bloques.
        """
        schedule_keys = list(self.controller.get_schedule().keys())
        now = datetime.now()
        minute = 30 if now.minute < 30 else 0
        hour = now.hour + (1 if now.minute >= 30 else 0)
        current_time = now.replace(hour=hour % 24, minute=minute, second=0, microsecond=0)
        current_label = current_time.strftime("%I:%M%p").lstrip("0")

        try:
            idx = schedule_keys.index(current_label)
        except ValueError:
            idx = 0

        for i in range(3):
            if idx + i < len(schedule_keys):
                slot = schedule_keys[idx + i]
                ads = self.controller.get_schedule().get(slot, [])
                text = f"{slot}: {', '.join(map(str, sorted(ads)))}"
            else:
                text = ""
            self.hud_labels[i].config(text=text)

        self.master.after(30000, self.update_overlay)

    def auto_save(self):
        """
        Guarda automáticamente los cambios cada 60 segundos.
        """
        if self.current_ad is not None:
            self.controller.save_data()
            self.last_updated_label.config(text=f"Guardado automático: {datetime.now().strftime('%H:%M:%S')}")
        self.master.after(AUTO_SAVE_INTERVAL, self.auto_save)
