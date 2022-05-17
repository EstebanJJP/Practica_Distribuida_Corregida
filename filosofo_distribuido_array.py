from multiprocessing import Process, Array
from multiprocessing import Lock

import paho.mqtt.client as mqtt
"ESTA ES UNA VERSION DONDE LA LISTA DE BOOLEANOS LA HE HECHO COMO UN ARRAY COMPARTIDO, PERO OBTENGO LOS MISMOS PROBLEMAS"
NPHIL =5

mqttBroker = "mqtt.eclipseprojects.io"
# mqttBroker = "wild.mat.ucm.es"
client = mqtt.Client()
client.connect(mqttBroker)

data_eat = Array('i',[0,0,0,0,0])
data_think = Array('i',[0,0,0,0,0])

def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    num = int(msg)
    topic = message.topic
    if topic == "Rwants_eat":
        data_eat[num] = 1
    else:
        data_think[num] = 1
    
def philosopher_task(num:int, lock):
    client.subscribe("Rwants_eat")
    client.subscribe("Rwants_think")
    client.publish("Current_phil", num)
    while True:
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        client.publish("wants_eat", num)
        while (data_eat[num]==0):
            client.loop_start()
            client.on_message = on_message
            client.loop_stop()
        data_eat[num] = 0
        print (f"Philosofer {num} eating")
        client.publish("wants_think", num)
        while (data_think[num]==0):
            client.loop_start()
            client.on_message = on_message
            client.loop_stop()
        data_think[num]=0
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