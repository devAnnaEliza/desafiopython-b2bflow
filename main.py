import os
import logging

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")


def get_contacts(limit=3):
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = (
        supabase
        .table("contatos")
        .select("nome, telefone")
        .eq("ativo", True)
        .limit(limit)
        .execute()
    )

    return response.data


def send_message(phone, name):
    url = (
        f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}"
        f"/token/{ZAPI_INSTANCE_TOKEN}/send-text"
    )

    payload = {
        "phone": phone,
        "message": f"Olá, {name} tudo bem com você?"
    }

    response = requests.post(
        url,
        json=payload,
        timeout=15
    )

    if response.status_code == 200:
        logging.info(f"Mensagem enviada para {name}")
    else:
        logging.error(
            f"Erro ao enviar para {name}: {response.text}"
        )


def main():
    contacts = get_contacts()

    if not contacts:
        logging.warning("Nenhum contato encontrado.")
        return

    logging.info(
        f"{len(contacts)} contato(s) encontrado(s)."
    )

    for contact in contacts:
        send_message(
            contact["telefone"],
            contact["nome"]
        )


if __name__ == "__main__":
    main()