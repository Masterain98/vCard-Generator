import os

import pandas as pd
from main import ticket_type_unify, make_qr_code_by_vcard_data


def add_genmall_prefix(num: int) -> str:
    return f"GM{str(num)}".replace(".0", "")


def name_process(name: str) -> tuple[str, str]:
    if not name or name.strip() == "":
        return "", ""
    name = name.split(" ")
    match len(name):
        case 0:
            fn = ""
            mn = ""
            ln = ""
        case 1:
            fn = name[0]
            mn = ""
            ln = ""
        case 2:
            fn = name[0]
            mn = ""
            ln = name[1]
        case 3:
            fn = name[0]
            mn = name[1]
            ln = name[2]
        case _:
            fn = name[0]
            mn = name[1]
            ln = ""
            for i in range(2, len(name)):
                ln += name[i] + " "
            ln = ln[:-1]
    fn = fn.capitalize()
    mn = mn.capitalize()
    ln = ln.capitalize()
    if not mn:
        return fn, ln
    else:
        return fn, f"{mn} {ln}"


if __name__ == "__main__":
    os.makedirs("genmall_qrcodes", exist_ok=True)
    df = pd.read_csv("genmall_full.csv")
    df = df.reset_index()
    df["index"] = df["index"].apply(add_genmall_prefix)
    df["First Name"] = df["Billing Name"].apply(lambda x: name_process(x)[0])
    df["Last Name"] = df["Billing Name"].apply(lambda x: name_process(x)[1])
    df["Ticket Type"] = df["Lineitem name"].apply(lambda x: ticket_type_unify(x))
    final_df = df[['index', 'First Name', 'Last Name', 'Email', 'Ticket Type']]
    final_df.to_excel("genmall_processed.xlsx", index=False)

    # Generate QR Codes
    for index, row in final_df.iterrows():
        this_vcard_data = {
            "first_name": row["First Name"],
            "last_name": row["Last Name"],
            "email": row["Email"],
        }
        qr_code_path = f"genmall_qrcodes/{row['index']}.png"
        make_qr_code_by_vcard_data(this_vcard_data, qr_code_path)

