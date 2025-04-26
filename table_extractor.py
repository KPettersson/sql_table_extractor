'''import pandas as pd

# Inställningar
csv_file = r"C:\workspace\chatGPT-ETLövning\etl2\customers(1).csv"   # <-- Din CSV-fil
table_name = 'customers'     # <-- Ditt tabellnamn

# Läs in CSV (bara headers)
df = pd.read_csv(csv_file, nrows=0)

# Funktion för att gissa datatyper
def guess_datatype(column_name):
    name = column_name.lower()
    if 'id' in name:
        return 'INTEGER'
    elif 'date' in name:
        return 'DATE'
    elif any(x in name for x in ['amount', 'price', 'total']):
        return 'DECIMAL(10,2)'
    else:
        return 'NVARCHAR(255)'

# Bygg CREATE TABLE
columns = [f"    {col} {guess_datatype(col)}" for col in df.columns]
create_statement = f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);"

# Print till terminalen
print(create_statement)'''


import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Funktioner

def guess_datatype(column_name):
    name = column_name.lower()
    if 'id' in name:
        return 'INTEGER'
    elif 'date' in name:
        return 'DATE'
    elif any(x in name for x in ['amount', 'price', 'total']):
        return 'DECIMAL(10,2)'
    else:
        return 'NVARCHAR(255)'

def choose_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    df = pd.read_csv(file_path, nrows=0)

    for widget in columns_frame.winfo_children():
        widget.destroy()

    global checkboxes
    checkboxes = {}

    tk.Label(columns_frame, text="Markera Primary Key:", font=('Arial', 10, 'bold')).pack(pady=(5, 5))

    for col in df.columns:
        var = tk.IntVar()
        cb = tk.Checkbutton(columns_frame, text=col, variable=var, command=update_sql)
        cb.pack(anchor='w', padx=10)
        checkboxes[col] = var

    update_sql()

def update_sql(*args):
    table_name = table_name_entry.get()
    if not table_name:
        table_name = "my_table"

    columns = []

    for col, var in checkboxes.items():
        datatype = guess_datatype(col)
        if var.get():
            datatype += " PRIMARY KEY"
        columns.append(f"    {col} {datatype}")

    create_statement = f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);"

    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, create_statement)

def copy_to_clipboard():
    sql_code = output_text.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(sql_code.strip())
    root.update()  # Viktigt för att få det att funka på alla plattformar

# GUI Setup
root = tk.Tk()
root.title("CREATE TABLE Generator")
root.geometry("600x700")

# Tabellnamnsruta
tk.Label(root, text="Tabellnamn:").pack(pady=(10, 0))
table_name_entry = tk.Entry(root)
table_name_entry.pack(pady=(0, 10))
table_name_entry.bind("<KeyRelease>", update_sql)

# Knapp för att välja CSV
tk.Button(root, text="Välj CSV-fil", command=choose_csv).pack(pady=5)

# Kolumnlistan
columns_frame = tk.Frame(root)
columns_frame.pack(pady=10)

# Knapp för att kopiera till urklipp
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

# Resultatruta
output_text = tk.Text(root, height=20, width=80)
output_text.pack(pady=10)

# Starta GUI
root.mainloop()