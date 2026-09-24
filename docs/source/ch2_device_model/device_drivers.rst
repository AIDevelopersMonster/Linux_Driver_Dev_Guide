===============================
Регистрация драйверов устройств
===============================

Введение
========

После регистрации шины и контроллера следующим логическим шагом становится регистрация драйверов устройств, которые будут обслуживать устройства, подключённые к этой шине.

Регистрация драйвера
=====================

Регистрация драйвера осуществляется с помощью вызова функции:

.. code-block:: c

   int driver_register(struct device_driver *drv);

Эта функция:
- добавляет драйвер в список доступных для данной шины
- запускает процесс сопоставления драйвера с подходящими устройствами на шине с помощью `match()`
- при нахождении устройства вызывает `probe()` драйвера

Структура device_driver
========================

Структура описана в `include/linux/device.h`:

.. code-block:: c

   struct device_driver {
       const char *name;
       struct bus_type *bus;
       struct module *owner;
       const char *mod_name;
       bool suppress_bind_attrs;
       const struct of_device_id *of_match_table;
       int (*probe) (struct device *dev);
       int (*remove) (struct device *dev);
       void (*shutdown) (struct device *dev);
       int (*suspend) (struct device *dev, pm_message_t state);
       int (*resume) (struct device *dev);
       const struct attribute_group **groups;
       const struct dev_pm_ops *pm;
       struct driver_private *p;
   };

Элементы:
- `name`  имя драйвера
- `bus`  к какой шине относится
- `probe`  вызывается при успешном сопоставлении устройства

Пример драйвера
===============

.. code-block:: c

   static int my_probe(struct device *dev) {
       pr_info("My device found!\n");
       return 0;
   }

   static struct device_driver my_driver = {
       .name = "my_driver",
       .bus = &platform_bus_type,
       .probe = my_probe,
   };

   static int __init my_driver_init(void) {
       return driver_register(&my_driver);
   }

   module_init(my_driver_init);

Сопоставление устройств и драйверов
====================================

При регистрации драйвера:
- список всех устройств на шине перебирается
- если `match()` возвращает истину  вызывается `probe()`

При добавлении устройства:
- аналогично перебирается список драйверов

Таким образом, привязка возможна в обе стороны: как при загрузке драйвера, так и при добавлении устройства.

Работа с sysfs
==============

После регистрации драйвера и устройства в `/sys/bus/platform/drivers/` появляется:
- каталог с именем драйвера
- символьные ссылки на устройства

Полезные ссылки на исходники в Elixir
======================================

- `driver_register`: https://elixir.bootlin.com/linux/latest/source/drivers/base/driver.c#L170  
- `struct device_driver`: https://elixir.bootlin.com/linux/latest/source/include/linux/device.h#L238  
- Пример `platform_driver_register`: https://elixir.bootlin.com/linux/latest/source/include/linux/platform_device.h#L134  

---

