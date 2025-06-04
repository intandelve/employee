import csv
import pandas as pd
from tkinter import filedialog, messagebox

def export_to_csv(treeview, filename):
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(["Employee Name", "Base Salary", "Bonus", "Deductions", "Net Pay"])

            # Write data from the table
            for row in treeview.get_children():
                values = treeview.item(row)["values"]
                writer.writerow([value.replace("$", "").replace(",", "") for value in values])

        messagebox.showinfo("Success", f"Report successfully exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export report:\n{e}")

def export_to_excel(treeview, filename):
    try:
        # Prepare data from treeview
        data = []
        for row in treeview.get_children():
            values = treeview.item(row)["values"]
            data.append(values)

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data, columns=["Employee Name", "Base Salary", "Bonus", "Deductions", "Net Pay"])

        # Save to Excel
        df.to_excel(filename, index=False)

        messagebox.showinfo("Success", f"Report successfully exported to {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export report:\n{e}")
