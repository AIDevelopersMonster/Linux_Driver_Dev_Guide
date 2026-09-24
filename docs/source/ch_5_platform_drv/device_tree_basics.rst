5.11. GPIOs in the Device Tree
==============================

Введение
--------

GPIO-пины в Linux не задаются напрямую в коде драйвера — вместо этого они описываются в Device Tree (DT).  
Это позволяет отделить описание "железа" от логики драйвера и адаптировать драйвер под разные платформы.

В этом разделе мы рассмотрим, как описываются GPIO в `.dts` файлах, как связать их с драйвером и как использовать имена (`gpio-names`) и флаги (`active-low`, `bias-disable`, `output-high` и т.п.).

Пример с кнопками (`hellokeys`)
-------------------------------

.. code-block:: dts

    hellokeys@0 {
        compatible = "arrow,hellokeys";
        gpios = <&gpio 17 0>, <&gpio 27 0>;
        gpio-names = "key1", "key2";
        status = "okay";
    };

Здесь:
- `gpios` — массив GPIO-ссылок: `<контроллер пинов> <номер пина> <флаги>`
- `gpio-names` — логические имена, по которым драйвер будет обращаться к каждому пину
- `<&gpio 17 0>` = GPIO №17, input, без флагов (0)
- `status = "okay"` — активирует узел

Пример драйвера с использованием `devm_gpiod_get()`:

.. code-block:: c

    key1 = devm_gpiod_get(&pdev->dev, "key1", GPIOD_IN);
    val = gpiod_get_value(key1);

---

План для RGB LED устройства
----------------------------

Следующий шаг — это подключение RGB LED на три GPIO пина. В `.dts` описание может выглядеть так:

.. code-block:: dts

    led_rgb@0 {
        compatible = "kontakts,rgb-led";
        gpios = <&gpio 20 0>, <&gpio 21 0>, <&gpio 22 0>;
        gpio-names = "led_r", "led_g", "led_b";
        status = "okay";
    };

Это создаёт логическую привязку:

- `led_r` → GPIO 20
- `led_g` → GPIO 21
- `led_b` → GPIO 22

Флаг `0` обозначает, что пины по умолчанию работают в активном высоком уровне (active-high).

---

Флаги GPIO
----------

В третьем аргументе каждой записи `<&gpio X F>` задаются флаги конфигурации:

- `0` — default (active-high input)
- `1` — active-low (инвертированная логика)
- `2` — output (значение зависит от ядра, часто используется с GPIOD_OUT_LOW / HIGH)
- `4` — bias-disable (отключение подтяжек)

Примеры более полной записи:

.. code-block:: dts

    <&gpio 17 GPIO_ACTIVE_LOW>
    <&gpio 18 GPIO_ACTIVE_HIGH>
    <&gpio 19 (GPIO_ACTIVE_HIGH | GPIO_PULL_DOWN)>

Флаги описываются в `include/dt-bindings/gpio/gpio.h`

---

Где и как искать узлы GPIO в Linux
-----------------------------------

После загрузки системы вы можете просмотреть подключённые устройства и их GPIO:

.. code-block:: bash

    ls /proc/device-tree/soc/
    cat /proc/device-tree/soc/led_rgb@0/gpios
    hexdump -C /proc/device-tree/soc/hellokeys@0/gpios

---

Вывод
-----

Работа с GPIO через Device Tree — это основа переносимости драйверов под Linux.  
Поддержка `gpios`, `gpio-names`, `interrupts` и других свойств позволяет адаптировать один и тот же драйвер к множеству аппаратных конфигураций, изменяя только `.dts`.

В следующих разделах мы продолжим использование GPIO в контексте RGB LED и других устройств, опираясь на этот подход.

