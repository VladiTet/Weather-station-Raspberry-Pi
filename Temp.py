import bme680
from w1thermsensor import W1ThermSensor
"""
Описание на класа
"""
class Temp:
    """
    TODO:
    Описание на конструктура
    """
    def __init__(self):
        self.__w1thermsensor    = None
        self.__sensor_bme680    = None
        self.temperature      = None
        self.pressure         = None
        self.humidity         = None
        self.gas_resistance   = None
        self.w1therm          = None

    """
    TODO: 
    Описание на метода
    """
    def __set_sensors(self):
        try:
            self.__sensor_bme680 = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.__sensor_bme680 = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        try:
            self.__w1thermsensor = W1ThermSensor()
        except Exception as e:
            print(e)
            pass
        if self.__sensor_bme680:
            self.__sensor_bme680.set_humidity_oversample(bme680.OS_2X)
            self.__sensor_bme680.set_pressure_oversample(bme680.OS_4X)
            self.__sensor_bme680.set_temperature_oversample(bme680.OS_8X)
            self.__sensor_bme680.set_filter(bme680.FILTER_SIZE_3)
            self.__sensor_bme680.set_gas_status(bme680.ENABLE_GAS_MEAS)
            self.__sensor_bme680.set_gas_heater_temperature(320)
            self.__sensor_bme680.set_gas_heater_duration(150)
            self.__sensor_bme680.select_gas_heater_profile(0)

    """
    TODO: 
    Описание на метода
    """
    def measure(self):
        temperature = None
        pressure = None
        humidity = None
        gas_resistance = None
        w1therm = None

        try:
            self.__set_sensors()
            try:
                state = False
                while state == False:
                    state = self.__sensor_bme680.get_sensor_data()
                    if state == True:
                        temperature = self.__sensor_bme680.data.temperature
                        pressure = self.__sensor_bme680.data.pressure
                        humidity = self.__sensor_bme680.data.humidity
                        gas_resistance = self.__sensor_bme680.data.gas_resistance
                if self.__w1thermsensor:
                    w1therm = self.__w1thermsensor.get_temperature()
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass




        return temperature, pressure, humidity, gas_resistance, w1therm
