5.15. Управление GPIO с помощью GPIOD API
=========================================

Описание
--------

В этом разделе мы переработали драйвер `gpiotoggle` для Raspberry Pi 3, чтобы использовать **современный GPIOD API** вместо устаревших `gpio_request()`, `gpio_set_value()` и `gpio_get_value()`.

Это важный шаг для совместимости с новыми ядрами и поддержки расширенного оборудования, такого как GPIO-экспандеры и виртуальные GPIO.

---

Цель
----

Создать `platform driver`, который:

- получает номер GPIO из Device Tree;
- настраивает его как выход;
- предоставляет интерфейс через `/dev/gpiotoggle`:
  
  + `echo 1 > /dev/gpiotoggle` — включить
  + `echo 0 > /dev/gpiotoggle` — выключить
  + `cat /dev/gpiotoggle` — вывести текущее состояние пина

---

Подключение и освобождение GPIO
-------------------------------

В предыдущих версиях мы использовали `GPIO21` как вывод RGB светодиода.

Теперь мы **перенесли `gpiotoggle` на GPIO26**, а `GPIO21` стал **свободен** — мы сможем использовать его для синего канала RGB LED в следующих разделах (см. `5.18`).

Это стало возможным, потому что GPIOD корректно освобождает ресурсы, используя `devm_gpiod_get()` и автоматически управляется ядром.

---

Пример Device Tree (фрагмент)
-----------------------------

.. code-block:: dts

    gpiotoggle@1 {
        compatible = "kontakts,gpiotoggle";
        reg = <1>;
        gpios = <&gpio 26 0>;
        status = "okay";
    };

---

Проверка работы драйвера
------------------------

1. Компиляция и загрузка:

.. code-block:: bash

    make
    sudo insmod gpiotoggle.ko

2. Проверка в `gpioinfo`:

.. code-block:: bash

    gpioinfo | grep 26

    # должен показать:
    # line 26: unnamed "gpiotoggle" output active-high [used]

3. Управление:

.. code-block:: bash

    echo 1 > /dev/gpiotoggle
    echo 0 > /dev/gpiotoggle
    cat /dev/gpiotoggle

    # Вывод:
    # GPIO is 1
    # или
    # GPIO is 0

4. Выгрузка:

.. code-block:: bash

    sudo rmmod gpiotoggle

---

Обновление Device Tree
----------------------

После редактирования `.dts` (например, добавления узла ``gpiotoggle@1``) нужно перекомпилировать его и заменить используемый `.dtb`.

1. Убедитесь, что у вас установлен Device Tree Compiler (`dtc`):

.. code-block:: bash

    sudo apt update
    sudo apt install device-tree-compiler

2. Перейдите в директорию, где находится `bcm2710-rpi-3-b.dts`, и скомпилируйте его в `.dtb`:

.. code-block:: bash

    dtc -I dts -O dtb -o bcm2710-rpi-3-b.dtb bcm2710-rpi-3-b.dts

3. Сделайте резервную копию оригинального `.dtb`, затем скопируйте новый в `/boot/`:

.. code-block:: bash

    sudo cp /boot/bcm2710-rpi-3-b.dtb /boot/bcm2710-rpi-3-b.dtb.bak
    sudo cp bcm2710-rpi-3-b.dtb /boot/

4. Перезагрузите Raspberry Pi, чтобы применить обновлённый DTB:

.. code-block:: bash

    sudo reboot

5. После загрузки проверьте, что узел появился в дереве устройств:

.. code-block:: bash

    ls /proc/device-tree/soc/gpiotoggle@1
    cat /proc/device-tree/soc/gpiotoggle@1/gpios
    
---

Преимущества GPIOD
------------------

- Совместим с будущими ядрами Linux
- Позволяет обращаться к GPIO по имени, индексу или в массиве
- Автоматическое освобождение через `devm_` API
- Работа с GPIO-экспандерами и нестандартными контроллерами
- Совместимость с `Device Tree` через `gpios = <...>;`

---

Вывод
-----

Мы перешли на GPIOD API и освободили GPIO21, который будет использоваться для RGB-светодиода.  
Это пример чистой архитектуры, основанной на платформенном драйвере и `miscdevice`.

Следующим шагом мы реализуем **RGB LED driver** с тремя GPIO (R/G/B), используя GPIOD и Device Tree.
