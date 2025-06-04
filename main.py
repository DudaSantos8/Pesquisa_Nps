import os
from dotenv import load_dotenv
from logs.logger_config import logger
from email_function.chamar_envio_ses import enviar_email_candidatos_recusados_ses
from greenhouse.greenhouse import configure, get_recent_candidates, extract_rejected_candidates
from storage.registro_csv import save_rejected_to_csv
from utils.busca_envios_hoje import buscar_envios_hoje

def main():
    load_dotenv()
    configure(os.getenv("API_KEY"))
    logger.info("Iniciando fluxo de NPS")

    candidatos = get_recent_candidates(days=10)
    rejeitados = extract_rejected_candidates(candidatos, days=3)

    save_rejected_to_csv(rejeitados)

    envios_hoje = buscar_envios_hoje()
    if envios_hoje:
        enviar_email_candidatos_recusados_ses(envios_hoje, limit=1)
    else:
        logger.info("Nenhum envio programado para hoje.")

if __name__ == "__main__":
    main()
