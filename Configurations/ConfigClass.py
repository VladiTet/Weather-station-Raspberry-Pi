from pathlib import Path
import os
from typing import *
import configparser

class Config():
    """
    TODO:
        Описание на класа
    """

    def __init__(self, conf_fileName=None, conf_dir=None, conf_type="ini"):
        """Конструктор на класа """
        if conf_fileName:
            self.conf_fileName = conf_fileName
        else:
            self.conf_fileName = "config.ini"
        if conf_dir:
            self.config_dir = conf_dir
        else:
            self.config_dir = Path(__file__).parent.parent

        self.conf_type = conf_type
        self.__set()

    def __initial_config(self):
        self.configuration.add_section('System.Runtime')
        self.configuration.set('System.Runtime', '; Автоматично генерирано при пуск и лиспса на конфигурации', None)
        self.configuration.set('System.Runtime', 'enable', '1')
        self.configuration.set('System.Runtime', 'transfer', '1')
        self.configuration.set('System.Runtime', 'ssl', '1')
        self.configuration.add_section('Comunications.Systems')
        self.configuration.set('Comunications.Systems', '; Автоматично генерирано при пуск и лиспса на конфигурации', None)
        self.configuration.set('Comunications.Systems', 'protocol', 'mqtt')
        self.configuration.set('Comunications.Systems', 'schema', 'https://')
        self.configuration.set('Comunications.Systems', 'host', 'iot.scrtl.xyz')
        self.configuration.set('Comunications.Systems', 'port', '8883')
        self.configuration.set('Comunications.Systems', 'user', 'vladimirtet:mqttuser')
        self.configuration.set('Comunications.Systems', 'password', '59f7de71-3e8e-4278-af96-a5dbc40c57a5')
        self.configuration.set('Comunications.Systems', 'cert', '/home/pi/Application/Project/BME680/secure/iot.scrtl.xyz.pem')
        self.configuration.add_section('Comunications.Topics')
        self.configuration.set('Comunications.Topics', '; Автоматично генерирано при пуск и лиспса на конфигурации', None)
        self.configuration.set('Comunications.Topics', 'humidity', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'lowPowerGas', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'pressure', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'temperature', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'windSpeed', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'windGust', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'windDirectionCustom', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'rainFall', '78pPLEWoCKPWMRhc2jqpXT')
        self.configuration.set('Comunications.Topics', 'groundTemperature', '78pPLEWoCKPWMRhc2jqpXT')
        


        self.configuration.write(Path(self.config_file).open("w") )

    def __set(self):
        assert os.path.isdir(self.config_dir) == True, "Directory not found"
        self.config_file = os.path.join(self.config_dir, self.conf_fileName)
        self.__get()
        if len(self.configuration.sections()) < 3:
            self.__initial_config()


    def __get(self):
        self.configuration = configparser.RawConfigParser(allow_no_value=True)
        self.configuration.optionxform = lambda option: option 
        self.configuration.read(self.config_file)
        self.configuration.optionxform = str


    def section(self):
        return self.configuration.sections()

    def add_section(self, section):
        print(f"Conf: {section}")
        try:
            self.configuration.add_section(f'{section}')
        except Exception as e:
            print(e)
    def remove_section(self, section):
        print(f"Conf: {section}")
        try:
            self.configuration.remove_section(f'{section}')
        except Exception as e:
            print(e)

    def set_value(self, section, param, value):
        try:
            self.configuration.set(section, param, value)
        except Exception as e:
            print(f"Section {section}, Param {param}, Value {value}, Error {e}")

    def save(self):
        self.configuration.write(Path(self.config_file).open("w") )
#
#
# conf = Config()

