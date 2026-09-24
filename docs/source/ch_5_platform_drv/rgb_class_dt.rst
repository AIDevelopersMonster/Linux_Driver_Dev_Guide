===============================================
5.25. Подключение RGB LED к LED class через DT
===============================================

Описание
========
В этой части проекта мы реализуем подключение RGB светодиода к встроенному механизм управления светодиодами в ядре Linux — **LED class**. Мы воспользуемся стандартным драйвером `gpio-leds`, который работает на основе описания в **Device Tree**. Каждая компонента RGB-светодиода будет зарегистрирована как отдельное `led_classdev`-устройство.

Структура Device Tree
---------------------
Ниже приведён фрагмент, который должен быть включён в `leds {}` внутри файла Device Tree:

.. code-block:: dts

    leds {
        compatible = "gpio-leds";
        phandle = <0x87>;

        ledred: ledred@0 {
            label = "ledred";
            gpios = <&gpio 16 0>;
            default-state = "off";
            linux,default-trigger = "none";
        };

        ledgreen: ledgreen@1 {
            label = "ledgreen";
            gpios = <&gpio 20 0>;
            default-state = "off";
            linux,default-trigger = "none";
        };

        ledblue: ledblue@2 {
            label = "ledblue";
            gpios = <&gpio 21 0>;
            default-state = "off";
            linux,default-trigger = "none";
        };
    };

Функциональные требования
-------------------------
- [x] **Регистрация каждого узла в LED class** — автоматически создаётся `/sys/class/leds/ledred`, `ledgreen`, `ledblue`
- [x] **Имя устройства через DT** — задаётся через `label = "..."`, и отображается в `sysfs`
- [x] **Поддержка атрибутов**:
    - `brightness` — установка 0 (выкл) / 255 (вкл)
    - `trigger` — переключение между `none`, `heartbeat`, `timer`, `cpu`, и др.
- [x] **default-state = "on"/"off"** из DT — влияет на стартовое поведение после загрузки
- [x] **GPIOD API** — драйвер использует `devm_gpiod_get()`, а не `legacy` GPIO API
- [x] **Работа без user-приложений** — управление полностью через `/sys/class/leds/*`
- [x] **Корректная выгрузка и освобождение ресурсов** (если используется custom-драйвер)
- [ ] *heartbeat-rgb trigger* — не реализован (пожелание, можно разработать отдельно)

Проверка
--------

1. Проверить `sysfs` после загрузки DT:

.. code-block:: bash

    ls /sys/class/leds/
    # → ledred  ledgreen  ledblue

2. Проверить работу триггеров:

.. code-block:: bash

    cat /sys/class/leds/ledred/trigger
    echo timer | sudo tee /sys/class/leds/ledred/trigger
    echo none | sudo tee /sys/class/leds/ledred/trigger

3. Проверить включение/выключение вручную:

.. code-block:: bash

    echo 1 | sudo tee /sys/class/leds/ledred/brightness
    echo 0 | sudo tee /sys/class/leds/ledred/brightness

4. Проверить статус:

.. code-block:: bash

    cat /sys/class/leds/ledred/brightness
    cat /sys/class/leds/ledred/trigger

5. Проверить, какие GPIO задействованы:

.. code-block:: bash

    gpioinfo | grep led
    raspi-gpio get 16
    raspi-gpio get 20
    raspi-gpio get 21

Заключение
----------
Мы успешно выполнили **включение RGB светодиода в LED class Linux** только с помощью **Device Tree**, без написания кода драйвера. Это позволяет полностью пользоваться встроенными возможностями ядра: управление яркостью, триггерами и автоматическое создание интерфейса `/sys/class/leds`.

Следующим шагом может быть создание пользовательского триггера `heartbeat-rgb` через kernel module.

