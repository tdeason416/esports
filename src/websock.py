 # ws://stream.meetup.com/2/rsvps

from websocket import create_connection
from kafka import KafkaProducer
import time
import json


def start_stream(
    ws = create_connection("ws://stream.meetup.com/2/rsvps")
    while True:
        result_json = ws.recv()
        # print("Received '%s'" % result_json)
        payload = json.loads(result_json)
        data = {}
        group_topic_list = []
        data["event_id"] = payload["event"]["event_id"]
        data["event_name"] = payload["event"]["event_name"]
        data["event_url"] = payload["event"]["event_url"]
        data["group_city"] = payload["group"]["group_city"]
        data["group_id"] = payload["group"]["group_id"]
        data["group_country"] = payload["group"]["group_country"]
        if "group_state" in payload["group"]:
        data["group_state"] = payload["group"]["group_state"]
        gtl = payload["group"]["group_topics"]
        for gt in gtl:
        group_topic_list.append(gt["urlkey"])
        
        data["group_topic_list"] = group_topic_list
        data["guests"] = payload["guests"]
        data["member_id"] = payload["member"]["member_id"]
        data["rsvp_id"] = payload["rsvp_id"]
        data["mtime"] = payload["mtime"]
        
        json_data = json.dumps(data)
        # print(json_data)
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        
        producer.send('meetup-rsvp', json_data)
        time.sleep(1)
    
    producer.close()


