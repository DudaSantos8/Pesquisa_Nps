import os
from dotenv import load_dotenv
from logs.logger_config import logger
from greenhouse.greenhouse import configure, get_recent_candidates, extract_rejected_candidates
from storage.gmail_enviar_relatorio import authenticate_gmail, send_summary_email
#from test.chamar_envio_gmail import enviar_email_candidatos_recusados # test
from email.chamar_envio_ses import enviar_email_candidatos_recusados_ses
from storage.registro_csv import save_rejected_to_csv
from utils.busca_envios_hoje import buscar_envios_hoje
from storage.google_sheets import SheetsClient

def main():
    load_dotenv()
    configure(os.getenv("API_KEY"))
    logger.info("Iniciando fluxo de NPS")

    all_c = get_recent_candidates()
    rejeitados = extract_rejected_candidates(all_c)

    sheets = SheetsClient(
        creds_path = "credenciais/test-pesquisa-nps-6d96b377fded.json",
        spreadsheet_key=os.getenv("GSHEET_KEY")
    )
    novos = sheets.append_candidates(rejeitados)

    save_rejected_to_csv(rejeitados)

    envios_hoje = buscar_envios_hoje()
    if envios_hoje:
        enviar_email_candidatos_recusados_ses(envios_hoje, limit=1)
    else:
        logger.info("Nenhum envio programado para hoje.")
    
    if novos:
        report = "\n".join(
            f"- {r[0]} ({r[1]}) → enviar em {r[4]}"
            for r in novos
        )
        service = authenticate_gmail('credenciais/credentials.json')
        your_email = os.getenv("EMAIL_TESTE")
        send_summary_email(service, your_email, your_email, report)
    else:
        logger.info("Sem novos candidatos para notificar.")

if __name__ == "__main__":
    main()
