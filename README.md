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

**Permissões de execução:**

```bash
chmod 750 /var/ossec/integrations/custom-telegram
chown root:wazuh /var/ossec/integrations/custom-telegram

chmod 750 /var/ossec/integrations/custom-telegram.py
chown root:wazuh /var/ossec/integrations/custom-telegram.py
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
