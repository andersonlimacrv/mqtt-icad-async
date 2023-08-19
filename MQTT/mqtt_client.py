import paho.mqtt.client as mqtt
import logging
import random
import time
import json
import asyncio


class MQTTClient:
    def __init__(self, broker, port, topic, username, password, context_topics):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.context_topics = context_topics
        self.client_id = f"CLIENT_ID_{random.randint(0, 1000)}"
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.received_messages = []
        self.subscribed_topics = []
        

    def connect(self):
        self.client.will_set(
            self.topic,
            payload=f"Client {self.client_id} Disconnected",
            qos=1,
            retain=False,
        )
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port, keepalive=3)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
        logging.info("Disconnected from MQTT Broker!")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0 and client.is_connected():
            logging.info("Connected to MQTT Broker!")

            client.subscribe(self.topic)
            self.client.publish(
                self.topic,
                payload=f"Client {self.client_id} Connected",
                qos=1,
                retain=False,
            )
            self.subscribed_topics.append(self.topic)

            for topic in self.context_topics:
                client.subscribe(topic)
                self.subscribed_topics.append(topic)

        else:
            logging.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logging.info("Disconnected with result code: %s", rc)
        if rc != 0:
            logging.info("Publishing Last Will message...")
            self.publish(f"{self.client_id} Disconnected")
        reconnect_count, reconnect_delay = 0, 1
        while reconnect_count < 12:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                self.client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= 2
            reconnect_delay = min(reconnect_delay, 60)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
        global FLAG_EXIT
        FLAG_EXIT = True

    def on_message(self, client, userdata, msg):
        logging.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        self.received_messages.append({
            'topic': msg.topic,
            'payload': msg.payload.decode()
        })

    def get_received_messages(self):
        return self.received_messages

    def get_subscribed_topics(self):
        return self.subscribed_topics

    def publish(self, topic, payload):
        if not self.client.is_connected():
            logging.error("publish: MQTT client is not connected!")
            return
        msg = payload
        result = self.client.publish(topic, msg)
        status = result.rc
        if status == mqtt.MQTT_ERR_SUCCESS:
            logging.info(f"Send `{msg}` to topic `{topic}`")
        else:
            logging.error(f"Failed to send message to topic {topic}")

    def is_connected(self):
        return self.client.is_connected()

    def subscribe(self, topic):
        if not self.is_connected():
            logging.error("subscribe: MQTT client is not connected!")
            return 
        self.client.subscribe(topic)
        self.subscribed_topics.append(topic)
        logging.info(f"Subscribed to topic {topic}")

    def unsubscribe(self, topic):
        if not self.is_connected():
            logging.error("unsubscribe: MQTT client is not connected!")
            return 
        self.client.unsubscribe(topic)
        self.subscribed_topics.remove(topic)
        logging.info(f"Unsubscribed from topic {topic}")


    def on_subscribe(self, client, userdata, mid, granted_qos):
        for topic in userdata:
            self.subscribed_topics.append(topic)

    def on_unsubscribe(self, client, userdata, mid):
        for topic in userdata:
            self.subscribed_topics.remove(topic)

    async def start(self):
        logging.basicConfig(
            filename="mqtt.log",
            format="%(asctime)s - %(levelname)s: %(message)s",
            level=logging.DEBUG,
        )
        self.connect()
        while not FLAG_EXIT:
            await asyncio.sleep(1)

        self.disconnect()

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "python-mqtt/tls"
USERNAME = ""
PASSWORD = ""

FLAG_EXIT = False

if __name__ == "__main__":
    mqtt_client = MQTTClient(BROKER, PORT, TOPIC, USERNAME, PASSWORD)
    asyncio.run(mqtt_client.start())
    mqtt_client.disconnect()
