##############################################################################################
# FIXME List:
# CC21 - Consider Change 21
#   Возможно, настройка формата логгера прямо в __init__ - не лучшая идея
##############################################################################################

# Установка Handler'а и формата по умолчанию для всех сообщений логгера
# Подробнее: https://docs.python.org/3/library/logging.html#logging.basicConfig
import logging
logging.basicConfig()

# Сохранение информации о версии платформы
VERSION = "v0.4-dev.1"
