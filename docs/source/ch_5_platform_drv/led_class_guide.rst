
LED Class в Linux
=================

Подсистема LED Class (`/sys/class/leds/`) — часть ядра Linux, предназначенная для абстрагированной работы с аппаратными светодиодами. Она позволяет управлять ими через userspace без обращения к конкретным регистрам или GPIO напрямую.

Общие сведения
--------------

Каждое LED-устройство отображается в виде каталога:

::

  /sys/class/leds/<имя_led>/

Примеры возможных имён:

- ``led0`` — индикатор активности/питания
- ``mmc0`` — активность SD-карты
- ``ledred`` — пользовательский RGB-светодиод

Основные файлы в каталоге:
^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``brightness`` — текущая яркость (0 = выкл, 1 или 255 = вкл)
- ``max_brightness`` — максимальное значение (обычно 1 или 255)
- ``trigger`` — список доступных триггеров (поведение: таймер, heartbeat и др.)
- ``uevent`` — информация о регистрации устройства
- ``device/`` — ссылка на физическое устройство

Примеры использования
---------------------

1. Включить светодиод:

::

  echo 1 | sudo tee /sys/class/leds/led0/brightness

2. Выключить светодиод:

::

  echo 0 | sudo tee /sys/class/leds/led0/brightness

3. Проверить доступные триггеры:

::

  cat /sys/class/leds/led0/trigger

4. Назначить светодиоду триггер:

::

  echo timer | sudo tee /sys/class/leds/led0/trigger

5. Управление частотой мигания при триггере ``timer``:

::

  echo 100 | sudo tee /sys/class/leds/led0/delay_on
  echo 100 | sudo tee /sys/class/leds/led0/delay_off

Пример: Управление встроенным светодиодом Raspberry Pi
------------------------------------------------------

На Raspberry Pi `led0` обычно отвечает за активность SD-карты (мигает при чтении/записи). Однако вы можете взять над ним полный контроль:

Сброс автоматического управления (trigger):

.. code-block:: bash

    echo none | sudo tee /sys/class/leds/led0/trigger

Ручное управление включением/выключением:

.. code-block:: bash

    echo 0   | sudo tee /sys/class/leds/led0/brightness
    echo 255 | sudo tee /sys/class/leds/led0/brightness

Проверка текущего состояния:

.. code-block:: bash

    cat /sys/class/leds/led0/trigger
    cat /sys/class/leds/led0/brightness

Возврат поведения по умолчанию (триггер ``mmc0``):

.. code-block:: bash

    echo mmc0 | sudo tee /sys/class/leds/led0/trigger

Программная регистрация LED из драйвера
---------------------------------------

Минимальный пример регистрации светодиода из драйвера:

.. code-block:: c

  #include <linux/leds.h>

  static struct led_classdev my_led = {
      .name = "myled",
      .brightness_set = my_set_brightness,
  };

  static void my_set_brightness(struct led_classdev *led_cdev,
                                enum led_brightness brightness)
  {
      // Ваша логика включения/выключения светодиода
  }

  // Регистрация
  led_classdev_register(dev, &my_led);

  // Отмена регистрации
  led_classdev_unregister(&my_led);

Работа с LED class в Device Tree
--------------------------------

Если светодиод описан в Device Tree, используется драйвер ``gpio-leds``:

.. code-block:: dts

  leds {
      compatible = "gpio-leds";

      ledred {
          label = "ledred";
          gpios = <&gpio 16 GPIO_ACTIVE_HIGH>;
          default-state = "off";
      };
  };

Дополнительно можно указать свойства:

- ``linux,default-trigger = "heartbeat";``
- ``default-state = "on"`` / ``"off"`` / ``"keep"``
- ``retain-state-suspended;``

Вывод информации о LED
-----------------------

.. code-block:: bash

  udevadm info -a -p /sys/class/leds/led0
  cat /sys/class/leds/led0/uevent

Полезные утилиты
----------------

- ``ls /sys/class/leds/`` — список светодиодов
- ``gpioinfo`` — покажет, какие GPIO привязаны к светодиодам (если через gpio-leds)
- ``udevadm info`` — подробности о регистрации устройства
- ``dmesg | grep led`` — сообщения ядра о подсистеме LED

Советы
------

- Значения в ``brightness`` и ``trigger`` можно управлять из скриптов и systemd-юнитов.
- Можно использовать LED class в комбинации с input-подсистемой (например, для индикации Caps Lock).
- Поддержка LED class определяется опцией ядра ``CONFIG_LEDS_CLASS``.

Дополнительные ресурсы
-----------------------

- https://www.kernel.org/doc/html/latest/leds/index.html
- https://www.kernel.org/doc/Documentation/devicetree/bindings/leds/leds-gpio.yaml
