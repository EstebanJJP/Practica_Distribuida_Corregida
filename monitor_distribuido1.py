"""Monitor distribuido:
   Ejecutar primero este programa para que pueda ir recibiendo mensajes
   Pedirá un input del número de filósofos que deseamos utilizar, tantos como programas de filosofo_distribuido2.py queramos abrir en una terminal aparte"""

from multiprocessing import Lock,Condition, Manager
from multiprocessing import Value
import paho.mqtt.client as mqtt

class Table():
    def __init__(self, NPHIL, manager):
        self.currentphil = None
        self.neating = Value('i',0)
        self.phil = manager.list([False]*NPHIL)
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        
    def set_current_phil(self, i):
        self.currentphil = i
        
    def nocomenlados(self):
        return self.phil[(self.currentphil - 1) % len(self.phil)] == False and self.phil[(self.currentphil +1)%len(self.phil)] == False

    def wants_eat(self,i):
        self.mutex.acquire()
        self.freefork.wait_for(self.nocomenlados)
        self.phil[i] = True
        self.neating.value += 1
        self.mutex.release()

    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.neating.value -= 1
        self.freefork.notify_all()
        self.mutex.release()
    
manager = Manager()
nphil = input('¿Cuántos filósofos va a ejecutar? ')
table= Table(int(nphil),manager)
def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    num = int(msg)
    topic = message.topic
    if topic == "Current_phil":
        table.set_current_phil(num)
    elif topic == "wants_eat":
        print(num)
        table.wants_eat(num)
        client.publish("Rwants_eat", num)
    else:
        table.wants_think(num)
        client.publish("Rwants_think", num)

def main():
    mqttBroker = "mqtt.eclipseprojects.io"
    #mqttBroker = "wild.mat.ucm.es"
    client = mqtt.Client()
    client.connect(mqttBroker)
    client.subscribe("Current_phil")
    client.subscribe("wants_eat")
    client.subscribe("wants_think")
    client.on_message = on_message
    client.loop_forever()

if __name__ == '__main__':
     main()
