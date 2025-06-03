import csv

CSV_PATH = r"C:\Users\Zupper\Desktop\TTP\pesquisas_de_satisfacao\registro_candidatos\rejeitados.csv"

def marcar_email_enviado(email: str, rejected_at: str, job: str):

    linhas = []

    with open(CSV_PATH, mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["email"] == email and row["rejected_at"] == rejected_at and row["job"] == job:
                row["email_enviado"] = "True"
            linhas.append(row)

    with open(CSV_PATH, mode="w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(linhas)
