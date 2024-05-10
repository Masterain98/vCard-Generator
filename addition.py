import pandas as pd
from main import name_process


def speaker_metadata_to_ticket_list():
    df_raw = pd.read_excel("./additonal/Copy of Speaker Metadata.xlsx", sheet_name="Sheet1")
    df = pd.DataFrame()
    for i, r in df_raw.iterrows():
        fn, ln = name_process(r["Name"])
        current_title = r["Title"]
        title_split = current_title.split("@")
        job_title = title_split[0].capitalize()
        company = title_split[1].capitalize()
        company = company.replace("Ai", "AI")
        df.at[i, "First Name"] = fn
        df.at[i, "Last Name"] = ln
        df.at[i, "Job Title"] = job_title
        df.at[i, "Company"] = company
    df.to_excel("./additonal/speaker_metadata_to_ticket_list.xlsx", index=False)
