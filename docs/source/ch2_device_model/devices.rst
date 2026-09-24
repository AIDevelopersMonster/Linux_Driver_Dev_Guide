====================
Устройства (Devices)
====================

Введение
========

В ядре Linux всё является объектом. Устройства  ключевые сущности, которые представляют физические или виртуальные элементы системы (например, GPIO, I2C, SPI, UART, память, и т.д.)

Регистрация устройств
======================

Для регистрации устройства используется функция:

.. code-block:: c

   int device_register(struct device *dev);

Это добавляет устройство в иерархию устройства Linux и инициирует поиск подходящего драйвера на соответствующей шине.

Структура device
================

Структура `device` определена в `include/linux/device.h`:

.. code-block:: c

   struct device {
       struct device           *parent;
       struct device_private   *p;
       struct kobject          kobj;
       const char              *init_name;
       const struct device_type *type;
       struct bus_type         *bus;
       struct device_driver    *driver;
       void                    *platform_data;
       struct dev_pm_info      power;
       ...
   };

Ключевые поля:
- `parent`  родительское устройство
- `bus`  указатель на шину
- `driver`  драйвер, связанный с этим устройством
- `platform_data`  данные, специфичные для платформы
- `init_name`  имя устройства

Создание и регистрация устройства вручную
==========================================

.. code-block:: c

   static struct device my_device = {
       .init_name = "my_device",
       .bus = &my_bus_type,
   };

   static int __init my_device_init(void) {
       return device_register(&my_device);
   }

   module_init(my_device_init);

Работа через platform_device
=============================

Обычно регистрация устройства упрощается через структуру `platform_device`, которая включает `struct device` внутри себя.

.. code-block:: c

   static struct platform_device my_pdev = {
       .name = "my_driver",
       .id = -1,
   };

   static int __init my_pdev_init(void) {
       return platform_device_register(&my_pdev);
   }

   module_init(my_pdev_init);

Sysfs и устройства
===================

После регистрации устройства оно отображается в `/sys/devices/` и в соответствующей шине `/sys/bus/platform/devices/`.

Можно наблюдать:
- параметры устройства
- ассоциацию с драйвером
- иерархию (родитель/дочерние)

Полезные ссылки на исходники в Elixir
======================================

- `struct device`: https://elixir.bootlin.com/linux/latest/source/include/linux/device.h#L501  
- `device_register`: https://elixir.bootlin.com/linux/latest/source/drivers/base/core.c#L2286  
- `platform_device_register`: https://elixir.bootlin.com/linux/latest/source/drivers/base/platform.c#L258

