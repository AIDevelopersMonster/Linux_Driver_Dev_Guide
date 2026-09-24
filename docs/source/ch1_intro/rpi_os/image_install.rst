Установка Raspberry Pi OS
=========================

Для подготовки Raspberry Pi к разработке драйверов потребуется официальная ОС Raspberry Pi OS (или Raspberry Pi Lite для минимальной системы).

Шаги установки:
---------------

1. Скачайте образ с сайта: https://www.raspberrypi.com/software/operating-systems/

2. Запишите образ на SD-карту с помощью Raspberry Pi Imager или ``dd`` в Linux:

   .. code-block:: bash

      sudo dd if=2025-05-raspios.img of=/dev/sdX bs=4M status=progress conv=fsync

3. Подключите SD-карту к Raspberry Pi и запустите.

Дополнительно:
--------------

- Для headless запуска: создайте пустой файл ``ssh`` на boot-разделе.
- Для Wi-Fi: создайте ``wpa_supplicant.conf`` на boot-разделе.
