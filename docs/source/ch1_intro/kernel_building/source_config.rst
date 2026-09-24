Получение исходников и базовая конфигурация
===========================================

1. Клонируйте официальный репозиторий Raspberry Pi:
::

    git clone --depth=1 https://github.com/raspberrypi/linux
    cd linux

2. Загрузите конфигурацию:
::

    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcmrpi_defconfig

Выбор конфигурации:
--------------------

- `bcmrpi_defconfig`  Raspberry Pi 1
- `bcm2709_defconfig`  Raspberry Pi 2/3
- `bcm2711_defconfig`  Raspberry Pi 4

Настройка:
::

    make menuconfig
