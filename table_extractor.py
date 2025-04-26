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

    tk.Label(columns_frame, text="Primary Key:", font=('Arial', 10, 'bold')).pack(pady=(5, 5))

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
    root.update()


root = tk.Tk()
root.title("CREATE TABLE Generator")
root.geometry("600x700")


tk.Label(root, text="Table name:").pack(pady=(10, 0))
table_name_entry = tk.Entry(root)
table_name_entry.pack(pady=(0, 10))
table_name_entry.bind("<KeyRelease>", update_sql)


tk.Button(root, text="Choose CSV-file", command=choose_csv).pack(pady=5)


columns_frame = tk.Frame(root)
columns_frame.pack(pady=10)


tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)


output_text = tk.Text(root, height=20, width=80)
output_text.pack(pady=10)

root.mainloop()