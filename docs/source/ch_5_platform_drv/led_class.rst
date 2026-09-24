=========================
5.22: Linux LED Class
=========================

В этом разделе мы рассмотрим подсистему управления светодиодами в ядре Linux — **LED Class**, которая позволяет стандартизировано управлять светодиодами через `/sys/class/leds`.

---------------------------------
Что такое LED Class в Linux
---------------------------------

`LED class` — это часть подсистемы устройств в Linux, предназначенная для абстрагированного управления светодиодами.

Каждый светодиод, управляемый через эту подсистему, отображается в пользовательском пространстве как отдельный каталог:

.. code-block:: bash

    /sys/class/leds/<имя_led>/

--------------------------------------------
Примеры полей и файлов в каталоге светодиода
--------------------------------------------

.. code-block:: bash

    /sys/class/leds/led0/
    ├── brightness         # уровень яркости (0 или 255)
    ├── max_brightness     # максимальная яркость (обычно 255)
    ├── trigger            # триггер: cpu, timer, heartbeat и т.д.
    ├── delay_on           # таймер "включено", если триггер — "timer"
    ├── delay_off          # таймер "выключено"

------------------------------------
Преимущества использования LED Class
------------------------------------

 Унифицированный интерфейс `/sys/class/leds` 
 
 Возможность использования встроенных триггеров (cpu, disk, timer...)  

 Работа с `udev`, `systemd`, `udevadm`  

 Лёгкая интеграция с user space

--------------------------------------
Пример использования с системным LED
--------------------------------------

.. code-block:: bash

    echo none > /sys/class/leds/led0/trigger
    echo 1 > /sys/class/leds/led0/brightness

    echo timer > /sys/class/leds/led0/trigger
    echo 200 > /sys/class/leds/led0/delay_on
    echo 200 > /sys/class/leds/led0/delay_off

---------------------------------------------------
Как драйвер ядра может зарегистрировать LED device
---------------------------------------------------

Пример на уровне драйвера:

.. code-block:: c

    #include <linux/leds.h>

    static struct led_classdev my_led = {
        .name = "myred",
        .brightness = 0,
        .max_brightness = 1,
        .brightness_set = my_led_set,
    };

    static void my_led_set(struct led_classdev *led_cdev,
                           enum led_brightness brightness)
    {
        gpio_set_value(MY_LED_GPIO, brightness);
    }

    // Регистрация
    led_classdev_register(&pdev->dev, &my_led);

    // Удаление
    led_classdev_unregister(&my_led);

--------------------------------------------------------
Связь с Device Tree (пример для GPIO-контроллера)
--------------------------------------------------------

.. code-block:: dts

    ledred {
        compatible = "gpio-leds";
        pinctrl-names = "default";
        pinctrl-0 = <&pinctrl_ledred>;
        led-0 {
            label = "led0";
            gpios = <&gpio 17 GPIO_ACTIVE_HIGH>;
            default-state = "off";
        };
    };

-----------------------
Выводы
-----------------------

- LED Class позволяет управлять светодиодами через `/sys/class/leds`, не реализуя прямую работу с GPIO.
- Подходит для LED, привязанных к GPIO или к другим железным источникам (PMIC, контроллерам и т.п.).
- Хороший выбор, если нужен стандартный, расширяемый интерфейс с поддержкой триггеров.

---------------
Связанные темы:
---------------

- GPIO descriptor API
- Device Tree binding: `gpio-leds`
- Sysfs-интерфейс и управление оборудованием из user space
