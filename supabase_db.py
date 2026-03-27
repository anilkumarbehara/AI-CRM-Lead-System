import os
import requests
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing in .env")

HEADERS = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}


def insert_lead(data: dict):
    url = f"{SUPABASE_URL}/rest/v1/leads"
    response = requests.post(url, headers=HEADERS, json=data, timeout=30)
    print("Insert lead status:", response.status_code)
    print("Insert lead response:", response.text)

    if not response.ok:
        raise ValueError(f"Supabase lead insert failed: {response.text}")

    return response.json() 


def get_all_leads():
    url = f"{SUPABASE_URL}/rest/v1/leads?select=*&order=id.desc"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def get_lead_by_id(lead_id: int):
    url = f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}&select=*"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data[0] if data else None


def update_lead(lead_id: int, data: dict):
    url = f"{SUPABASE_URL}/rest/v1/leads?id=eq.{lead_id}"
    response = requests.patch(url, headers=HEADERS, json=data, timeout=30)
    print("Update lead:", response.status_code, response.text)
    response.raise_for_status()
    return response.json() if response.text else []


def insert_message(data: dict):
    url = f"{SUPABASE_URL}/rest/v1/messages"
    response = requests.post(url, headers=HEADERS, json=data, timeout=30)
    print("Insert message:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()


def get_messages_by_lead(lead_id: int):
    url = f"{SUPABASE_URL}/rest/v1/messages?lead_id=eq.{lead_id}&select=*&order=id.asc"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()


def insert_task(data: dict):
    url = f"{SUPABASE_URL}/rest/v1/tasks"
    response = requests.post(url, headers=HEADERS, json=data, timeout=30)
    print("Insert task:", response.status_code, response.text)
    response.raise_for_status()
    return response.json()


def get_tasks_by_lead(lead_id: int):
    url = f"{SUPABASE_URL}/rest/v1/tasks?lead_id=eq.{lead_id}&select=*&order=id.desc"
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response.json()