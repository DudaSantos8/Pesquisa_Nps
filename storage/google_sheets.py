import gspread
from google.oauth2.service_account import Credentials
from logs.logger_config import logger

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_NAME = "Relatorio_NPS"

EXPECTED_HEADERS = ["name", "email", "job", "rejected_at", "send_at"]

class SheetsClient:
    def __init__(self, creds_path: str, spreadsheet_key: str):
        logger.info("Autenticando Google Sheets")
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(spreadsheet_key).sheet1
        self._validate_headers()

    def _validate_headers(self):
        actual_headers = self.sheet.row_values(1)
        if len(actual_headers) != len(set(actual_headers)):
            logger.warning(f"⚠️ Cabeçalho duplicado detectado: {actual_headers}")
        if actual_headers != EXPECTED_HEADERS:
            logger.warning(f"⚠️ Cabeçalho inesperado na planilha. Esperado: {EXPECTED_HEADERS}, Encontrado: {actual_headers}")

    def get_existing_keys(self) -> set:
        logger.info("Lendo registros existentes na planilha")
        try:
            vals = self.sheet.get_all_records(expected_headers=EXPECTED_HEADERS)
        except Exception as e:
            logger.error(f"Erro ao ler registros: {e}")
            return set()
        return { (r["email"], r["send_at"]) for r in vals }

    def append_candidates(self, candidates: list) -> list:
        existing = self.get_existing_keys()
        new_rows = []
        for c in candidates:
            key = (c["email"], c["send_at"])
            if key not in existing:
                new_rows.append([
                    c["name"], c["email"], c["job"],
                    c["rejected_at"], c["send_at"]
                ])
        if new_rows:
            logger.info(f"Adicionando {len(new_rows)} novas linhas na planilha")
            self.sheet.append_rows(new_rows, value_input_option="USER_ENTERED")
        else:
            logger.info("Nenhum registro novo para adicionar")
        return new_rows
