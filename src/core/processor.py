from src.api.client import AlegraClient
from src.core.excel_handler import ExcelHandler
from src.utils.logger import setup_logger

logger = setup_logger()


class AlegraProcessor:
    def __init__(self, file_path):
        self.excel_handler = ExcelHandler(file_path)
        self.api_client = AlegraClient()

    def process_invoices(self):
        grouped_data = self.excel_handler.get_grouped_data()
        for data in grouped_data:
            try:
                client_doc = data["client"]["identification"]
                client_name = data["client"]["name"]
                contact = self.api_client.get_contact_by_id(client_doc)
                if not contact:
                    contact_payload = {
                        "name": client_name,
                        "identification": client_doc,
                        "type": ["client"],
                    }
                    contact = self.api_client.create_contact(contact_payload)
                client_id = contact["id"]
                invoice_payload = {
                    "date": data["date"],
                    "dueDate": data["date"],
                    "client": client_id,
                    "items": data["items"],
                }
                response = self.api_client.create_invoice(invoice_payload)
                logger.info(
                    f"ID Externo {data['external_id']} procesado. ID Alegra {response.get('id')}"
                )
            except Exception as e:
                logger.error(f"Fallo en ID Externo {data.get('external_id')}: {str(e)}")
