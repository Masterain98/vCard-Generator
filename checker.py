import pandas as pd
from main import ticket_type_unify
import os


def count_check():
    df = pd.read_excel("aio-05072024165806.xlsx", sheet_name="Sheet1")
    duplicates = df["index"].duplicated()
    if duplicates.any():
        print("Found duplicated data")
        print(df[duplicates])
    else:
        print("No duplicated data")

    for i, r in df.iterrows():
        qr_code_file_name = f"qrcodes/{r['index']}.png"
        if not os.path.exists(qr_code_file_name):
            print(f"QR Code not found for {r['index']}")
            continue


def make_badge_type_code(excel_file_path: str):
    df = pd.read_excel(excel_file_path, sheet_name="Sheet1")
    df["Ticket Code"] = df["Ticket Type"].apply(lambda x: ticket_type_unify(x, True))
    df.to_excel(excel_file_path.replace(".xlsx", "-code.xlsx"), index=False)

make_badge_type_code("./history/523/523_cleaned.xlsx")