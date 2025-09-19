Perfeito! Vou atualizar o README referenciando suas pastas e arquivos existentes como você pediu (`custom-telegram` e `custom-telegram.py`) e mantendo o estilo GitHub/Teams.

---

# Wazuh Telegram Integration Setup

Este repositório contém a integração do **Wazuh** com **Telegram**, permitindo que alertas do Wazuh sejam enviados diretamente para um **chat ou grupo no Telegram**.

---

## **1️⃣ Criar o Bot no Telegram**

1. Abra o Telegram e converse com o [@BotFather](https://t.me/BotFather).
2. Crie um novo bot usando:

   ```
   /newbot
   ```
3. Escolha um nome e um username para o bot.
4. Copie o **token do bot** fornecido pelo BotFather.

   > Exemplo: `123456789:ABCdefGHIjklMNOpQRstuvWXyz`
5. Crie ou escolha um **grupo** e adicione o bot como membro.
6. Obtenha o **chat ID** do grupo:

   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```

   > IDs de supergrupo começam com `-100...`

---

## **2️⃣ Estrutura da Integração**

Coloque os arquivos do script em uma pasta chamada `custom-telegram` dentro do diretório de integrações do Wazuh:

```
/var/ossec/integrations/custom-telegram/
│
├── custom-telegram
├── custom-telegram.py   # Script que envia alertas para Telegram
```

* `custom-telegram.py` é o script responsável por processar o alerta JSON e enviar a mensagem para o Telegram.

---

## **3️⃣ Script de Integração (`custom-telegram.py`)**

````python
#!/usr/bin/env python3
import sys
import json
import requests

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

CHAT_ID = "-100SEU_CHAT_ID"

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

payload = {"chat_id": CHAT_ID, "text": msg_text, "parse_mode": "Markdown"}
headers = {'Content-Type': 'application/json'}

response = requests.post(hook_url, headers=headers, json=payload)
if response.status_code != 200:
    print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
    sys.exit(1)

sys.exit(0)
````

**Permissões de execução:**

```bash
chmod +x /var/ossec/integrations/custom-telegram/custom-telegram.py
```

---

## **4️⃣ Configuração no Wazuh**

Adicione a integração no arquivo `ossec.conf`:

```xml
<integration>
  <name>custom-telegram</name>
  <level>3</level>
  <hook_url>https://api.telegram.org/bot<COLOQUE_AQUI_ID_BOT>/sendMessage</hook_url>
  <alert_format>json</alert_format>
</integration>
```

* `<level>`: nível mínimo de alerta que será enviado.
* `<hook_url>`: URL da API do Telegram com o token do bot.

Reinicie o Wazuh para aplicar:

```bash
systemctl restart wazuh-manager
```

---

## **5️⃣ Testando a Integração**

Para testar, use o **logtest** do Wazuh:

```bash
/var/ossec/bin/ossec-logtest
```

Ou envie um alerta de nível ≥ 3 e verifique se a mensagem chega no Telegram.

---

## **6️⃣ Observações**

* Use Markdown para formatar mensagens.
* Emojis podem ser incluídos para destacar alertas.
* Certifique-se de que o bot está no grupo e tem permissão para enviar mensagens.

---

Se quiser, posso criar uma **versão do README com cURL de teste pronto**, simulando um alerta completo do Wazuh, para validar antes de gerar alertas reais.

Quer que eu faça isso?
