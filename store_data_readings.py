"""A demo of subscribing to MQTT
"""
import getpass
import json
import os.path
import random
import ssl

from paho.mqtt import client as mqtt_client

from db.data_sqlite3 import SQLite3db

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

SQLITE3_DB = os.path.join(ROOT_DIR, "db/data_readings.db")

# Establish a DB depending on the existence of ../secrets/mysql.json
db = SQLite3db(SQLITE3_DB)

# Client IDs must be random
CLIENT_ID = f"python-roller-mqtt-{random.randint(0, 4095)}"
TOPIC = "au701034/airquality"
MQTT_SECRETS = {}

MQTT_SECRETS_FILE = os.path.join(ROOT_DIR, "../secrets/mqtt.json")
# Get username/password from ../secrets/mqtt.json or user input
if os.path.exists(MQTT_SECRETS_FILE):
    with open(MQTT_SECRETS_FILE, "r", encoding="UTF8") as secrets:
        MQTT_SECRETS = json.load(secrets)
else:
    MQTT_SECRETS["USERNAME"] = input("Username: ")
    MQTT_SECRETS["PASSWORD"] = getpass.getpass("Password:  ")

MQTT_SECRETS["BROKER"] = "itwot.mooo.com"
MQTT_SECRETS["PORT"] = 8883


def connect_mqtt():
    """Creates a MQTT client

    Returns:
        client: a MQTT client
    """

    def on_connect(client, _userdata, _flags, return_code):
        if return_code == 0:
            print(f"Connected to {MQTT_SECRETS['BROKER']}")
            client.subscribe(TOPIC)
        else:
            print(f"Failed to connect, return code {return_code}")

    def on_message(_client, _userdata, msg):
        data = json.loads(msg.payload)
        tvoc = data["tvoc"]
        eco2 = data["eco2"]
        print(f"Message received [{msg.topic}]: {data}")
        db.store_data_readings(tvoc, eco2)

    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(MQTT_SECRETS["USERNAME"], MQTT_SECRETS["PASSWORD"])
    client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SECRETS["BROKER"], MQTT_SECRETS["PORT"])
    return client


def run():
    """Get the MQTT client going"""
    client = connect_mqtt()
    client.loop_forever()


if __name__ == "__main__":
    run()
