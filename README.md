# 🚀 Monitoring Bot (TCP / HTTP / ICMP)

A lightweight, config-driven Python monitoring tool that checks service availability and sends alerts via notification channels (e.g. Telegram).

---

## ✨ Features

* 🔌 TCP port monitoring
* 🌐 HTTP/HTTPS health checks
* 📡 ICMP (ping) checks
* 📢 Multiple notification channels
* ⚙️ YAML-based configuration
* 🔄 Per-service intervals
* 🧩 Extensible architecture

---

## 📁 Project Structure

```bash
.
├── main.py
├── config.yaml
├── channels/
│   ├── __init__.py
│   ├── base.py
│   ├── telegram.py
├── checks/
│   ├── __init__.py
│   ├── base.py
│   ├── tcp.py
│   ├── http.py
│   ├── icmp.py
└── utils/
    └── logger.py
```

---

## ⚙️ Configuration

The application is fully configured via a YAML file.

### 🔧 Global Settings

```yaml
log_level: info
default_channel: telegram-dev
check_interval: 6
```

| Parameter         | Description                                         |
| ----------------- | --------------------------------------------------- |
| `log_level`       | Logging level (`debug`, `info`, `warning`, `error`) |
| `default_channel` | Channel used if a service does not specify one      |
| `check_interval`  | Default interval (seconds) between checks           |

---

# 📢 Channels

Channels define where alerts are sent.

**Example**

```yaml
channels:
  telegram-dev:
    type: telegram
    config:
      bot_token: ${TELEGRAM_BOT_TOKEN}
      chat_ids:
        - ${TELEGRAM_CHAT_ID_1}

  telegram-prod:
    type: telegram
    config:
      bot_token: ${TELEGRAM_BOT_TOKEN}
      chat_ids:
        - ${TELEGRAM_CHAT_ID_1}
        - ${TELEGRAM_CHAT_ID_2}
```

---

## 📲 Telegram Channel

The `telegram` channel allows sending alerts to one or multiple Telegram chats using a bot.

---

### ⚙️ Configuration Options

| Parameter   | Required | Type             | Description                                  |
| ----------- | -------- | ---------------- | -------------------------------------------- |
| `bot_token` | ✅        | string           | Telegram Bot API token                       |
| `chat_ids`  | ✅        | list[string/int] | List of chat IDs where messages will be sent |

---

### 💡 Notes

* `chat_ids` supports:

  * personal chats
  * group chats
  * channels (if bot has access)
* You can send alerts to multiple destinations at once
* Environment variables are supported (`${VAR_NAME}`)

---

### 🤖 How to Create a Telegram Bot Token

1. Open Telegram and search for BotFather

2. Start a chat and run:

   ```
   /start
   ```

3. Create a new bot:

   ```
   /newbot
   ```

4. Follow the instructions:

   * Set bot name
   * Set bot username

5. You will receive a token like:

   ```
   123456789:AAxxxxxxxxxxxxxxxxxxxx
   ```

👉 Official documentation:
[https://core.telegram.org/bots#how-do-i-create-a-bot](https://core.telegram.org/bots#how-do-i-create-a-bot)

---

### 💬 How to Get Your Chat ID

1. Open Telegram and search for:

   ```
   @userinfobot
   ```
2. Start the bot
3. It will return your **chat ID**


### ⚠️ Notes for Groups

* Add your bot to the group
* Send a message in the group
* Use `getUpdates` to retrieve the group `chat_id`
* Group IDs are usually negative numbers (e.g. `-1001234567890`)

---

### ✅ Example with Environment Variables

```yaml
channels:
  telegram:
    type: telegram
    config:
      bot_token: ${TELEGRAM_BOT_TOKEN}
      chat_ids:
        - ${TELEGRAM_CHAT_ID}
```

```bash
export TELEGRAM_BOT_TOKEN=123456:ABC...
export TELEGRAM_CHAT_ID=123456789
```

---

# 🖥️ Services

Each service defines what should be monitored.

**Example:**

```yaml
services:
  - name: router
    check:
      type: icmp
      host: 8.8.8.8
  - name: nas
    interval: 30
    check:
      type: tcp
      host: 1.1.1.1
      port: 22

  - name: light
    check:
      type: icmp
      host: light.h.com
    up_message: "Power is up!"
    down_message: "Power is down!"
    channels:
      - telegram-prod
```

---

## 🔎 Service Parameters

| Parameter      | Required | Description                          |
| -------------- | -------- | ------------------------------------ |
| `name`         | ✅       | Service name                         |
| `check.type`   | ✅       | `http`, `tcp`, `icmp`                |
| `interval`     | -        | Override global interval             |
| `channels`     | -        | List of channels                     |
| `up_message`   | -        | Custom message when service recovers |
| `down_message` | -        | Custom message on failure            |

---

## 🔍 Check Types

### 🌐 HTTP

```yaml
check:
  type: http
  url: http://example.com
  expected_status: 200
```

---

### 🔌 TCP

```yaml
check:
  type: tcp
  host: 192.168.1.1
  port: 22
```

---

### 📡 ICMP

```yaml
check:
  type: icmp
  host: example.com
```

---

# 🔔 Notifications configuration

## Default behavior

* On failure → alert is sent, `down_message`
* On recovery → `up_message` is sent
* If not configured then default is sent

## Example alerts

```
❌ Service DOWN: nas (tcp 192.168.88.225:22)
```

```
✅ Service UP: light
Power is up!
```

---

# ▶️ Run locally

```bash
pip install -r requirements.txt
python main.py
```

---

## 🔐 Environment Variables

You can inject secrets via environment variables:

```bash
export TELEGRAM_BOT_TOKEN=xxx
export TELEGRAM_CHAT_ID_1=123456
```

---

# 🐳 Run with Docker Compose

## 📄 `docker-compose.yaml`


```yaml
services:
  vartovyi:
    image: ghcr.io/adskyiproger/vartovyi:latest
    restart: unless-stopped
    volumes:
      - ./bot.yaml:/app/bot.yaml:ro
    environment:
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
      TELEGRAM_CHAT_ID: ${TELEGRAM_CHAT_ID}

```

## config.yaml

Create `bot.yaml` in the same directory as `docker-compose.yaml`, see example at [bot.yaml](bot.yaml)

---

## 🔐 Environment Variables

Create file `.env` in the same folder as `docker-compose.yaml`:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## ▶️ Run

```bash
docker compose up -d
```

---

## 📜 Logs

```bash
docker compose logs -f
```

---

## 🛑 Stop

```bash
docker compose down
```

# 🧩 Extending

## Add new check

1. Create file in `checks/`
2. Implement base interface
3. Add configuration to bot.yaml

---

## Add new channel

1. Create file in `channels/`
2. Implement `send()`
3. Add configuration to bot.yaml

---

# 📌 Roadmap

* [ ] Retry logic
* [ ] Alert deduplication
* [ ] Cooldown / silence mode
* [ ] Prometheus metrics
* [ ] Web UI
* [ ] Config hot reload

---

# 📄 License

MIT
