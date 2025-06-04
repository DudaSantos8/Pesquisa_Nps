import requests
from dateutil.parser import parse
from datetime import datetime, timedelta
from utils.verificacao_datas import add_business_days, is_business_day
from logs.logger_config import logger

GH_BASE = "https://harvest.greenhouse.io/v1"
GH_HEADERS = {}

def configure(api_key: str):
    global GH_HEADERS
    GH_HEADERS = {"Authorization": f"Basic {api_key}"}
    logger.info("✅ Greenhouse client configurado com sucesso.")

def get_recent_candidates(days: int = 10):
    since = (datetime.utcnow().date() - timedelta(days=days)).isoformat() + "T00:00:00Z"
    params = {"created_after": since, "per_page": 100, "page": 1}
    all_candidates, page_number = [], 1

    logger.info(f"📥 Buscando candidatos criados após {since}")
    while True:
        resp = requests.get(f"{GH_BASE}/candidates", headers=GH_HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        logger.info(f"📄 Página {page_number}: {len(data)} candidatos encontrados")
        if not data:
            break
        all_candidates.extend(data)
        if 'rel="next"' not in resp.headers.get("Link", ""):
            break
        params["page"] += 1
        page_number += 1

    return all_candidates

def extract_rejected_candidates(candidates: list, days: int = 3) -> list:
    result = []
    limite_rejeicao = datetime.utcnow().date() - timedelta(days=days)

    for c in candidates:
        emails = c.get("email_addresses", [])
        if not emails:
            logger.warning(f"⚠️ Candidato {c.get('id')} sem email. Pulando.")
            continue

        email = emails[0].get("value")
        name = f"{c.get('first_name','').strip()} {c.get('last_name','').strip()}".strip()

        for app in c.get("applications", []):
            if app.get("status") != "rejected" or not app.get("rejected_at"):
                continue

            rej_dt = parse(app["rejected_at"]).date()
            if rej_dt < limite_rejeicao:
                continue

            send_dt = add_business_days(rej_dt, 3)
            if not is_business_day(send_dt):
                send_dt = add_business_days(send_dt, 1)

            jobs = app.get("jobs") or []
            job_name = jobs[0].get("name") if jobs else "Sem Vaga Associada"

            result.append({
                "name": name,
                "email": email,
                "job": job_name,
                "rejected_at": rej_dt.isoformat(),
                "send_at": send_dt.isoformat()
            })

    result.sort(key=lambda x: x["rejected_at"], reverse=True)

    logger.info(f"✅ {len(result)} candidatos rejeitados nos últimos {days} dias encontrados.")
    return result
