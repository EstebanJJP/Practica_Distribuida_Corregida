from multiprocessing import Process
from multiprocessing import Lock

import paho.mqtt.client as mqtt

NPHIL =5

mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "wild.mat.ucm.es"
client = mqtt.Client()
client.connect(mqttBroker)

data_eat = [False]*5
data_think = [False]*5

def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    topic = msg.topic
    if topic == "Rwants_eat":
        data_eat[msg] = True
    else:
        data_think[msg] = True
    
def philosopher_task(num:int, lock):
    client.subscribe("Rwants_eat")
    client.subscribe("Rwants_think")
    client.publish("Current_phil", num)
    while True:
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        client.publish("wants_eat", num)
        while not(data_eat[num]):
            client.on_message = on_message
        data_eat[num] = False
        print (f"Philosofer {num} eating")
        client.publish("wants_think", num)
        while not(data_think[num]):
            client.on_message = on_message
        data_think[num]=False
        print (f"Philosofer {num} stops eating")
        
        
def main():
    lock = Lock()
    philosofers = [Process(target=philosopher_task, args=(i,lock)) \
                   for i in range(NPHIL)]
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()
if __name__ == '__main__':
    main()

