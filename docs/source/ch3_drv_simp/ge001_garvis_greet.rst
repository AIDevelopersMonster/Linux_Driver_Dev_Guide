================================
Первый модуль ядра: garvis_greet
================================

Введение
========

В этом разделе мы создадим простой модуль ядра Linux под названием ``garvis_greet`` — это наш *индивидуальный Hello World*.  
Этот модуль напечатает сообщение в журнал ядра при загрузке и выгрузке, представляясь как «Garvis» — ваш новый друг в мире драйверов. 

Мы будем использовать Raspberry Pi 3, подключённый по SSH, а ядро и сборка будут выполняться локально.

Теория: как устроен модуль ядра
===============================

Модуль ядра — это двоичный объект (.ko), который можно загружать и выгружать в ядро без его перекомпиляции.  
Основные компоненты:

- ``#include <linux/init.h>`` — директивы для функций инициализации
- ``#include <linux/module.h>`` — макросы и типы для работы с модулями
- ``module_init()`` / ``module_exit()`` — точки входа и выхода
- ``printk()`` — логирование в ядро

Создание проекта garvis_greet
=============================

1. Структура каталога::

    garvis_greet/
    ├── garvis_greet.c
    ├── Makefile
    └── demo_garvis_greet.sh

2. Исходный код модуля: ``garvis_greet.c``

.. code-block:: c

    #include <linux/module.h>
    #include <linux/init.h>

    MODULE_LICENSE("GPL");
    MODULE_AUTHOR("You");
    MODULE_DESCRIPTION("Garvis говорит из ядра!");

    static int __init garvis_init(void) {
        printk(KERN_INFO "Garvis говорит: Привет из ядра Linux!\\n");
        return 0;
    }

    static void __exit garvis_exit(void) {
        printk(KERN_INFO "Garvis уходит: До встречи!\\n");
    }

    module_init(garvis_init);
    module_exit(garvis_exit);

3. Makefile

.. code-block:: make

    obj-m += garvis_greet.o

    all:
        make -C ../linux M=$(PWD) modules

    clean:
        make -C ../linux M=$(PWD) clean

4. Скрипт запуска: ``demo_garvis_greet.sh``

.. code-block:: bash

    #!/bin/bash
    echo " Проверка: загружен ли модуль garvis_greet..."
    if lsmod | grep -q garvis_greet; then
        echo " Модуль уже загружен. Удаляем..."
        sudo rmmod garvis_greet
    fi

    echo " 1. Очистка предыдущей сборки (на всякий случай)..."
    make clean

    echo " 2. Повторная сборка драйвера..."
    make

    echo " 3. Загрузка модуля garvis_greet.ko в ядро..."
    sudo insmod garvis_greet.ko

    echo " 4. Чтение последних сообщений ядра (dmesg)..."
    echo "---------------------------------------------"
    dmesg | tail -n 10
    echo "---------------------------------------------"
    echo " Выше вы должны увидеть сообщение от Garvis!"
    read -p " Нажмите [Enter] для удаления модуля..."

    echo " Удаление модуля из ядра..."
    sudo rmmod garvis_greet
    echo " Готово! Модуль выгружен."

5. Не забудьте:

.. code-block:: bash

    chmod +x demo_garvis_greet.sh

Сборка и запуск на Raspberry Pi
===============================

1. Убедитесь, что у вас локальная сборка ядра или headers:

.. code-block:: bash

    git clone --depth=1 https://github.com/raspberrypi/linux
    cd linux
    KERNEL=kernel7
    make bcm2709_defconfig

2. Вернитесь в каталог ``garvis_greet`` и запустите:

.. code-block:: bash

    ./demo_garvis_greet.sh

Вывод в `dmesg` должен содержать:

.. code-block:: text

    Garvis говорит: Привет из ядра Linux!

Вывод
=====

Вы создали, собрали, загрузили и выгрузили свой первый модуль ядра Linux.  
Поздравляем! Вы теперь знаете, как *Garvis* передаёт привет из ядра 

В следующем модуле мы добавим взаимодействие с пользователем через `/proc` или `/sys`.

