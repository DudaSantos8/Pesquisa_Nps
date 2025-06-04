from typing import List
from email_function.enviar_ses import send_email
from utils.marcar_pesquisa_enviada import marcar_email_enviado
from logs.logger_config import logger

def enviar_email_candidatos_recusados_ses(
    candidates: List[dict],
    sender: str = "tp.automations@zup.com.br",
    subject: str = "[Zup] Queremos saber sua opinião!",
    limit: int = None,
    header_descricao: str = "Queremos saber como foi sua experiência com nosso processo seletivo.",
    url_formulario: str = "https://zup1.typeform.com/to/jay2SoZ7?typeform-source=www.google.com"
) -> List[dict]:

    template_path = r"C:\Users\Zupper\Desktop\TTP\pesquisas_de_satisfacao\template_recusados.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    results = []
    to_process = candidates if limit is None else candidates[:limit]

    for cand in to_process:
        name = cand.get("name", "Candidato")
        recipient = "tp.automations@zup.com.br"  # cand.get("email")
        job = cand.get("job")
        rejected_at = cand.get("rejected_at")

        if not recipient:
            results.append({
                "name": name,
                "email": None,
                "status": "E",
                "message_id": "E-mail não informado"
            })
            continue

        body_html = (
            template
            .replace("{{NOME_CANDIDATO}}", name)
            .replace("{{HEADER_DESCRICAO}}", header_descricao)
            .replace("{{URL_FORMULARIO}}", url_formulario)
        )

        body_text = (
            f"Oi, {name}! Tudo bem?\n\n"
            "Agradecemos sua participação no nosso processo seletivo!\n\n"
            "Para continuarmos melhorando, gostaríamos de saber como foi a sua experiência com nosso time.\n\n"
            "Responda nossa pesquisa de satisfação e nos ajude a evoluir! 😊\n\n"
            f"Enviar feedback agora: {url_formulario}\n\n"
            "Deixamos nosso agradecimento antecipado pela sua contribuição\n\n"
            "Abraços,\n"
            "Time de Talent Acquisition da Zup Innovation\n\n"
            "------------------------------\n"
            "Este é um e-mail automático. Por favor, não responda."
        )

        response = send_email(
            sender=sender,
            recipient=recipient,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            aws_region="sa-east-1",
            charset="UTF-8"
        )

        if response["status"] == "S":
            try:
                marcar_email_enviado(recipient, rejected_at, job)
                logger.info(f"CSV atualizado: email_enviado=True para {recipient}/{rejected_at}")
            except Exception as e:
                logger.error(f"Falha ao atualizar CSV para {recipient}/{rejected_at}: {e}")

        results.append({
            "name": name,
            "email": recipient,
            "status": response["status"],
            "message_id": response["response"]
        })

    return results
