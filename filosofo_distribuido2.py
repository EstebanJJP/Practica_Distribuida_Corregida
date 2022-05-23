from multiprocessing import Semaphore
import paho.mqtt.client as mqtt
import sys



def on_message(client, userdata, message):
    msg = message.payload.decode("utf-8")
    num = int(msg)
    topic = message.topic
    if topic == "Rwants_eat":
        if num == numero:
            userdata['wants_eat'].release() 
    else:
        if num == numero:
            userdata['wants_think'].release()




def quiero_comer(num,user_data,client):
    client.publish("wants_eat",num)
    user_data['wants_eat'].acquire()

def quiero_pensar(num,user_data,client):
    client.publish("wants_think",num)
    user_data['wants_think'].acquire()


def main(num,user_data):
    mqttBroker = "mqtt.eclipseprojects.io"
    # mqttBroker = "wild.mat.ucm.es"
    client = mqtt.Client(userdata = user_data)
    client.connect(mqttBroker)
    client.subscribe("Rwants_eat")
    client.subscribe("Rwants_think")
    client.on_message = on_message
    client.loop_start()
    while True:
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        quiero_comer(num,user_data,client)
        print (f"Philosofer {num} eating")
        quiero_pensar(num,user_data,client)
        print (f"Philosofer {num} stops eating")
    
if len(sys.argv)>1:
    numero = sys.argv[1]

if __name__ == '__main__':
    user_data = {'wants_eat':Semaphore(0),'wants_think':Semaphore(0)}
    if len(sys.argv)>1:
        num = sys.argv[1]
        main(num,user_data)