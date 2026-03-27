import pandas as pd
import schedule
import time
from llm_agent import generate_followup_with_llm
from email_sender import send_email

CSV_FILE = "contacts.csv"

def followup():
    df = pd.read_csv(CSV_FILE)

    for i, row in df.iterrows():
        if row["Followup"] == "Yes":
            continue

        description = row["Description"]
        intent = row["Intent"]
        status = row["Status"]
        task = row["Task"]
        email = row["Email"]
        name = row["Name"]

        followup_result = generate_followup_with_llm(description, intent, status, task)

        subject = followup_result["email_subject"]
        body = followup_result["email_body"]

        send_email(email, subject, body, lead_id=id)
        df.at[i, "Followup"] = "Yes"

    df.to_csv(CSV_FILE, index=False)
    print("Follow-up cycle completed")


schedule.every(5).minutes.do(followup)

while True:
    schedule.run_pending()
    time.sleep(1)