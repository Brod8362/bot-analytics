Discord analytics microservice
==============================

Concept:
- Bots upload very basic usage statistics here
- API pushes them to the influxDB
- Grafana pulls from Influx DB to make pretty graphs

## Endpoints

**POST** `/v1/data/<bot>/<guild>/<channel>`
- Log a usage of the bot in a given guild/channel.
- Expects guild/channel snowflakes.
- EX: `/v1/data/knuckles/189571157446492161/197743857889312778`

**POST** `/v1/guild/<bot>/<count>`
- Send an update of the bot's current guild count.
- EX: `/v1/guild/knuckles/650`

**POST** `/v1/log/<bot>`
- FORM DATA: `message` -> string, `level` -> string
- Levels are `log`, `warn`, `error`

## Setup
```bash
docker build -t botms:latest .
docker run -d --restart unless-stopped botms:latest
```