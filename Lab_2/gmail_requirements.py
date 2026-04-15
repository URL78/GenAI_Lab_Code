import os
import base64
import requests

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# ================= CONFIG =================
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"
# =========================================


def authenticate_gmail():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def fetch_latest_email():
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    results = service.users().messages().list(
        userId="me",
        maxResults=1,
        labelIds=["INBOX"]
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return None

    msg = service.users().messages().get(
        userId="me",
        id=messages[0]["id"],
        format="full"
    ).execute()

    payload = msg.get("payload", {})
    parts = payload.get("parts", [])

    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part["body"].get("data")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8").strip()

    return None


def call_llm(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=300)
    response.raise_for_status()
    return response.json()["response"]


# ========== STAGE 1: REQUIREMENTS ==========
def extract_requirements(email_text):
    prompt = f"""
You are a software requirements engineer.

From the email below, extract:
1. Functional Requirements
2. Non-Functional Requirements
3. Assumptions

Email:
\"\"\"
{email_text}
\"\"\"

Use clear bullet points.
"""
    return call_llm(prompt)


# ========== STAGE 2: ELICITATION ==========
def generate_elicitation(requirements):
    prompt = f"""
You are a requirements engineering expert.

Given the following extracted requirements:

\"\"\"
{requirements}
\"\"\"

1. Select suitable requirement elicitation techniques
   (e.g., interviews, questionnaires, workshops, observation, prototyping).


Output clearly with headings.
"""
    return call_llm(prompt)


# ========== STAGE 3: JUSTIFICATION ==========
def justify_elicitation(requirements, elicitation):
    prompt = f"""
You are a senior requirements analyst.

Based on:
Requirements:
\"\"\"
{requirements}
\"\"\"

Chosen Elicitation Techniques:
\"\"\"
{elicitation}
\"\"\"

Provide a justification explaining:
- Why these techniques are appropriate
- How they reduce ambiguity and risk
- Why alternatives may be less effective

Limit your answer to 8–10 bullet points.
"""
    return call_llm(prompt)


# ================= MAIN PIPELINE =================
if __name__ == "__main__":

    print("\n" + "=" * 90)
    print("📬 STEP 1: FETCHING LATEST EMAIL FROM GMAIL")
    print("=" * 90)

    email = fetch_latest_email()
    if not email:
        print("❌ No email found.")
        exit(1)

    print("\n📧 EMAIL CONTENT:\n")
    print(email)

    print("\n" + "=" * 90)
    print("📋 STEP 2: EXTRACTING REQUIREMENTS")
    print("=" * 90)

    requirements = extract_requirements(email)
    print("\n✅ EXTRACTED REQUIREMENTS:\n")
    print(requirements)

    print("\n" + "=" * 90)
    print("🧠 STEP 3: GENERATING ELICITATION TECHNIQUES")
    print("=" * 90)

    elicitation = generate_elicitation(requirements)
    print("\n🛠️ ELICITATION TECHNIQUES:\n")
    print(elicitation)

    print("\n" + "=" * 90)
    print("📖 STEP 4: JUSTIFYING ELICITATION TECHNIQUES")
    print("=" * 90)

    justification = justify_elicitation(requirements, elicitation)
    print("\n🧾 JUSTIFICATION:\n")
    print(justification)

    print("\n" + "=" * 90)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 90)
