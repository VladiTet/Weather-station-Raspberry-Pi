import time
import random
import ssl
from typing import *
"""
    TODO:    
    Да се оправи анотацията на променливите;
    Да се прихванат възможните exceptions и да се обработят;
    Да се използват глобални променливи;
    
"""

"""Импортиране на външни библиотеки"""
from paho.mqtt import client as mqtt_client

"""Импортиране на собствени модули"""
from Temp import Temp
from Wind import Wind
from Configurations.ConfigClass import Config

"""Инициализация на клас Config"""
conf = Config()
"""Инициализация на секциите от Config"""
sys_conf = conf.configuration.__getitem__('System.Runtime')
mqtt_conf = conf.configuration.__getitem__('Comunications.Systems')
topics_conf = conf.configuration.__getitem__('Comunications.Topics')
"""Генериране на клиент за връзка с mqtt server"""
client_id = f"python-mqtt-{random.randint(0, 1000)}"
"""инициализация на речник за топици за mqtt"""
topics = {}

"""Напълване на речник за топици"""
for v in topics_conf:
    topics[v] = topics_conf.get(str(v))


"""Метод за конструиране на вързка с mqtt server"""
def connect_mqtt() -> object:
    def on_connect(client, userdata, flags, rc):
        # print(rc)
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    """Сетване на атрибути към клиента"""
    client = mqtt_client.Client(client_id)
    client.username_pw_set(mqtt_conf.get('user'), mqtt_conf.get('password'))
    client.on_connect = on_connect
    client.tls_set(mqtt_conf.get('cert'), tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)
    client.connect(mqtt_conf.get('host'), mqtt_conf.getint('port'))

    return client


"""Метод за публикуване към топик в mqtt server"""
def publishing(mq_client, topic, value) -> bool:
    pub_result = mq_client.publish(topic, value)
    status = pub_result[0]
    if status == 0:
        # print(f"Send {str(value)} to topic `{topic}`")
        return True
    else:
        print(f"Failed to send message to topic {topic}")
        return False


"""Инициализране на клиент"""
try:
    client_pub = connect_mqtt()
except Exception as e:
    print(e)
    pass

"""Метод за конструиране на топици"""
def construct_url(attribute_type, assetid, attribute_name) -> str:
    url = f"{attribute_type}/{assetid}/{attribute_name}"

    return url

"""Mетод за обработка и изпращане на топици към mqtt server"""
def sent(temperature, pressure, humidity, lowPowerGas, groundTemperature, windDirection, windGust, windSpeed, rainFall) -> None:
    urls = []
    urls.append((construct_url("attributevalue", topics['temperature'], "temperature"), temperature))
    urls.append((construct_url("attributevalue", topics['pressure'], "pressure"), pressure))
    urls.append((construct_url("attributevalue", topics['humidity'], "humidity"), humidity))
    urls.append((construct_url("attributevalue", topics['lowPowerGas'], "lowPowerGas"), lowPowerGas))
    urls.append((construct_url("attributevalue", topics['groundTemperature'], "groundTemperature"), groundTemperature))
    urls.append((construct_url("attributevalue", topics['windDirectionCustom'], "windDirectionCustom"), windDirection))
    urls.append((construct_url("attributevalue", topics['windGust'], "windGust"), windGust))
    urls.append((construct_url("attributevalue", topics['windSpeed'], "windSpeed"), windSpeed))
    urls.append((construct_url("attributevalue", topics['rainFall'], "rainFall"), rainFall))
    """
        TODO: Да се предвиди променливата от конфигурационнен файл `transfer`
        спрямо нея да се прави заявка към сървъра
        Тази променлива трябва да се достъпва чрез mqtt от отделен service,
        който да я сетва.            
    """
    for url in urls:
        try:
            publishing(client_pub, url[0], url[1])
        except Exception as e:
            print(e)
            pass

        time.sleep(1)
"""Метод за стартиране на бизнес логиката"""
def start():
    temp = Temp()
    wind = Wind()
    while True:
        measure = []
        try:
            """
                TODO: Да се предвиди променливата от конфигурационнен файл `enable`
                спрямо нея да се прави измерването.
                Тази променлива трябва да се достъпва чрез mqtt от отделен service,
                който да я сетва.            
            """
            temperature, pressure, humidity, lowPowerGas, groundTemperature = temp.measure()
            measure.extend([temperature, pressure, humidity, lowPowerGas, groundTemperature])
            windDirection, windGust, windSpeed, rainFall = wind.measure()
            measure.extend([round(windDirection, 1), windGust, windSpeed, rainFall])

            sent(*measure)

        except Exception as e:
            print(e)
