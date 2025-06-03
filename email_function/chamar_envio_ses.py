from typing import List
from email_function.enviar_ses import send_email

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
        recipient = "tp.automations@zup.com.br"#cand.get("email")
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

        # Corpo em texto simples (fallback)
        body_text = (
            f"Oi {name}! Tudo bem?\n\n"
            "Agradecemos sua participação no nosso processo seletivo!\n\n"
            "Para continuarmos melhorando, gostaríamos de saber como foi a sua experiência com nosso time.\n\n"
            "Responda nossa pesquisa de satisfação e nos ajude a evoluir! 😊\n\n"
            f"Deixar feedback agora: {url_formulario}\n\n"
            "Já deixamos nosso agradecimento antecipado pelo seu feedback.\n\n"
            "Abraços,\n"
            "Time de Talent Acquisition da Zup Innovation\n\n"
            "------------------------------\n"
            "Este é um e-mail automático. Por favor, não responda."
        )

        # Envio do e-mail via SES
        resp = send_email(
            sender=sender,
            recipient=recipient,
            job = job,
            rejected_at = rejected_at,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            aws_region="sa-east-1",
            charset="UTF-8"
        )

        results.append({
            "name": name,
            "email": recipient,
            "status": resp.get("status"),
            "message_id": resp.get("response")
        })

    return results
