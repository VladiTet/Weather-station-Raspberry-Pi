import time#Модулът time позволява работа с времето в Python. Позволява функции
#като получаване на текущото време, спиране на изпълнението на програмата и др
from gpiozero import Button, MCP3008
#Модулът позовлява работа със сензор MCP3008
import math
#Модулът позволява работа с математически функции, които са дефинирани
#по C стандарт
import statistics
#Вградена библиотека за дискриптивна статистика


"""
    TODO: Описание на класа
"""
#Клас за работа със Analog-to-Digital Converter MCP3008
class Wind:
    """
    TODO:
    Описание на конструктура
    """
    #Конструктор на класа
    def __init__(self):
        self.__sensor_temp_bme = None
        self.__sensor_temp_w1therm = None
        self.__interval = 5
        self.wind_count = 0
        self.__rain_count = 0
        self.__gust = 0
        self.__store_speeds = []
        self.__store_directions = []
        self.__BUCKET_SIZE = 0.2794
        self.__radius_cm = 9.0
        self.wind_inerval = 5
        self.__count = 0
        self.__values = []
        """TODO:
            Да се изнесат volts в конфигурационен файл;
            Да се предвиди преизчисляване спрямо позицията на станцията;
            В момента е предвидено, че Резистор с номиналното съпротивление 10 000 мили Ома е в позиция север;
        """
        self.volts = {0.4: 0.0, 1.4: 22.5, 1.2: 45.0, 2.8: 67.5,
                      2.9: 112.5, 2.2: 135.0, 2.5: 157.5, 1.8: 180.0,
                      2.0: 202.5, 0.7: 225.0, 0.8: 247.5, 0.1: 270.0,
                      0.3: 292.5, 0.2: 315.0, 0.6: 337.5, 2.7: 90.0}

    """RainFall метод, NotImplemented"""
    #Метод - брояч на отчитания на изливане на контейнер за вода

    def __bucket_tipped(self):
        self.__rain_count = self.__rain_count + 1

    """RainFall метод, NotImplemented"""

#Метод – нулиране на брояч, отитащ брой отчитания – напълнен контейнер
    def __reset_rainfall(self):
        self.__rain_count = 0

#Метод – нулиране на брояч при изчисление на скорост на вятъра
    def _reset_wind(self):
        self.wind_count = 0

#Метод – нулиране на параметър – порив на вятъра
    def __reset_gust(self):
        self.__gust = 0

#Метод – увеличаване на брояч на брой завъртания на анемометъра
    def _spin(self) -> None:
        self.wind_count = self.wind_count + 1

#Метод за изчисление на скорост на вятъра
    def __calculate_speed(self, time_sec: int) -> float:
        CM_IN_A_KM = 100000.0
        ADJUSTMENT = 1.18
        SECS_IN_AN_HOUR = 3600
        circumference_cm = (2 * math.pi) * self.__radius_cm
        rotations = self.wind_count / 2.0

        dist_km = (circumference_cm * rotations) / CM_IN_A_KM

        km_per_sec = dist_km / time_sec
        km_per_hour = km_per_sec * SECS_IN_AN_HOUR

        return km_per_hour * ADJUSTMENT

#Метод за изчисление посоката на вятъра
    def __get_average(self, angles: list):

        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))

        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 and c > 0:
            average = arc + 360

        return 0.0 if average == 360 else average

#Метод за изчитане от сензора на параметри за изчисление на порив на вятъра, скорост на вятъра
    def get_value(self, lng=5):
        windi = windi_direction = None
        adc = MCP3008(channel=0)
        data = []
        start_time = time.time()
        volts = {0.4: 0.0, 1.4: 22.5, 1.2: 45.0, 2.8: 67.5,
                 2.9: 112.5, 2.2: 135.0, 2.5: 157.5, 1.8: 180.0,
                 2.0: 202.5, 0.7: 225.0, 0.8: 247.5, 0.1: 270.0,
                 0.3: 292.5, 0.2: 315.0, 0.6: 337.5, 2.7: 90.0}

        while time.time() - start_time <= lng:
            windi = round(adc.value * 3.3, 1)
            if windi in volts:
                data.append(volts[windi])
                # print(wind, volts[wind])
            if len(data) > 0:
                windi_direction = self.__get_average(data)
            else:
                windi_direction = False

        return windi, windi_direction

#Метод за взимане на показания на сензора
    def measure(self):
        wind_average = wind_gust = wind_speed = rainfall = None
        wind_speed_sensor = Button(5)
        wind_speed_sensor.when_pressed = self._spin
        store_directions = []
        start_time = time.time()
        store_speeds = []
        #Изчитане на показанията на определен времеви интервал
        while time.time() - start_time <= self.__interval:
            wind_start_time = time.time()
            self._reset_wind()

            while time.time() - wind_start_time <= self.wind_inerval:
                #Изчитане на показанията за скорост на вятъра, посока на вятъра
                wind, wind_direction = self.get_value()
                if not wind_direction == False:
                    store_directions.append(wind_direction)
                    #Изчисление на скорост на вятъра
            final_speed = self.__calculate_speed(self.wind_inerval)
            store_speeds.append(final_speed)

        if len(store_directions) > 0:
            wind_average = self.__get_average(store_directions)
        else:
            wind_average = 0.0
            #Стойност на порив на вятъра
        wind_gust = max(store_speeds)
        #Стойност на скорост на вятъра
        wind_speed = statistics.mean(store_speeds)
        #Изчисление на валеж на единица площ
        rainfall = self.__rain_count * self.__BUCKET_SIZE
        self.__reset_rainfall()
        return wind_average, wind_gust, wind_speed, rainfall
