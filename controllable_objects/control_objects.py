from controllable_objects.specific.shift_reg.trigger import Trigger
from controllable_objects.specific.shift_reg.slider import Slider
from connections.shift_reg_wrapper import ShiftRegWrapper

import logging


class ControlObjects(object):

    def __init__(self):
        """
        Конструктор, производит иницализацию всех компонентов, необходимых для вывода
        :return: none
        """
        logging.debug("{0} init started".format(self))

        # устанавливаем пины
        si = 37    # пин для входных данных
        rck = 33   # пин для сдвига регистров хранения
        sck = 35   # пин для синхросигнала и сдвига
        sclr = 40  # пин для очистки

        self.shift_reg = ShiftRegWrapper(si, sck, rck, sclr, 2)

        door_1_plus  = 0
        door_1_minus = 1
        door_2_plus  = 2
        door_2_minus = 3
        diode_1 = 4
        diode_2 = 5
        door_3_plus  = 6
        door_3_minus = 7
        blind_1_plus  = 8
        blind_1_minus = 9
        blind_2_plus  = 10
        blind_2_minus = 11
        diode_3 = 12
        diode_4 = 13
        blind_3_plus  = 14
        blind_3_minus = 15
        blind_4_plus  = 16
        blind_4_minus = 17
        diode_5 = 18
        diode_6 = 19
        cooler  = 20

        # FIXME: Not shifts
        self.door_shifts = {
            'Entrance door':    Slider(self.shift_reg, Slider.PinStruct(door_1_plus, door_1_minus)),
            'Bedroom door':     Slider(self.shift_reg, Slider.PinStruct(door_2_plus, door_2_minus)),
            'Office door':      Slider(self.shift_reg, Slider.PinStruct(door_3_plus, door_3_minus))
        }

        self.room_led_shifts = {
            'Corridor':     Trigger(self.shift_reg, diode_1),
            'Kitchen':      Trigger(self.shift_reg, diode_2),
            'Bathroom':     Trigger(self.shift_reg, diode_3),
            'Bedroom':      Trigger(self.shift_reg, diode_4),
            'Office':       Trigger(self.shift_reg, diode_5),
            'Living Room':  Trigger(self.shift_reg, diode_6)
        }

        self.coolers_shifts = {
            'cooler':       Trigger(self.shift_reg, cooler)
        }

        self.blind_shifts = {
            'Kitchen':      Slider(self.shift_reg, Slider.PinStruct(blind_1_plus, blind_1_minus)),
            'Bedroom':      Slider(self.shift_reg, Slider.PinStruct(blind_2_plus, blind_2_minus)),
            'Office':       Slider(self.shift_reg, Slider.PinStruct(blind_3_plus, blind_3_minus)),
            'Living Room':  Slider(self.shift_reg, Slider.PinStruct(blind_4_plus, blind_4_minus))
        }

        logging.debug("{0} init finished".format(self))

    def __del__(self):
        """
        Деструктор, производит установку всех компонентов в начальное состояние
        :return: none
        """
        logging.debug("{0} destruction started".format(self))

        self.door_shifts.clear()
        self.room_led_shifts.clear()
        self.coolers_shifts.clear()
        self.blind_shifts.clear()

        del self.shift_reg  # FIXME: Consider deletion

        logging.debug("{0} destruction finished".format(self))
        return

    def __get_state(self):
        return self.shift_reg.get_buffer()

    def toggle_door(self, door_id):
        """
        Функция для переключения шторы в противоположное состояние
        :param door_id: идентификатор двери (строка либо число, выбери сам)
        :return: True - успешно, False - неуспешно
        """
        if type(door_id) != str:
            raise ValueError('Value must be a string literal')

        if door_id not in self.door_shifts:
            raise ValueError('id not found')

        door_data = self.door_shifts.get(door_id)

        door_data.toggle()

        return True

    def toggle_blind(self, blind_id):
        """
        Функция для переключения шторы в противоположное состояние
        :param blind_id: идентификатор шторки
        :return: True - успешно, False - неуспешно
        """
        if type(blind_id) != str:
            raise ValueError('Value must be a string literal')

        if blind_id not in self.blind_shifts:
            raise ValueError('id not found')

        blind_data = self.blind_shifts.get(blind_id)

        blind_data.toggle()

        return True

    def toggle_light(self, room_name):
        """
        Переключение света
        :param room_name: имя комнаты, строка
        :return: True - успешно, False - неуспешно
        """
        if type(room_name) != str:
            raise ValueError('room_name must be a string')

        elif room_name not in self.room_led_shifts:
            raise ValueError('unable to find the room with such name')

        led_data = self.room_led_shifts.get(room_name)

        led_data.toggle()

        return True

    def toggle_cooler(self, cooler_id):
        if type(cooler_id) != str:
            raise ValueError('Value must be a string literal')

        if cooler_id not in self.coolers_shifts:
            raise ValueError('Cooler name is not found')

        cooler_data = self.coolers_shifts.get(cooler_id)

        cooler_data.toggle()

        return True
