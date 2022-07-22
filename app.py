#!/bin/python3
from flask import Flask, request
from influxdb import InfluxDBClient
import sys
import time
import os

app = Flask(__name__)
HOST = os.environ.get("HOST", "localhost")
try:
    client = InfluxDBClient(host=HOST, port=8086)
except:
    print("failed to connect to influx")
    exit(1)

def generic_write(data, database="discord"):
    try:
        timestamp = int(time.time())
        client.write_points(data+f" {timestamp}", database=database, time_precision="s", protocol="line")
        return f"", 200
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return f"{str(exc_type)}: {exc_value}\n{exc_traceback}", 500

@app.post("/v1/data/<bot>/<guild>/<channel>")
def upload_data(bot, guild, channel):
    data = f"use,bot={bot},guild={guild},channel={channel} value=1"
    return generic_write(data)

@app.post("/v1/guild/<bot>/<count>")
def update_guild_count(bot, count):
    data = f"guild_count,bot={bot} value={count}"
    return generic_write(data)

@app.post("/v1/log/<bot>")
def upload_log(bot):
    required = ["message", "level"]
    for x in required:
        if x not in request.form:
            return f"missing {x}", 400
    content = request.form["message"]
    level = request.form["level"]
    data = f"log,bot={bot},level={level} value=\"{content}\""
    return generic_write(data)

@app.post("/v1/guild_name/<guild>")
def update_guild_name(guild):
    if "name" not in request.form:
        return f"missing name", 400
    data = f"guild_names,guild={guild} value=\"{request.form['name']}\""
    return generic_write(data)
