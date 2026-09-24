Включение интерфейсов: I2C, SPI, UART
=====================================

Чтобы использовать периферию и подключать устройства, необходимо включить соответствующие интерфейсы.

Через raspi-config:
--------------------

::

    sudo raspi-config

- Интерфейс  Enable I2C
- Интерфейс  Enable SPI
- Интерфейс  Enable Serial (UART)

Через config.txt:
------------------

Файл `/boot/config.txt`, строки:

::

    dtparam=i2c_arm=on
    dtparam=spi=on
    enable_uart=1

Проверка:
---------

- I2C: `ls /dev/i2c-1`, `i2cdetect -y 1`
- SPI: `ls /dev/spidev0.0`
- UART: `dmesg | grep ttyAMA`

После включения желательно перезагрузить:
::

    sudo reboot
