5.6: Работа с GPIO и подсистемой pin control
=============================================

Цель
----

Разобраться, как ядро Linux взаимодействует с GPIO и подсистемой управления пинами (pin control), как использовать эти возможности в драйверах и описывать поведение пинов в Device Tree.

GPIO API в ядре
----------------

Для взаимодействия с GPIO до GPIO descriptor API использовались следующие функции:

.. code-block:: c

   int gpio_request(unsigned gpio, const char *label);
   int gpio_direction_input(unsigned gpio);
   int gpio_direction_output(unsigned gpio, int value);
   int gpio_get_value(unsigned gpio);
   void gpio_set_value(unsigned gpio, int value);
   void gpio_free(unsigned gpio);

Они по-прежнему доступны, но для новых драйверов предпочтителен `gpiod_*` API (descriptor-based GPIO).

Pin controller (pinctrl)
--------------------------

Pin controller (или pinmux/pinctrl) отвечает за:

- выбор функции пина (GPIO, I2C, UART, SPI, PWM...),
- управление подтяжкой (pull-up/pull-down),
- направление (in/out),
- активацию альтернативных функций.

Подсистема pinctrl может быть описана в Device Tree или вручную назначена драйвером.

Device Tree: pinmux и pinctrl
------------------------------

Пример назначения пинов через DT:

.. code-block:: dts

   my_device {
       compatible = "vendor,mydev";
       pinctrl-names = "default";
       pinctrl-0 = <&mydev_pins>;

       // другие свойства
   };

   mydev_pins: mydev_pins {
       pins = "gpio17", "gpio27";
       function = "input";
       bias-pull-up;
   };

Таким образом:

- `pinctrl-names = "default"` — активный режим по умолчанию;
- `pinctrl-0 = <...>` — ссылка на node с описанием режима;
- `function` — режим работы пинов;
- `bias-pull-up/down` — подтяжка.

Пример: GPIO-устройство (драйвер)
----------------------------------

В модуле можно использовать:

.. code-block:: c

   int gpio = of_get_named_gpio(dev->of_node, "gpios", 0);
   gpio_request(gpio, "mydev");
   gpio_direction_input(gpio);
   int val = gpio_get_value(gpio);

Или с использованием дескрипторов:

.. code-block:: c

   struct gpio_desc *desc;
   desc = devm_gpiod_get(dev, "input", GPIOD_IN);
   int val = gpiod_get_value(desc);

Интерфейс /sys/class/gpio
--------------------------

Это legacy-интерфейс, который позволяет экспортировать GPIO в userspace:

.. code-block:: bash

   echo 17 > /sys/class/gpio/export
   echo in > /sys/class/gpio/gpio17/direction
   cat /sys/class/gpio/gpio17/value

Хотя он работает, **в новых драйверах предпочтительно не использовать его напрямую**.

Итог
----

+-----------------+--------------------------------------------+
| Слой            | Назначение                                 |
+=================+============================================+
| Device Tree     | описание пинов, функций, режимов           |
+-----------------+--------------------------------------------+
| pinctrl         | выбор функции пина (alt, in, out, pull)    |
+-----------------+--------------------------------------------+
| GPIO API        | работа с состоянием пина (1/0)             |
+-----------------+--------------------------------------------+
| Драйвер (C)     | чтение/запись значений, регистрация        |
+-----------------+--------------------------------------------+
| Userspace       | доступ через /dev/ или sysfs (устаревший)  |
+-----------------+--------------------------------------------+



Следующий шаг — создать демонстрационный модуль `gpio_toggle` с управлением пином из `/dev/mydev` + описание DT.
