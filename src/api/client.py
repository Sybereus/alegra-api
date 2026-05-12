import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()


class AlegraClient:
    def __init__(self):
        self.email = os.getenv("ALEGRA_EMAIL")
        self.token = os.getenv("ALEGRA_TOKEN")
        self.base_url = os.getenv("ALEGRA_API_URL")
        self.auth = HTTPBasicAuth(self.email, self.token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_contact_by_id(self, identification):
        params = {"identification": identification}
        response = requests.get(
            f"{self.base_url}contacts", auth=self.auth, params=params
        )
        if response.status_code == 200:
            contacts = response.json()
            return contacts[0] if contacts else None
        return None

    def create_contact(self, contact_data):
        response = requests.post(
            f"{self.base_url}contacts", auth=self.auth, json=contact_data
        )
        response.raise_for_status()
        return response.json()

    def create_invoice(self, invoice_data):
        response = requests.post(
            f"{self.base_url}invoices", auth=self.auth, json=invoice_data
        )
        response.raise_for_status()
        return response.json()
