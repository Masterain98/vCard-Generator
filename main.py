import datetime
from PIL import Image, ImageFilter
import pandas as pd
import numpy as np
import qrcode
import os


def add_genmall_prefix(num: int) -> str:
    return f"GM{str(num)}".replace(".0", "")


def add_eb_prefix(num: int) -> str:
    return f"EB{str(num)}".replace(".0", "")


def add_luma_prefix(num: int) -> str:
    return f"Luma{str(num)}".replace(".0", "")


def add_ad_prefix(num: int) -> str:
    return f"AD{str(num)}".replace(".0", "")


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


def remove_special_characters(text: str) -> str:
    text = str(text)
    return ''.join(e for e in text if e.isalnum() or e.isspace())


def phone_number_process(phone_number) -> str:
    phone_number = str(phone_number)
    return ''.join(e for e in phone_number if e.isalnum() or e.isspace() or e == "+" or e == "(" or e == ")")


def ticket_type_unify(t_type: str, short_mode: bool = False) -> str:
    t_type = str(t_type).lower()
    return_result = None

    if "early bird" in t_type:
        t_type = t_type.replace(" ", "").replace("-", "")

    if "vip" in t_type:
        return_result = "VIP"
    elif "booth type" in t_type:
        return_result = "General Admission 3-Day"
        if short_mode:
            return_result = "GA3"
    elif "all access" in t_type or "aa" in t_type:
        return_result = "All Access"
        if short_mode:
            return_result = "AA"
    elif "general admission" in t_type or "ga" in t_type or "general access" in t_type:
        if "1" in t_type:
            return_result = "General Admission 1-Day"
            if short_mode:
                return_result = "GA1"
        elif "2" in t_type:
            return_result = "General Admission 2-Day"
            if short_mode:
                return_result = "GA2"
        elif "3" in t_type or "sponsor" in t_type or "exhibitor" in t_type or "invited" in t_type:
            return_result = "General Admission 3-Day"
            if short_mode:
                return_result = "GA3"
        else:
            print(f"Unknown Ticket Type: {t_type}")
    elif "earlybird" in t_type:
        if "1day" in t_type:
            return_result = "General Admission 1-Day"
            if short_mode:
                return_result = "GA1"
        elif "2day" in t_type:
            return_result = "General Admission 2-Day"
            if short_mode:
                return_result = "GA2"
        elif "3day" in t_type:
            return_result = "General Admission 3-Day"
            if short_mode:
                return_result = "GA3"
        elif "booth" in t_type:
            return_result = "General Admission 3-Day"
            if short_mode:
                return_result = "GA3"
    elif "media" in t_type:
        return_result = "Media Partner"
        if short_mode:
            return_result = "Media"
    elif "speaker" in t_type:
        return_result = "Speaker"
        if short_mode:
            return_result = "Speaker"
    elif "staff" in t_type:
        return_result = "Staff"
        if short_mode:
            return_result = "Staff"
    elif "vc" in t_type:
        return_result = "VC"
        if short_mode:
            return_result = "VC"
    elif "accessories" in t_type:
        return_result = ""
    elif "edu" in t_type:
        return_result = "General Admission 3-Day"
        if short_mode:
            return_result = "GA3"
    else:
        print(f"Unknown Ticket Type: {t_type}")
    print(f"{t_type} -> {return_result}")
    return return_result


def make_qr_code_by_vcard_data(vcard_data: dict, save_path: str):
    last_name = vcard_data.get("last_name", "")
    first_name = vcard_data.get("first_name", "")
    job_title = vcard_data.get("title", "")
    phone = vcard_data.get("phone", "")
    email = vcard_data.get("email", "")
    organization = vcard_data.get("organization", "")
    website_url = vcard_data.get("url", "")
    github = vcard_data.get("github", "")
    linkedin = vcard_data.get("linkedin", "")
    twitter = vcard_data.get("twitter", "")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )

    qr_data = f'''BEGIN:VCARD
VERSION:3.0
N:{last_name};{first_name}
TITLE:{job_title}
TEL:{phone}
EMAIL:{email}
ORG:{organization}
URL:{linkedin if linkedin else website_url if website_url else github if github else twitter if twitter else ""}
URL;type=LinkedIn:{linkedin}
URL;type=Github:{github}
URL;type=Twitter:{twitter}
NOTE: {"Github: " + str(github) if github else ""}   {"LinkedIn: " + str(linkedin) if linkedin else ""}   {"Twitter: " + str(twitter) if twitter else ""}  {"Website: " + str(website_url) if website_url else ""}
END:VCARD'''
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    if img.size != (650, 650):
        img = img.resize((650, 650), Image.Resampling.LANCZOS)
    img.save(save_path)
    return save_path


if __name__ == "__main__":
    os.makedirs("cache", exist_ok=True)
    luma_file_exists = os.path.exists("luma_full.csv")
    eb_file_exists = os.path.exists("eb_full.csv")
    additional_file_exists = os.path.exists("Additional Ticket List.xlsx")
    if not luma_file_exists or not eb_file_exists:
        print("Please put the luma_full.csv and eb_full.csv in the same directory of this program")
        input("Press Enter to exit")
        exit(1)
    if not additional_file_exists:
        print("Additional Ticket Excel is not found, not going to export additional tickets")

    os.makedirs("qrcodes", exist_ok=True)

    # luma
    df = pd.read_csv("luma_full.csv")
    df = df.reset_index()
    df["index"] = df["index"].apply(add_luma_prefix)
    df["First Name"] = df["name"].apply(lambda x: name_process(x)[0])
    df["Last Name"] = df["name"].apply(lambda x: name_process(x)[1])
    df.rename(columns={"What company/organization do you work for?": "Company"}, inplace=True)
    df.rename(columns={"What is your job title or function?": "Job Title"}, inplace=True)
    df.rename(columns={"ticket_name": "Ticket Type"}, inplace=True)
    df.rename(columns={"phone_number": "Phone"}, inplace=True)
    df.rename(columns={"email": "Email"}, inplace=True)
    df["Ticket Type"] = df["Ticket Type"].apply(lambda x: ticket_type_unify(x))
    df['Github Profile'] = None
    df['LinkedIn Profile'] = None
    df['Twitter Handle'] = None
    df['Website'] = None
    luma_df = df[['index', 'First Name', 'Last Name', 'Email', 'Phone', 'Job Title', 'Company', 'Ticket Type',
                  "Github Profile", "LinkedIn Profile", "Twitter Handle", "Website"]]
    luma_df.to_csv("./cache/luma_slim.csv", index=False)

    # eventbrite
    df = pd.read_csv("eb_full.csv")
    df = df.reset_index()
    df["index"] = df["index"].apply(add_eb_prefix)
    df.rename(columns={"Cell Phone": "Phone"}, inplace=True)
    df["Ticket Type"] = df["Ticket Type"].apply(lambda x: ticket_type_unify(x))
    eb_df = df[['index', 'First Name', 'Last Name', 'Email', 'Phone', 'Job Title', 'Company', 'Ticket Type',
                "Github Profile", "LinkedIn Profile", "Twitter Handle", "Website"]]
    eb_df.to_csv("./cache/eventbrite_slim.csv", index=False)

    # Data Cleaning
    eb_df.reset_index(inplace=True, drop=True)
    luma_df.reset_index(inplace=True, drop=True)
    aio_df = pd.concat([eb_df, luma_df], ignore_index=True)
    aio_df['First Name'] = df['First Name'].apply(lambda x: remove_special_characters(x))
    aio_df['Last Name'] = df['Last Name'].apply(lambda x: remove_special_characters(x))
    aio_df['Phone'] = df['Phone'].apply(lambda x: phone_number_process(x))
    aio_df['Ticket Type'] = df['Ticket Type'].apply(lambda x: ticket_type_unify(x))
    aio_df.to_csv("./cache/aio_slim.csv", index=False)
    exit(0)

    # Genmall
    """
    df = pd.read_csv("genmall_full.csv")
    df = df.reset_index()
    df["index"] = df["index"].apply(add_genmall_prefix)
    df["First Name"] = df["Billing Name"].apply(lambda x: name_process(x)[0])
    df["Last Name"] = df["Billing Name"].apply(lambda x: name_process(x)[1])
    df["Ticket Type"] = df["Lineitem name"].apply(lambda x: ticket_type_unify(x))
    genmall_df = df[['index', 'First Name', 'Last Name', 'Email', 'Ticket Type']].copy()
    genmall_df.to_excel("./cache/genmall_processed.xlsx", index=False)
    aio_df = pd.concat([aio_df, genmall_df]).copy()
    """

    # Additional ticket
    if additional_file_exists:
        additional_df = pd.read_excel("Additional Ticket List.xlsx", sheet_name="Sheet1")
        additional_df["index"] = additional_df["index"].apply(add_ad_prefix)
        if "All Ticket Type Allowed here" in df.columns:
            additional_df = additional_df.drop("All Ticket Type Allowed here", axis=1)
        aio_df = pd.concat([aio_df, additional_df]).copy()

    # Remove
    columns_checks = ["Job Title", "Phone", "Email"]
    for c in columns_checks:
        df[c] = df[c].replace('nan', np.nan)

    duplicates = aio_df["index"].duplicated()
    if duplicates.any():
        print("Found duplicated data")
        print(aio_df[duplicates])
    else:
        print("No duplicated data")

    ticket_type_counts = aio_df['Ticket Type'].value_counts()
    print(ticket_type_counts)
    print(f"Total {len(aio_df)} tickets processed")

    # Generate QR Codes
    for index, row in aio_df.iterrows():
        this_vcard_data = {
            "first_name": row["First Name"],
            "last_name": row["Last Name"],
            "title": row["Job Title"],
            "phone": row["Phone"],
            "email": row["Email"],
            "organization": row["Company"],
            "url": row["Website"],
            "github": row["Github Profile"],
            "linkedin": row["LinkedIn Profile"],
            "twitter": row["Twitter Handle"]
        }
        qr_code_path = f"qrcodes/{row['index']}.png"
        make_qr_code_by_vcard_data(this_vcard_data, qr_code_path)

    aio_df.to_excel(f"aio-{datetime.datetime.now().strftime("%m%d%Y-%H%M%S")}.xlsx", index=False)
    input("task completed, press enter to exit")
