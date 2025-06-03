import os
from typing import List
from test.enviar_gmail import authenticate_gmail, send_email_gmail

def enviar_email_candidatos_recusados(
    candidates: List[dict],
    creds_path: str = 'credenciais/credentials.json',
    sender: str = '@gmail.com',
    subject: str = '[Zup] Queremos saber sua opinião!',
    limit: int = None,
    header_descricao: str = "Queremos saber como foi sua experiência com nosso processo seletivo.",
    url_formulario: str = "https://zup1.typeform.com/to/jay2SoZ7?typeform-source=www.google.com"
) -> List[dict]:

    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, 'template_oficial_recusados.html')

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Autentica com Gmail
    service = authenticate_gmail(creds_path)

    results = []
    to_process = candidates if limit is None else candidates[:limit]

    for cand in to_process:
        name = cand['name']
        recipient = cand['email']
        data_processo = cand.get('rejected_at', 'data não informada')

        # Substituição de placeholders no HTML
        body_html = (
            template
            .replace('{{NOME_CANDIDATO}}', name)
            .replace('{{HEADER_DESCRICAO}}', header_descricao)
            .replace('{{URL_FORMULARIO}}', url_formulario)
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
        # Envio do e-mail
        resp = send_email_gmail(service, sender, subject, body_text, body_html)
        results.append({
            'name': name,
            'email': recipient,
            'status': resp['status'],
            'message_id': resp['response']
        })

    return results
