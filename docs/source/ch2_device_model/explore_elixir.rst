.. _explore_elixir:

Изучение исходников Linux через Elixir
=======================================

Одним из самых мощных инструментов для работы с исходным кодом ядра Linux является Elixir:

`https://elixir.bootlin.com <https://elixir.bootlin.com>`_

Он позволяет:

- Исследовать структуру дерева исходников ядра Linux
- Быстро находить нужные функции, структуры, интерфейсы
- Переходить по коду с гиперссылками
- Смотреть изменения между версиями

Примеры:

- Все драйверы SPI:
  https://elixir.bootlin.com/linux/latest/source/drivers/spi

- Структура и регистрация платформенных драйверов:
  https://elixir.bootlin.com/linux/latest/source/include/linux/platform_device.h

- Список всех драйверов шин:
  https://elixir.bootlin.com/linux/latest/source/drivers/bus

Мы будем использовать Elixir на протяжении всей главы, чтобы изучать готовые драйверы и структуру системы устройств и шин в Linux.
