from datetime import datetime, timedelta, time
import holidays
import pytz

from logs.logger_config import logger

BR_HOLIDAYS = holidays.Brazil()

def is_business_day(dt: datetime) -> bool:
    return dt.weekday() < 5 and dt not in BR_HOLIDAYS

def add_business_days(start: datetime, days: int) -> datetime:
    current = start
    added = 0
    while added < days:
        current += timedelta(days=1)
        if is_business_day(current):
            added += 1
    return current

def next_business_morning(dt: datetime, hour: int = 9) -> datetime:
    """Se estiver fora do horário comercial (9–18h BRT), retorna próximo dia útil às `hour`."""
    local = dt.astimezone(pytz.timezone("America/Sao_Paulo"))
    if local.weekday() >= 5 or local.date() in BR_HOLIDAYS or not (time(9) <= local.time() < time(18)):
        nxt = add_business_days(local, 1).replace(hour=hour, minute=0, second=0, microsecond=0)
        logger.info(f"Fora do horário comercial. Agendado para {nxt.isoformat()}")
        return nxt.astimezone(pytz.utc)
    return dt
