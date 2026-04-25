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

## 📢 Channels

Channels define where alerts are sent.

### Example:

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

### 🔍 Notes

* Supports **environment variables** via `${VAR_NAME}`
* Multiple `chat_ids` supported
* You can define multiple channels and reuse them across services

---

## 🖥️ Services

Each service defines what should be monitored.

### Example:

```yaml
services:
  - name: street
    check:
      type: http
      url: http://192.168.88.227
      expected_status: 200

  - name: nas
    interval: 30
    check:
      type: tcp
      host: 192.168.88.225
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

## 🔔 Notifications

### Default behavior

* On failure → alert is sent
* On recovery → optional `up_message` is sent

### Example alerts

```
❌ Service DOWN: nas (tcp 192.168.88.225:22)
```

```
✅ Service UP: light
Power is up!
```

---

## ▶️ Run

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

## 🧩 Extending

### Add new check

1. Create file in `checks/`
2. Implement base interface
3. Register in `CHECK_REGISTRY`

---

### Add new channel

1. Create file in `channels/`
2. Implement `send()`
3. Register in `CHANNEL_REGISTRY`

---

## 📌 Roadmap

* [ ] Retry logic
* [ ] Alert deduplication
* [ ] Cooldown / silence mode
* [ ] Prometheus metrics
* [ ] Web UI
* [ ] Config hot reload

---

## 📄 License

MIT
