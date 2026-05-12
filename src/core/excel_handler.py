import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger()


class ExcelHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.required_columns = [
            "ID_COMPROBANTE",
            "TIPO",
            "CLIENTE_DOC",
            "CLIENTE_NOMBRE",
            "MONEDA",
            "ITEM_ID",
            "ITEM_PRECIO",
            "ITEM_CANTIDAD",
        ]

    def read_and_validate(self):
        try:
            df = pd.read_excel(self.file_path)
            missing = [col for col in self.required_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Faltan columnas: {', '.join(missing)}")
            return df
        except Exception as e:
            logger.error(f"Error leyendo Excel: {e}")
            raise

    def get_grouped_data(self):
        df = self.read_and_validate()
        grouped = []
        for group_id, data in df.groupby("ID_COMPROBANTE"):
            first_row = data.iloc[0]
            items = []
            for _, row in data.iterrows():
                items.append(
                    {
                        "id": int(row["ITEM_ID"]),
                        "price": float(row["ITEM_PRECIO"]),
                        "quantity": float(row["ITEM_CANTIDAD"]),
                    }
                )
            invoice_data = {
                "external_id": str(group_id),
                "type": first_row["TIPO"],
                "date": first_row.get("FECHA", None),
                "currency": first_row["MONEDA"],
                "client": {
                    "name": first_row["CLIENTE_NOMBRE"],
                    "identification": str(first_row["CLIENTE_DOC"]),
                },
                "items": items,
            }
            grouped.append(invoice_data)
        return grouped
