Загрузка модулей ядра: /etc/modules и modules-load.d
====================================================

Автозагрузка модулей ядра:

- `/etc/modules`  список имён модулей
- `/etc/modules-load.d/*.conf`  конфиги для systemd

Пример:
::

    i2c-dev
    spi-dev

Параметры:
::

    options i2c_bcm2708 baudrate=400000  # в modprobe.d
