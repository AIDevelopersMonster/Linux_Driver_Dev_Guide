======================================================
5.2: Создание своего platform_device (hellokeys_rpi3)
======================================================

В этом лабораторном задании вы создадите собственное платформенное устройство и соответствующий драйвер для Raspberry Pi 3. Этот модуль будет использовать GPIO-контакты для чтения состояний кнопок или других цифровых входов. Отличие от предыдущих драйверов — использование **platform driver API** и регистрация устройства и драйвера вручную (без Device Tree).

Цели:
- Зарегистрировать platform_device и platform_driver;
- Использовать GPIO API (gpio_request, gpio_direction_input, gpio_get_value);
- Выводить диагностику через `dev_info()` и `dmesg`;
- Работать с простыми входами: кнопки, герконы, GPIO-ключи.

---

1. Подключение заголовков
--------------------------

Для начала необходимо подключить заголовочные файлы для работы с platform driver и GPIO API:

.. code-block:: c

    #include <linux/platform_device.h>
    #include <linux/gpio.h>
    #include <linux/init.h>
    #include <linux/module.h>
    #include <linux/kernel.h>

---

2. Описание устройства (platform_device)
----------------------------------------

Создаём структуру фиктивного устройства и регистрируем его вручную:

.. code-block:: c

    static struct platform_device hellokeys_device = {
        .name = "hellokeys",
        .id = -1,
    };

    static int __init hellokeys_init_device(void)
    {
        return platform_device_register(&hellokeys_device);
    }

    static void __exit hellokeys_exit_device(void)
    {
        platform_device_unregister(&hellokeys_device);
    }

    module_init(hellokeys_init_device);
    module_exit(hellokeys_exit_device);

---

3. Реализация драйвера (platform_driver)
----------------------------------------

Теперь создаём платформенный драйвер, который привязывается к устройству по имени.

.. code-block:: c

    struct gpio_desc {
        unsigned gpio;
        const char *label;
    };

    static struct gpio_desc my_keys[] = {
        { 17, "key1" },
        { 27, "key2" },
    };

    static int hellokeys_probe(struct platform_device *pdev)
    {
        int i;
        dev_info(&pdev->dev, "hellokeys_probe called\n");

        for (i = 0; i < ARRAY_SIZE(my_keys); i++) {
            gpio_request(my_keys[i].gpio, my_keys[i].label);
            gpio_direction_input(my_keys[i].gpio);
        }

        return 0;
    }

    static int hellokeys_remove(struct platform_device *pdev)
    {
        int i;
        for (i = 0; i < ARRAY_SIZE(my_keys); i++) {
            gpio_free(my_keys[i].gpio);
        }
        dev_info(&pdev->dev, "hellokeys removed\n");
        return 0;
    }

    static struct platform_driver hellokeys_driver = {
        .probe = hellokeys_probe,
        .remove = hellokeys_remove,
        .driver = {
            .name = "hellokeys",
        },
    };

    module_platform_driver(hellokeys_driver);

---

4. Сборка и установка модуля
----------------------------

Добавьте файл `hellokeys_rpi3.c` в папку `~/linux_rpi3_drivers/` и добавьте его в Makefile:

.. code-block:: make

    obj-m += hellokeys_rpi3.o

Затем соберите модуль:

.. code-block:: bash

    make -C /lib/modules/$(uname -r)/build M=$PWD modules

Установите и проверьте:

.. code-block:: bash

    sudo insmod hellokeys_rpi3.ko
    dmesg | grep hellokeys

---

5. Проверка состояния GPIO-кнопок
---------------------------------

Напишите короткую утилиту или проверьте состояние через `gpio_get_value()` внутри `probe()` или через `timer`/`workqueue` по желанию.

---

6. Подключение физических кнопок
---------------------------------

Вы можете использовать:
- Модуль на 5 кнопок (5-key input module);
- Reed switch (геркон);
- 4x4 keypad (одиночные линии);
- IO Keypad board.

Подключите кнопки к GPIO 17 и 27 на Raspberry Pi 3.

---

7. Итоги и следующий шаг
------------------------

Вы создали ручной platform_device и platform_driver, зарегистрировали GPIO-контакты и реализовали считывание входов. В следующем разделе (5.3) мы покажем демонстрацию этого модуля с реальными нажатиями кнопок.
