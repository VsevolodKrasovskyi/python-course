import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class EconomicTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Services")
        
        self.data_files = ["cars.txt"]
        self.car_data = []
        self.repair_folder = "repairs"
        
        self.read_files()
        self.create_widgets()
        
        if not os.path.exists(self.repair_folder):
            os.makedirs(self.repair_folder)

    def read_files(self):
        for file in self.data_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=',')  
                    if file == "cars.txt":
                        self.car_data = []
                        for row in reader:
                            self.car_data.append(row)
            except FileNotFoundError:
                messagebox.showerror("Грешка", f"Файлът {file} не е намерен.")
            except Exception as e:
                messagebox.showerror("Грешка", f"Възникна грешка при четене на {file}: {e}")

    def write_file(self, file_name, data):
        try:
            with open(file_name, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerows(data)
        except Exception as e:
            messagebox.showerror("Грешка", f"Възникна грешка при запис в файла: {e}")

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Коли")
        
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="Търсене по VIN")
        
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text="Добавяне на кола")
        
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab4, text="Управление на ремонти")

        self.tab5 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab5, text="Премахване на данни")  # Новая вкладка для удаления

        self.tab_control.pack(expand=1, fill="both")
        
        self.visualize_data(self.tab1)
        self.create_search_data_widgets(self.tab2)
        self.create_add_data_widgets(self.tab3)
        self.create_manage_repair_widgets(self.tab4)
        self.create_delete_data_widgets(self.tab5)  # Создаем виджеты на новой вкладке

    def visualize_data(self, tab):
        columns = ["Марка", "Модел", "Година", "VIN", "Цвят", "Обем на двигателя", "Модификация на двигателя", "Конски сили", "Тип гориво"]
        
        self.car_data_tree = ttk.Treeview(tab, columns=columns, show='headings')
        for col in columns:
            self.car_data_tree.heading(col, text=col)
            self.car_data_tree.column(col, width=100, anchor='center') 
        self.car_data_tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        for row in self.car_data:
            self.car_data_tree.insert('', tk.END, values=row)
        
        self.car_data_tree.bind("<Button-3>", self.show_context_menu)
        
        self.context_menu = tk.Menu(self.car_data_tree, tearoff=0)
        self.context_menu.add_command(label="Копирай VIN", command=self.copy_selected_row)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_row(self):
        selected_item = self.car_data_tree.selection()
        if selected_item:
            row_data = self.car_data_tree.item(selected_item, 'values')
            vin = row_data[3]  # Assuming VIN is the fourth column (index 3)
            self.root.clipboard_clear()
            self.root.clipboard_append(vin)
            # messagebox.showinfo("Информация", "VIN номерът е копиран в клипборда.")

    def create_search_data_widgets(self, tab):
        search_label = ctk.CTkLabel(tab, text="Въведете VIN номер:")
        search_label.pack(pady=5)
        
        self.search_entry = ctk.CTkEntry(tab)
        self.search_entry.pack(pady=5)

        paste_vin_button = ctk.CTkButton(tab, text="Поставете VIN", command=self.paste_vin2)
        paste_vin_button.pack(pady=5)

        search_button = ctk.CTkButton(tab, text="Търсене", command=self.search)
        search_button.pack(pady=5)
        
        columns = ["Марка", "Модел", "Година", "VIN", "Цвят", "Обем на двигателя", "Модификация на двигателя", "Конски сили", "Тип гориво"]
        self.search_tree = ttk.Treeview(tab, columns=columns, show='headings')
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=100)
        self.search_tree.pack(expand=True, fill="both")

    def search(self):
        vin = self.search_entry.get()
        results = [row for row in self.car_data if len(row) > 3 and row[3] == vin]  # Проверяем длину строки
        for row in self.search_tree.get_children():
            self.search_tree.delete(row)
        if results:
            for result in results:
                self.search_tree.insert('', tk.END, values=result)
        else:
            messagebox.showinfo("Информация", "Не е намерен автомобил с посочения VIN номер.")

    def create_add_data_widgets(self, tab):
        labels = ["Марка", "Модел", "Година", "VIN", "Цвят", "Обем на двигателя", "Модификация на двигателя", "Конски сили", "Тип гориво"]
        self.entries = {}
        
        container = ctk.CTkFrame(tab)
        container.pack(pady=20, padx=20, fill='both', expand=True)
        
        for i, label in enumerate(labels):
            lbl = ctk.CTkLabel(container, text=label, width=20, anchor='w')
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            
            entry = ctk.CTkEntry(container, width=300)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
            self.entries[label] = entry

        add_button = ctk.CTkButton(container, text="Добави", command=self.add_car)
        add_button.grid(row=len(labels), column=0, columnspan=2, pady=20)
        
    def add_car(self):
        car = []
        for key, entry in self.entries.items():
            car.append(entry.get())
        
        if len(car) != 9 or not all(car):
            messagebox.showinfo("Грешка", "Невалиден формат на въвеждане")
        else:
            self.car_data.append(car)
            self.write_file("cars.txt", self.car_data)  # Записване на обновените данни във файла
            self.update_car_data_tree()
            messagebox.showinfo("Информация", "Автомобилът е добавен")

    def update_car_data_tree(self):
        for row in self.car_data_tree.get_children():
            self.car_data_tree.delete(row)
        for row in self.car_data:
            self.car_data_tree.insert('', tk.END, values=row)

    def create_manage_repair_widgets(self, tab):
        container = ctk.CTkFrame(tab)
        container.pack(pady=20, padx=20, fill='both', expand=True)

        vin_label = ctk.CTkLabel(container, text="Въведете VIN за управление на ремонти:")
        vin_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
        
        self.vin_entry = ctk.CTkEntry(container, width=300)
        self.vin_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        paste_vin_button = ctk.CTkButton(container, text="Поставете VIN", command=self.paste_vin)
        paste_vin_button.grid(row=0, column=2, padx=10, pady=5)

        search_vin_button = ctk.CTkButton(container, text="Търсене", command=self.search_repairs)
        search_vin_button.grid(row=0, column=3, padx=10, pady=5)

        self.repair_tree = ttk.Treeview(container, columns=["Дата", "Описание", "Цена"], show='headings')
        for col in ["Дата", "Описание", "Цена"]:
            self.repair_tree.heading(col, text=col)
            self.repair_tree.column(col, width=100)
        self.repair_tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        container.rowconfigure(1, weight=1)
        container.columnconfigure(1, weight=1)

        add_repair_label = ctk.CTkLabel(container, text="Добавете ремонт (дата описание цена):")
        add_repair_label.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky='w')

        self.add_repair_entries = {}
        repair_labels = ["Дата", "Описание", "Цена"]
        for i, label in enumerate(repair_labels):
            lbl = ctk.CTkLabel(container, text=label)
            lbl.grid(row=3+i, column=0, padx=10, pady=5, sticky='w')
            
            entry = ctk.CTkEntry(container, width=300)
            entry.grid(row=3+i, column=1, columnspan=3, padx=10, pady=5, sticky='ew')
            self.add_repair_entries[label] = entry

        add_repair_button = ctk.CTkButton(container, text="Добави ремонт", command=self.add_repair)
        add_repair_button.grid(row=6, column=0, columnspan=4, pady=20)


#paste vincode
    def paste_vin(self):
        try:
            vin = self.root.clipboard_get()
            self.vin_entry.delete(0, tk.END)
            self.vin_entry.insert(0, vin)
        except tk.TclError:
            messagebox.showinfo("Грешка", "Клипбордът е празен или не съдържа валидни данни.")

    def paste_vin2(self):
        try:
            vin2 = self.root.clipboard_get()
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, vin2)
        except tk.TclError:
            messagebox.showinfo("Грешка", "Клипбордът е празен или не съдържа валидни данни.")

    def paste_vin3(self):
        try:
            vin3 = self.root.clipboard_get()
            self.delete_entry.delete(0, tk.END)
            self.delete_entry.insert(0, vin3)
        except tk.TclError:
            messagebox.showinfo("Грешка", "Клипбордът е празен или не съдържа валидни данни.")


    def search_repairs(self):
        vin = self.vin_entry.get()
        repair_file = os.path.join(self.repair_folder, f"{vin}.txt")
        for row in self.repair_tree.get_children():
            self.repair_tree.delete(row)
        if os.path.exists(repair_file):
            with open(repair_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ')
                for repair in reader:
                    self.repair_tree.insert('', tk.END, values=repair)
        else:
            messagebox.showinfo("Информация", "Не са намерени ремонти за посочения VIN номер.")

    def add_repair(self):
        vin = self.vin_entry.get()
        repair = []
        for key, entry in self.add_repair_entries.items():
            repair.append(entry.get())

        if len(repair) != 3 or not all(repair):
            messagebox.showinfo("Грешка", "Невалиден формат на въвеждане")
        else:
            repair_file = os.path.join(self.repair_folder, f"{vin}.txt")
            with open(repair_file, 'a', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=' ')
                writer.writerow(repair)
            self.update_repair_tree(vin)
            messagebox.showinfo("Информация", "Ремонтът е добавен")

    def update_repair_tree(self, vin):
        for row in self.repair_tree.get_children():
            self.repair_tree.delete(row)
        repair_file = os.path.join(self.repair_folder, f"{vin}.txt")
        if os.path.exists(repair_file):
            with open(repair_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ')
                for repair in reader:
                    self.repair_tree.insert('', tk.END, values=repair)

    def create_delete_data_widgets(self, tab):
        delete_label = ctk.CTkLabel(tab, text="Въведете VIN номер за премахване:")
        delete_label.pack(pady=5)
        
        self.delete_entry = ctk.CTkEntry(tab, width=300)
        self.delete_entry.pack(pady=5)

        paste_vin_button = ctk.CTkButton(tab, text="Поставете VIN", command=self.paste_vin3)
        paste_vin_button.pack(pady=5)

        delete_button = ctk.CTkButton(tab, text="Премахване", command=self.confirm_delete)
        delete_button.pack(pady=10)

    def confirm_delete(self):
        vin = self.delete_entry.get()
        if not vin:
            messagebox.showwarning("Предупреждение", "Моля, въведете VIN номер.")
            return
        
        result = messagebox.askyesno("Потвърждение", f"Сигурни ли сте, че искате да премахнете автомобила с VIN: {vin}?")
        if result:
            self.delete_car(vin)

    def delete_car(self, vin):
        car_to_delete = None
        for car in self.car_data:
            if len(car) > 3 and car[3] == vin:
                car_to_delete = car
                break
        
        if car_to_delete:
            self.car_data.remove(car_to_delete)
            self.write_file("cars.txt", self.car_data)  # Обновляем файл с данными
            self.update_car_data_tree()
            messagebox.showinfo("Информация", "Автомобилът е премахнат успешно.")
        else:
            messagebox.showwarning("Предупреждение", "Автомобилът с този VIN номер не е намерен.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EconomicTaskApp(root)
    root.mainloop()
