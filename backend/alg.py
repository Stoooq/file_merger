import csv
import os
import pandas as pd
from collections import defaultdict
 
input_dir = "file_in"
output_dir = "file_out"
 
os.makedirs(output_dir, exist_ok=True)
 
for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    base_name, ext = os.path.splitext(filename)
    ext = ext.lower()
 
    # ---- Wczytywanie CSV ----
    if ext == ".csv":
        groups = defaultdict(list)
        with open(file_path, newline='', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if len(row) > 1:
                    level = row[1]   # kolumna B
                    groups[level].append(row)
 
    # ---- Wczytywanie XLSX (z nagłówkami) ----
    elif ext == ".xlsx":
        df = pd.read_excel(file_path)  # Pandas sam odczytuje nagłówki
        if df.shape[1] < 2:
            print(f"❗ Plik {filename} nie ma kolumny B – pomijam.")
            continue
       
        groups = defaultdict(list)
       
        for _, row in df.iterrows():
            level = str(row.iloc[1])        # kolumna B
            groups[level].append(row.tolist())
 
    else:
        continue  # pomiń inne pliki
 
    # Tworzenie katalogu wyjściowego dla danego pliku
    target_folder = os.path.join(output_dir, base_name)
    os.makedirs(target_folder, exist_ok=True)
 
    # Zapis plików wynikowych
    for level, rows in groups.items():
        output_file = os.path.join(target_folder, f"{level}.csv")
        with open(output_file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerows(rows)
 
        print(f"Utworzono: {output_file}")
 
print("✔ Zakończono przetwarzanie wszystkich plików.")