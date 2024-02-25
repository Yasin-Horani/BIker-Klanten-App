import tkinter as tk
from tkinter import ttk, messagebox
import csv
from tkinter import PhotoImage
import re


class CustomerManagementApp:
    def __init__(self, root):
        # Variables
        self.root = root
        self.root.title("Klantbeheer App")
        self.customer_data = []
        self.klantnummer = tk.StringVar(value="Het klantnummer wordt automatisch toegevoegd.")
        self.selected_customer = tk.StringVar()
        self.search_text = tk.StringVar()
        self.voornaam = tk.StringVar()
        self.achternaam = tk.StringVar()
        self.straatnaam = tk.StringVar()
        self.nummer = tk.StringVar()
        self.postcode = tk.StringVar()
        self.woonplaats = tk.StringVar()
        self.geboortedatum = tk.StringVar()

        # Navigation Buttons
        ttk.Button(root, text="Klanten", command=self.customuer_navigation).grid(row=1, column=2, padx=25, pady=10)
        ttk.Button(root, text="Medewerker").grid(row=1, column=3, padx=1, pady=10)
        ttk.Button(root, text="Artikel").grid(row=1, column=4, padx=1, pady=10)
        ttk.Button(root, text="Huurovereenkomst").grid(row=1, column=5, padx=1, pady=10)
        ttk.Button(root, text="Reparatie").grid(row=1, column=6, padx=1, pady=10)

        # Labels
        ttk.Label(root, text="Klant gegevens", font=("Helvetica", 18)).place(x=80, y=75)
        self.aantal_label = ttk.Label(root, text="Aantal klanten: 0", font=("Helvetica", 12))
        self.aantal_label.place(x=480, y=80)

        # Entry for Search
        ttk.Entry(root, textvariable=self.search_text, width=30).place(x=800, y=70)

        # Search Button
        ttk.Button(root, text="Zoeken", command=self.search_customers).place(x=1050, y=70)

        # Klant gegevens lables
        ttk.Label(root, text="Klantnummer: ", font=("Helvetica", 10)).place(x=30, y=120)
        ttk.Label(root, text="Voornaam: ", font=("Helvetica", 10)).place(x=30, y=155)
        ttk.Label(root, text="Achternaam:", font=("Helvetica", 10)).place(x=30, y=195)
        ttk.Label(root, text="Straatnaam:", font=("Helvetica", 10)).place(x=30, y=235)
        ttk.Label(root, text="Nummer:", font=("Helvetica", 10)).place(x=30, y=275)
        ttk.Label(root, text="Postcode:", font=("Helvetica", 10)).place(x=30, y=315)
        ttk.Label(root, text="Woonplaats:", font=("Helvetica", 10)).place(x=30, y=355)
        ttk.Label(root, text="Geboortedatum:", font=("Helvetica", 10)).place(x=30, y=395)

        # Klant gegevens Entry
        ttk.Label(root, textvariable=self.klantnummer, text="Het klantnummer wordt automatisch toegevoegd.",
                  font=("Helvetica", 10)).place(x=150, y=120)
        # validate strings
        just_string_input = root.register(self.validate_input)
        ttk.Entry(root, textvariable=self.voornaam, width=40, validate="key",
                  validatecommand=(just_string_input, "%P")).place(x=150, y=150)
        ttk.Entry(root, textvariable=self.achternaam, width=40, validate="key",
                  validatecommand=(just_string_input, "%P")).place(x=150, y=190)
        ttk.Entry(root, textvariable=self.straatnaam, width=40, validate="key",
                  validatecommand=(just_string_input, "%P")).place(x=150, y=230)
        ttk.Entry(root, textvariable=self.nummer, width=40).place(x=150, y=270)

        # validate Postcode
        postcode_validation = root.register(self.validate_postcode)
        ttk.Entry(root, textvariable=self.postcode, width=40, validate="key",
                  validatecommand=(postcode_validation, "%P")).place(x=150, y=310)
        ttk.Entry(root, textvariable=self.woonplaats, width=40, validate="key",
                  validatecommand=(just_string_input, "%P")).place(x=150, y=350)

        ttk.Entry(root, textvariable=self.geboortedatum, width=40).place(x=150, y=390)

        # OptionMenu
        ttk.Label(root,
                  text="Klantnummer | Voornaam | Achternaam | Straatnaam | Nummer | Postcode | Woonplaats | Geboortedatum").place(
            x=470, y=120)
        self.customer_menu = ttk.OptionMenu(root, self.selected_customer, "Selecteer een klant")
        self.customer_menu.place(x=470, y=140)

        # Opslaan Button
        ttk.Button(root, text="Opslaan", command=self.save_customer).place(x=30, y=450)
        # refresh Button
        ttk.Button(root, text="Annuleren", command=self.clear_fields).place(x=170, y=450)
        # Wijzigen Button
        ttk.Button(root, text="Wijzigen", command=self.update_customer).place(x=480, y=450)
        # Verwijderen Button
        ttk.Button(root, text="Verwijderen", command=self.delete_customer).place(x=580, y=450)
        # Alles tonen Button
        ttk.Button(root, text="Alles tonen", command=self.show_all_customers).place(x=680, y=450)

        # Logo
        image_path = "logo.png"
        self.logo_image = PhotoImage(file=image_path)
        desired_width = 150
        self.logo_image = self.logo_image.subsample(int(self.logo_image.width() / desired_width))
        self.logo_label = ttk.Label(root, image=self.logo_image)
        self.logo_label.place(x=950, y=350)

        ttk.Label(root, text="Copyright Yasin Horani!", font=("Helvetica", 7)).place(x=580, y=520)
        # switch mode
        # self.mode_switch = ttk.Checkbutton(root, text="Mode", style="Switch", command=self.toggle_mode)
        # self.mode_switch.place(x=1100, y=520)

        # functions
        self.load_customer_data()

    def customuer_navigation(self):
        messagebox.showinfo("Navigatie", "klanten Button Clicked")

    def validate_input(self, char_value):
        return all(char.isalpha() or char.isspace() for char in char_value)

    # klant opslaan
    def save_customer(self):
        last_customer_number = self.get_last_customer_number()
        new_customer_number = last_customer_number + 1

        self.klantnummer.set(new_customer_number)
        first_name = self.voornaam.get()
        last_name = self.achternaam.get()
        street = self.straatnaam.get()
        number = self.nummer.get()
        zipcode = self.postcode.get()
        place = self.woonplaats.get()
        date_of_birth = self.geboortedatum.get()

        if not first_name or not last_name or not street or not number or not zipcode or not place or not date_of_birth:
            messagebox.showerror("Error", "Vul alle verplichte velden in.")
            return

        main_file_path = "Klanten_data.csv"
        backup_file_path = "Klanten_data_backup.csv"

        with open(main_file_path, mode="a", newline='') as main_file:
            main_writer = csv.writer(main_file)
            main_writer.writerow(
                [new_customer_number, first_name, last_name, street, number, zipcode, place, date_of_birth])

        # Write to the backup file
        with open(backup_file_path, mode="a", newline='') as backup_file:
            backup_writer = csv.writer(backup_file)
            backup_writer.writerow(
                [new_customer_number, first_name, last_name, street, number, zipcode, place, date_of_birth])
        self.clear_fields()
        self.load_customer_data()
        messagebox.showinfo("Success", "Klantgegevens succesvol opgeslagen.")

    def get_last_customer_number(self):
        try:
            with open("Klanten_data.csv", mode="r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                if rows:
                    last_customer_number = int(rows[-1][0])
                    return last_customer_number
                else:
                    return 0
        except:
            return "Data Error"

    def clear_fields(self):
        self.klantnummer.set("Het klantnummer wordt automatisch toegevoegd.")
        self.voornaam.set("")
        self.achternaam.set("")
        self.straatnaam.set("")
        self.nummer.set("")
        self.postcode.set("")
        self.woonplaats.set("")
        self.geboortedatum.set("")
        self.search_text.set("")
        self.aantal_label["text"] = f"Aantal klanten: 0"
        self.selected_customer.set("Selecteer een klant")

    # update customer menu
    def update_customer_menu(self):
        self.customer_menu["menu"].delete(0, "end")
        for customer in self.customer_data:
            label = f"{customer[0]}    |    {customer[1]}    |    {customer[2]}    |    {customer[3]}    |    {customer[4]}    |    {customer[5]}    |    {customer[6]}    |    {customer[7]}"
            self.customer_menu["menu"].add_command(label=label, command=lambda c=label: self.set_selected_customer(c))

    # Select widget functions
    def set_selected_customer(self, customer_label):
        self.selected_customer.set(customer_label)
        selected_customer_id = customer_label.split()[0]
        selected_customer = None
        for customer in self.customer_data:
            if customer[0] == selected_customer_id:
                selected_customer = customer
                break

        if selected_customer:
            self.klantnummer.set(selected_customer[0])
            self.voornaam.set(selected_customer[1])
            self.achternaam.set(selected_customer[2])
            self.straatnaam.set(selected_customer[3])
            self.nummer.set(selected_customer[4])
            self.postcode.set(selected_customer[5])
            self.woonplaats.set(selected_customer[6])
            self.geboortedatum.set(selected_customer[7])

    # load customer data
    def load_customer_data(self):
        try:
            with open("Klanten_data.csv", mode="r") as file:
                reader = csv.reader(file)
                header = next(reader)
                self.customer_data = [row[0::] for row in reader]
                aantal_klanten = len(self.customer_data)
                self.aantal_label["text"] = f"Aantal klanten: {aantal_klanten}"
            self.update_customer_menu()
        except:
            self.customer_data = []

    def show_all_customers(self):
        self.load_customer_data()

    # update customer
    def update_customer(self):
        selected_customer_id = self.klantnummer.get()
        if not selected_customer_id or selected_customer_id == "Het klantnummer wordt automatisch toegevoegd.":
            messagebox.showerror("Error", "Selecteer een klant om te wijzigen.")
            return

        # Get updated data
        first_name = self.voornaam.get()
        last_name = self.achternaam.get()
        street = self.straatnaam.get()
        number = self.nummer.get()
        zipcode = self.postcode.get()
        place = self.woonplaats.get()
        date_of_birth = self.geboortedatum.get()

        if not first_name or not last_name or not street or not number or not zipcode or not place or not date_of_birth:
            messagebox.showerror("Error", "Vul alle verplichte velden in.")
            return
        try:
            file_path = "Klanten_data.csv"
            with open(file_path, mode="r", newline='') as infile:
                reader = csv.reader(infile)
                rows = list(reader)
            for row in rows:
                if row[0] == selected_customer_id:
                    row[1:] = [first_name, last_name, street, number, zipcode, place, date_of_birth]

            with open(file_path, mode="w", newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(rows)
            self.clear_fields()
            self.load_customer_data()
            messagebox.showinfo("Success", "Klantgegevens succesvol gewijzigd.")
        except Exception as e:
            messagebox.showerror("Error", f"Fout bij het wijzigen van klantgegevens: {e}")

    # Delete function
    def delete_customer(self):
        selected_customer_id = self.klantnummer.get()
        if not selected_customer_id or selected_customer_id == "Het klantnummer wordt automatisch toegevoegd.":
            messagebox.showerror("Error", "Selecteer een klant om te verwijderen.")
            return
        self.customer_data = [customer for customer in self.customer_data if customer[0] != selected_customer_id]
        try:
            file_path = "Klanten_data.csv"
            with open(file_path, mode="w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["Klantnummer", "Voornaam", "Achternaam", "Straatnaam", "Nummer", "Postcode", "Woonplaats",
                     "Geboortedatum"])
                writer.writerows(self.customer_data)

            self.clear_fields()
            self.load_customer_data()

            messagebox.showinfo("Success", "Klantgegevens succesvol verwijderd.")
        except Exception as e:
            messagebox.showerror("Error", f"Fout bij het verwijderen van klantgegevens: {e}")

    def search_customers(self):
        search_term = self.search_text.get().lower()

        if not search_term:
            # If the search term is empty, show all customers
            self.show_all_customers()
        else:
            # Filter customers based on the search term
            filtered_customers = [customer for customer in self.customer_data if
                                  search_term in [str(value).lower() for value in customer]]
            # Update the customer data and the menu
            self.customer_data = filtered_customers
            self.update_customer_menu()
            self.load_customer_data()
            # If there are matching customers, select the first one and populate the data
            if filtered_customers:
                selected_customer_label = f"{filtered_customers[0][0]}    |    {filtered_customers[0][1]}    |    {filtered_customers[0][2]}    |    {filtered_customers[0][3]}    |    {filtered_customers[0][4]}    |    {filtered_customers[0][5]}    |    {filtered_customers[0][6]}    |    {filtered_customers[0][7]}"
                self.set_selected_customer(selected_customer_label)
            else:
                messagebox.showinfo("No Data", "No Data.")

    def validate_postcode(self, filterd_postcode):
        # print(f"test: {filterd_postcode}")
        return bool(re.match(r'^\d{0,4}[A-Z]{0,2}$', filterd_postcode.upper()))

    def toggle_mode(self):
        if self.mode_switch.instate(["selected"]):
            style.theme_use("forest-light")
        else:
            style.theme_use("forest-dark")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    root.tk.call("source", "forest-light.tcl")
    #root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-light")
    root.geometry("1200x550")
    root.resizable(False, False)
    app = CustomerManagementApp(root)
    root.mainloop()

print("copyright Yasin Horani (～￣▽￣)～  -.-- .- ... .. -. / .... --- .-. .- -. ..")


