# controller.py
from tkinter import filedialog, messagebox
from datetime import datetime
from model import AdSchedulerModel


class AdSchedulerController:

    def __init__(self):
        self.model = AdSchedulerModel()
        self.view = None

    def set_view(self, view):
        self.view = view

    def get_schedule(self):
        return self.model.schedule

    def save_data(self):
        self.model.save_ad_data()

    def export_data(self):
        export_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        if export_path:
            self.model.export_schedule(export_path)
            messagebox.showinfo("Exportación", f"Programación exportada a:\n{export_path}")

    def update_ad_in_slot(self, ad_number, hour, add=True):
        slot_ads = self.model.schedule[hour]
        if add and ad_number not in slot_ads:
            slot_ads.append(ad_number)
        elif not add and ad_number in slot_ads:
            slot_ads.remove(ad_number)
        self.save_data()
        self.view.refresh_slot(hour)
        self.view.update_overlay()

    def delete_ad_globally(self, ad_number):
        for hour in self.model.schedule:
            if ad_number in self.model.schedule[hour]:
                self.model.schedule[hour].remove(ad_number)
                self.view.refresh_slot(hour)
        self.save_data()
        self.view.update_overlay()
