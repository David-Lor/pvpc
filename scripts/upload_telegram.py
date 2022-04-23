import datetime
import requests
import pydantic
from export_pvpc import PVPCOutput, String


class Settings(pydantic.BaseSettings):
    telegram_bot_token: String
    telegram_chatid: String
    data_path: pydantic.FilePath


class Const:
    weekdays = [
        "lunes",
        "martes",
        "miércoles",
        "jueves",
        "viernes",
        "sábado",
        "domingo"
    ]
    months = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre"
    ]
    prices_emojis = [
        # from cheaper to more expensive; logic in _price_to_emoji()
        "🔵",
        "🟡",
        "🟤"
    ]


def _read_file(path: str) -> PVPCOutput:
    return PVPCOutput.parse_file(path)


def _price_to_emoji(price: float) -> str:
    if price < 0.1:
        return Const.prices_emojis[0]  # < 0,10 €/kWh
    if price < 0.15:
        return Const.prices_emojis[1]  # 0,10 ~ 0,15 €/kWh
    return Const.prices_emojis[2]  # > 0,15 €/kWh


def _format_date_human(date: datetime.date) -> str:
    return f"{Const.weekdays[date.weekday()]}, {date.day} de {Const.months[date.month-1]} del {date.year}"


def _format_telegram_message(data: PVPCOutput) -> str:
    prices_text_lines = []
    for hour, price in data.data.items():
        price: float
        hour = str(hour).zfill(2)

        emoji = _price_to_emoji(price)
        price_str = str(price).ljust(7)  # adjust to 7 characters (0.12345)
        line = f"{emoji}<code>{hour}h: {price_str} €/kWh</code>"
        prices_text_lines.append(line)

    date_human = _format_date_human(data.day)
    prices_text = "\n".join(prices_text_lines)
    return f"<b>{date_human}</b>\n\n{prices_text}"


def _send_to_telegram(data: PVPCOutput, telegram_bot_token: str, telegram_chatid: str):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    text = _format_telegram_message(data)
    body = dict(
        chat_id=telegram_chatid,
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    r = requests.post(
        url=url,
        json=body,
    )
    r.raise_for_status()


def main():
    settings = Settings()
    data = _read_file(settings.data_path.as_posix())
    _send_to_telegram(
        data=data,
        telegram_bot_token=settings.telegram_bot_token,
        telegram_chatid=settings.telegram_chatid,
    )


if __name__ == '__main__':
    main()
