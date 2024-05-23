import pandas as pd
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


count_check()
