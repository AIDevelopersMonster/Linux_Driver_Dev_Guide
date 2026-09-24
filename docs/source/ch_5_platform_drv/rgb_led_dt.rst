5.20: RGB LED через Device Tree и MMIO
=======================================


Описание проекта
-----------------

В этом упражнении мы реализовали драйвер для управления RGB-светодиодами на Raspberry Pi 3 с использованием:

- Регистров MMIO (Memory-Mapped I/O)
- Описания устройств в Device Tree (DT)
- Создания трёх символических устройств `/dev/ledred`, `/dev/ledgreen`, `/dev/ledblue`
- Работа через фреймворк `miscdevice`
- Управление пинами напрямую через регистры (FSEL, SET, CLR)

Мы не использовали GPIO API (gpiod), а напрямую управляли GPIO на низком уровне через регистры SoC.


Физические соединения
---------------------

RGB LED подключён к пинам:

- R → GPIO16 (BCM)
- G → GPIO20
- B → GPIO21

Все пины конфигурируются как `output` в `probe()` функции.


Код драйвера
-------------

1. В `probe()` мы:

- читаем из DT:
  - метку устройства `label`
  - битовую маску `led-mask` — например, `1 << 16` (0x00010000) для GPIO16
- вызываем `ioremap()` для диапазона регистров GPIO (`0x3F200000`, 0xB4)
- конфигурируем FSEL регистр через `set_gpio_output(gpio)`
- регистрируем `miscdevice`

2. При `write()` в `/dev/ledred`:

- строка `'1'` вызывает `iowrite32(mask, gpio_base + GPIO_SET_OFFSET)`
- строка `'0'` вызывает `iowrite32(mask, gpio_base + GPIO_CLR_OFFSET)`

3. При `read()` возвращается текущий символ: `'1'` или `'0'`.


Device Tree (DT)
----------------

Пример узла для одного светодиода (вставляется в `soc {}`):

.. code-block:: dts

    ledred@3 {
        compatible = "kontakts,rgb-led";
        label = "ledred";
        reg = <3>;
        status = "okay";
        led-mask = <0x10000>; // GPIO16
    };

Устройства создаются на основании `compatible` и `label`, `led-mask` определяет нужный пин.


Проверка DT
-----------

.. code-block:: bash

    ls /proc/device-tree/soc/ledred@3
    cat /proc/device-tree/soc/ledred@3/label
    hexdump -C /proc/device-tree/soc/ledred@3/led-mask


Проверка драйвера
-----------------

Загрузка:

.. code-block:: bash

    sudo insmod rgb_led_dt.ko

Проверка устройств:

.. code-block:: bash

    ls -l /dev/ledred /dev/ledgreen /dev/ledblue

Включение и чтение:

.. code-block:: bash

    echo "1" > /dev/ledred
    cat /dev/ledred


Проверка GPIO через gpioinfo и raspi-gpio
-----------------------------------------

.. code-block:: bash

    gpioinfo | grep 16
    gpioinfo | grep 20
    gpioinfo | grep 21

Вывод:

::

    line  16: unnamed unused output active-high
    line  20: unnamed unused output active-high
    line  21: unnamed unused output active-high

Или:

.. code-block:: bash

    sudo raspi-gpio get 16
    sudo raspi-gpio get 20
    sudo raspi-gpio get 21

Результат:

::

    GPIO 16: level=1 fsel=1 func=OUTPUT


Финальный вывод
----------------

- Мы создали полноценный low-level RGB LED драйвер
- Использовали MMIO напрямую
- Применили Device Tree с масками пинов
- Проверили работу через `/dev/*`, `gpioinfo` и `raspi-gpio`
- Освободили пины, используя `set_gpio_output()`


Лицензия
--------

GPL. Для обучения. Автор: ChatGPT + пользователь.
