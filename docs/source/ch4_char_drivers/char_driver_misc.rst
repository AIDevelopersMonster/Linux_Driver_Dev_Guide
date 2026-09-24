===============================================
Раздел 4.3: Символьный драйвер через miscdevice
===============================================

В этом разделе мы реализуем символьный драйвер на базе интерфейса `miscdevice`, который
предоставляет простой способ регистрации устройства без ручного управления мажорными/минорными номерами
и создания классов (`class_create`, `device_create`).

Преимущества miscdevice
------------------------

* Автоматическая регистрация устройства с динамическим минорным номером
* Автоматическое создание файла /dev/<имя>
* Упрощённый интерфейс: достаточно одной структуры `miscdevice` и набора `file_operations`

Исходный код: misc_char_driver.c
---------------------------------

.. code-block:: c

    static struct file_operations fops = {
        .owner = THIS_MODULE,
        .read = dev_read,
        .write = dev_write,
    };

    static struct miscdevice garvis_misc_device = {
        .minor = MISC_DYNAMIC_MINOR,
        .name = "garvis_misc",
        .fops = &fops,
        .mode = 0666
    };

    static int __init garvis_misc_init(void) {
        return misc_register(&garvis_misc_device);
    }

    static void __exit garvis_misc_exit(void) {
        misc_deregister(&garvis_misc_device);
    }

    module_init(garvis_misc_init);
    module_exit(garvis_misc_exit);

Сборка и тестирование
----------------------

.. code-block:: bash

    $ make
    $ sudo insmod misc_char_driver.ko
    $ echo "Hello, Garvis" > /dev/garvis_misc
    $ cat /dev/garvis_misc
    $ sudo rmmod misc_char_driver

Вывод в dmesg
^^^^^^^^^^^^^

.. code-block:: text

    Garvis misc: device registered with /dev/garvis_misc
    Garvis misc: received 13 bytes: Hello, Garvis
    Garvis misc: device unregistered

Заключение
-----------

Интерфейс miscdevice идеально подходит для упрощённой разработки символьных драйверов, особенно в учебных или
небольших прикладных проектах. Он минимизирует код регистрации устройства и устраняет необходимость управлять классами и номерами вручную.
