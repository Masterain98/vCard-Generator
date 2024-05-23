import os
import pandas as pd


def check_and_remove_duplicates(old_df, new_df):
    common_columns = [col for col in old_df.columns if col != 'index']

    merged = new_df.merge(old_df[common_columns], on=common_columns, how='left', indicator=True)
    duplicates = merged[merged['_merge'] == 'both']

    duplicate_indices = duplicates['index'].tolist()

    new_df_cleaned = new_df[~new_df['index'].isin(duplicate_indices)]

    return new_df_cleaned, duplicate_indices


old_df_path = "./history/511/511.xlsx"
new_df_path = "./history/523/523.xlsx"
old_df_obj = pd.read_excel(old_df_path, sheet_name="Sheet1")
new_df_obj = pd.read_excel(new_df_path, sheet_name="Sheet1")
cleaned_df, duplicated_list = check_and_remove_duplicates(old_df_obj, new_df_obj)

print(f"Removed {len(duplicated_list)} duplicates")
print(duplicated_list)
cleaned_df.to_excel("./history/523/523_cleaned.xlsx", index=False)
for i in duplicated_list:
    try:
        os.remove(f"./history/523/qrcodes/{i}.png")
        print(f"Removed {i}.png")
    except FileNotFoundError:
        print(f"{i}.png not found")
