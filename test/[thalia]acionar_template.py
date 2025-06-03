#from [thalia]amazon_ses import send_email

def enviar_email_candidatos_recusados():
    sender = "tp.automations@zup.com.br"
    template_path = 'amazon_web_services/template_recusados.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    recipient = 'thalia.lopes@zup.com.br'
    nome_candidato = 'Thalia'
    data_processo = '11/04/2025'
    # Substitui os placeholders pelos valores reais
    body_html = (
        template
        .replace('{{NOME_CANDIDATO}}', nome_candidato)
        .replace('{{DATA_PROCESSO}}', data_processo)
    )
    body_text = (
        f"Olá {nome_candidato},\n\n"
        f"Sabemos que o resultado do processo seletivo realizado em {data_processo} não foi o esperado desta vez, "
        "mas agradecemos sinceramente pelo seu interesse em fazer parte do nosso time.\n\n"
        "Sua opinião é muito importante para que possamos melhorar nossos processos. Por favor, responda a pesquisa no link enviado."
    )

    #message_id = send_email(sender, recipient, 'Sua opinião é importante para nós!', body_text, body_html)
    #return message_id


if __name__ == "__main__":
    enviar_email_candidatos_recusados()