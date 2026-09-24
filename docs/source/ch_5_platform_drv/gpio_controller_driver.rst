
5.8. GPIO Controller Driver
===========================

Введение
--------

В этом разделе мы рассмотрим создание и назначение **GPIO-контроллеров** в рамках ядра Linux.  
В отличие от простого использования GPIO в драйверах устройств, GPIO-контроллеры — это специальные платформенные драйверы,  
которые предоставляют доступ к множеству линий ввода-вывода и регистрируются в подсистеме GPIO ядра.

Такие драйверы, как `gpio-bcm2835.c`, позволяют использовать API GPIO для других устройств, в том числе через pinctrl.

Роль GPIO контроллера
----------------------

GPIO контроллер:

- управляет множеством GPIO линий;
- предоставляет функции: `gpio_get_value()`, `gpio_direction_input()`, `gpio_direction_output()`, `gpio_set_value()` и т.д.;
- может взаимодействовать с pinctrl и IRQ подсистемами;
- регистрируется как gpiochip в `/sys/class/gpio/` или через pin descriptor API.

Связь с Device Tree
--------------------

GPIO контроллер должен быть описан в DT. Пример:

.. code-block:: dts

    gpio: gpio@7e200000 {
        compatible = "brcm,bcm2835-gpio";
        reg = <0x7e200000 0x100>;
        gpio-controller;
        #gpio-cells = <2>;
    };

Пояснение:

- `gpio:` — label, на который ссылаются другие узлы (`&gpio`);
- `compatible` — привязка к драйверу (например, `gpio-bcm2835.c`);
- `gpio-controller` — признак контроллера;
- `#gpio-cells = <2>` — означает, что для каждого GPIO потребуется 2 аргумента: номер и флаги.

Регистрация драйвера
----------------------

Типичный драйвер GPIO реализует интерфейс `struct gpio_chip` и регистрирует его через `gpiochip_add_data()`:

.. code-block:: c

    static struct gpio_chip mychip = {
        .label = "mygpio",
        .get = my_gpio_get,
        .set = my_gpio_set,
        .direction_input = my_gpio_dir_in,
        .direction_output = my_gpio_dir_out,
        .base = -1,
        .ngpio = 8,
        .owner = THIS_MODULE,
    };

    gpiochip_add_data(&mychip, NULL);

После регистрации:

- пины становятся доступны для pinctrl и платформенных устройств;
- можно использовать `devm_gpiod_get()` в драйверах для запроса нужных пинов по label.

Вывод
-----

Драйверы GPIO контроллеров — это фундаментальная часть Linux GPIO подсистемы.  
Они позволяют управлять наборами пинов и предоставляют интерфейс для других драйверов.  
На Raspberry Pi эту роль выполняет `gpio-bcm2835.c`, взаимодействующий с pinctrl, irq и другими слоями.
