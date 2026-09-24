5.3: Platform Driver + miscdevice + GPIO из Device Tree
=======================================================

Описание
--------

Модуль ``hellokeys_rpi3_misc_dt.c`` демонстрирует создание платформенного драйвера с поддержкой:

- platform driver (``probe()`` / ``remove()``)
- устройства ``/dev/mydev`` через ``miscdevice``
- считывания состояния кнопок с GPIO, описанных в Device Tree
- чтения значений из user space через ``cat /dev/mydev``

Содержимое архива
-----------------

- ``hellokeys_rpi3_misc_dt.c`` — исходный код модуля
- ``Makefile`` — для сборки с помощью ``make``
- ``5_2_miscdevice_dt_gpio.pptx`` — презентация по работе
- ``5_2_miscdevice_dt_gpio.rst`` — эта документация

Требования
----------

- Raspberry Pi 3 с Linux kernel 5.x
- Device Tree с описанием ``gpios``
- Компилятор модуля ядра (``make``, ``linux-headers``)

Пример Device Tree
------------------

В файл ``.dts`` (например, ``bcm2710-rpi-3-b.dts``) нужно добавить:

.. code-block:: dts

   hellokeys@0 {
       compatible = "arrow,hellokeys";
       gpios = <&gpio 17 0>, <&gpio 27 0>;
       status = "okay";
   };

Работа с Device Tree (DTB и DTS)
================================

Преобразование .dtb → .dts
---------------------------

Если у вас есть скомпилированный файл Device Tree Blob (например, ``/boot/bcm2710-rpi-3-b.dtb``),
вы можете получить исходный ``.dts`` так:

.. code-block:: bash

   dtc -I dtb -O dts -o bcm2710-rpi-3-b.dts /boot/bcm2710-rpi-3-b.dtb

Редактируйте ``bcm2710-rpi-3-b.dts``, добавляя свой ``hellokeys@0 { ... }`` в нужное место.

Сборка обратно: .dts → .dtb
----------------------------

После редактирования соберите обратно:

.. code-block:: bash

   dtc -I dts -O dtb -o bcm2710-rpi-3-b.dtb bcm2710-rpi-3-b.dts

Затем скопируйте новый ``.dtb`` в ``/boot/`` на Raspberry Pi:

.. code-block:: bash

   sudo cp bcm2710-rpi-3-b.dtb /boot/
   sudo reboot

Проверка после загрузки
------------------------

Проверьте, что узел ``hellokeys`` виден в памяти устройства:

.. code-block:: bash

   ls /proc/device-tree/soc/hellokeys@0
   cat /proc/device-tree/soc/hellokeys@0/gpios
   hexdump /proc/device-tree/soc/hellokeys@0/compatible

Сборка и установка
------------------

.. code-block:: bash

   make
   sudo insmod hellokeys_rpi3_misc_dt.ko
   dmesg | grep hellokeys
   cat /dev/mydev

Пример вывода:

::

   key1: 0
   key2: 1

Удаление модуля:

.. code-block:: bash

   sudo rmmod hellokeys_rpi3_misc_dt

Лицензия
--------

GPL. Образовательное использование.  
Авторы: *Linux Driver Development Guide + ChatGPT*
