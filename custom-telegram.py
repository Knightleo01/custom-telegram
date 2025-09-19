#!/usr/bin/env python3
import sys
import json
import requests

# Lendo alerta
alert_file = sys.argv[1]
hook_url = sys.argv[3]  # Vem do ossec.conf

with open(alert_file) as f:
    alert_json = json.load(f)

alert_level = alert_json.get('rule', {}).get('level', "N/A")
description = alert_json.get('rule', {}).get('description', "N/A")
rule_id = alert_json.get('rule', {}).get('id', "N/A")
agent_name = alert_json.get('agent', {}).get('name', "N/A")
agent_ip = alert_json.get('agent', {}).get('ip', "N/A")
manager_name = alert_json.get('manager', {}).get('name', "N/A")
timestamp = alert_json.get('timestamp', "N/A")
full_log = alert_json.get('full_log', "N/A")

# Mensagem formatada
msg_text = (
    f"🚨 *Alerta do Wazuh*\n\n"
    f"*Descrição:* {description}\n"
    f"*Nível:* {alert_level}\n"
    f"*Regra ID:* {rule_id}\n"
    f"*Agente:* {agent_name}\n"
    f"*IP do Agente:* {agent_ip}\n"
    f"*Gerenciado por:* {manager_name}\n"
    f"*Horário:* {timestamp}\n"
    f"*Log Completo:*\n```\n{full_log}\n```"
)

# O chat_id do grupo
CHAT_ID = "COLOQUE_AQUI_ID_GRUPO"

payload = {
    "chat_id": CHAT_ID,
    "text": msg_text,
    "parse_mode": "Markdown"
}

headers = {'Content-Type': 'application/json'}
response = requests.post(hook_url, headers=headers, json=payload)

if response.status_code != 200:
    print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
    sys.exit(1)

sys.exit(0)
