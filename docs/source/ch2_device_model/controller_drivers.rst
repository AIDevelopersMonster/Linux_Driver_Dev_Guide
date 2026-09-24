Контроллеры шин
===============

.. note::

   Эта глава является частью книги **The Linux Driver Development Guide for Raspberry Pi 3** и предназначена для русскоязычной аудитории. В ней мы рассмотрим роль **контроллеров шин**, их реализацию в ядре Linux и приведём примеры.

Что такое контроллер шины?
--------------------------

Контроллер шины  это часть драйвера, которая отвечает за:

- Обнаружение устройств на определённой шине.
- Регистрацию этих устройств в подсистеме устройства.
- Связывание с драйверами устройств через механизм сопоставления (matching).

Контроллер шины реализует и вызывает функции `device_register()` или `device_add()` для каждого устройства, которое он обнаруживает.

Пример: контроллер платформенной шины
--------------------------------------

Контроллер платформенной шины (platform bus) является встроенным инициализатором устройств, которые не находятся на какой-либо внешней шине (например, I2C или PCI), а жёстко заданы в платформе (часто в DTB или ACPI).

Рассмотрим код инициализации:

.. code-block:: c

   int __init platform_bus_init(void)
   {
       int error;
       early_platform_cleanup();
       error = device_register(&platform_bus);
       if (error)
           return error;

       error = bus_register(&platform_bus_type);
       if (error)
           device_unregister(&platform_bus);

       return error;
   }

Здесь:

- `device_register(&platform_bus)`  регистрирует корневое устройство шины.
- `bus_register(&platform_bus_type)`  регистрирует саму шину как `bus_type`.

Связь с драйверами
------------------

После регистрации устройств контроллер должен гарантировать, что они будут сопоставлены с подходящими драйверами.

Это достигается с помощью поля `match()` структуры `bus_type`, которое вызывается автоматически для определения, подходит ли данный драйвер данному устройству.

Полезные ссылки
---------------

**Elixir**  интерактивный браузер исходного кода ядра Linux:

-  `platform_bus_init()` в Elixir:
   https://elixir.bootlin.com/linux/latest/source/drivers/base/platform.c#L964

-  Структура `platform_device`:
   https://elixir.bootlin.com/linux/latest/source/include/linux/platform_device.h

-  Регистрация устройства:
   https://elixir.bootlin.com/linux/latest/source/drivers/base/core.c#L2420

-  Пример добавления устройства:
   https://elixir.bootlin.com/linux/latest/source/arch/arm/mach-omap2/board-generic.c#L118

Примеры: регистрация виртуального устройства
--------------------------------------------

Минимальный пример регистрации устройства с помощью платформенного контроллера:

.. code-block:: c

   static struct platform_device my_device = {
       .name = "my_platform_device",
       .id = -1,
   };

   static int __init my_init(void)
   {
       return platform_device_register(&my_device);
   }

   static void __exit my_exit(void)
   {
       platform_device_unregister(&my_device);
   }

   module_init(my_init);
   module_exit(my_exit);

   MODULE_LICENSE("GPL");

Что происходит:
- Мы создаём структуру `platform_device`.
- Регистрируем её при инициализации модуля.
- Ядро создаёт устройство `/sys/devices/platform/my_platform_device`.

Дополнительно
----------------

- Контроллеры важны для **автоматического обнаружения устройств**.
- Особенно актуальны для систем с **динамически подключаемыми устройствами** (например, USB, PCI).

Итог
-------

Контроллер шины  это та часть системы, которая "оживляет" устройства на шине и позволяет связать их с соответствующими драйверами.

Следующая тема  регистрация самих **драйверов устройств** и их связывание с зарегистрированными устройствами.

----

.. admonition:: Смотри также

   Видео по этой главе с живым кодом и разбором ты найдешь на нашем YouTube-канале! 


