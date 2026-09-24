.. SPDX-License-Identifier: GPL-2.0
.. char_driver_simple:


=============================================================
Простейший символьный драйвер Linux (без создания /dev-файла)
=============================================================

Этот пример показывает, как создать и зарегистрировать **символьный драйвер** в ядре Linux **без использования** `class_create()` и **без создания устройства в /dev**. Модуль просто демонстрирует базовые функции `open`, `read`, `write`, `release` и взаимодействие через `dmesg`.

Автор: **Garvis** (aka ChatGPT)

Описание
~~~~~~~~

- Используется `register_chrdev()` для регистрации устройства.
- Файл устройства не создаётся.
- Все вызовы логируются в `dmesg`.
- Возврат значений реализован как заглушка (ничего не читается и не пишется по факту).

Исходный код
~~~~~~~~~~~~

.. code-block:: c

    // SPDX-License-Identifier: GPL-2.0
    // char_driver_simple.c — Простейший символьный драйвер без /dev файла

    #include <linux/module.h>    // Для всех модулей ядра
    #include <linux/fs.h>        // Для file_operations
    #include <linux/uaccess.h>   // Для доступа к пользовательскому пространству

    #define DEVICE_NAME "garvis_simple"  // Имя устройства
    static int major;                    // Major-номер, выделяется динамически

    // Функция вызывается при открытии устройства
    static int dev_open(struct inode *inode, struct file *file)
    {
        pr_info("garvis_simple: Устройство открыто\n");
        return 0;
    }

    // Функция вызывается при чтении
    static ssize_t dev_read(struct file *file, char __user *buf, size_t len, loff_t *offset)
    {
        pr_info("garvis_simple: Запрошено чтение (заглушка)\n");
        return 0;  // Не читаем данные
    }

    // Функция вызывается при записи
    static ssize_t dev_write(struct file *file, const char __user *buf, size_t len, loff_t *offset)
    {
        pr_info("garvis_simple: Запрошена запись %zu байт (заглушка)\n", len);
        return len;  // Проглатываем данные
    }

    // Функция вызывается при закрытии устройства
    static int dev_release(struct inode *inode, struct file *file)
    {
        pr_info("garvis_simple: Устройство закрыто\n");
        return 0;
    }

    // Структура операций устройства
    static struct file_operations fops = {
        .owner = THIS_MODULE,
        .open = dev_open,
        .read = dev_read,
        .write = dev_write,
        .release = dev_release,
    };

    // Функция инициализации модуля
    static int __init char_driver_simple_init(void)
    {
        major = register_chrdev(0, DEVICE_NAME, &fops);  // 0 → динамический major
        if (major < 0) {
            pr_alert("garvis_simple: Ошибка регистрации устройства\n");
            return major;
        }
        pr_info("garvis_simple: Зарегистрировано с major номером %d\n", major);
        return 0;
    }

    // Функция выгрузки модуля
    static void __exit char_driver_simple_exit(void)
    {
        unregister_chrdev(major, DEVICE_NAME);
        pr_info("garvis_simple: Драйвер выгружен\n");
    }

    module_init(char_driver_simple_init);
    module_exit(char_driver_simple_exit);

    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("Garvis");
    MODULE_DESCRIPTION("Простой символьный драйвер без class_create");

Компиляция и загрузка
~~~~~~~~~~~~~~~~~~~~~

Создайте отдельный `Makefile` (например, `Makefile_ge03`):

.. code-block:: make

    obj-m := char_driver_simple.o

    all:
        make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

    clean:
        make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

Загрузите модуль:

.. code-block:: bash

    make -f Makefile_ge03
    sudo insmod char_driver_simple.ko
    dmesg | tail
    sudo rmmod char_driver_simple

Вывод будет примерно таким:

.. code-block:: text

    [....] garvis_simple: Зарегистрировано с major номером 240
    [....] garvis_simple: Устройство открыто
    [....] garvis_simple: Запрошена запись 12 байт (заглушка)
    [....] garvis_simple: Устройство закрыто
    [....] garvis_simple: Драйвер выгружен

Заключение
~~~~~~~~~~

📌 Этот минималистичный модуль — отличная точка входа в разработку **символьных драйверов** под Linux.  
Он не использует классы, устройства, `udev` или `sysfs`, зато даёт понимание базового потока `open → read/write → release`.

--- 

Хочешь, могу сгенерировать `.rst` файл и отправить его как `.zip`, как раньше — дай команду.
