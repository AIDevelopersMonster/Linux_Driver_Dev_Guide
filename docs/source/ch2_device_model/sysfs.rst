======================
Файловая система sysfs
======================

Обзор
=====

`sysfs`  это виртуальная файловая система, создаваемая ядром Linux, которая предоставляет представление в виде иерархии каталогов, отражающей внутреннюю структуру устройств, драйверов и шин.

Путь монтирования: `/sys`

Назначение sysfs:
-----------------

- Позволяет пользователям и разработчикам взаимодействовать с ядром через файловую систему
- Используется для отладки, управления параметрами устройств и мониторинга
- Предоставляет доступ к объектам: устройства, драйверы, шины, классы и атрибуты

Связь с model device-driver
===========================

Каждое устройство (`struct device`) и драйвер (`struct device_driver`) автоматически создают записи в `sysfs` при регистрации.

Примеры расположения:
---------------------

.. code-block:: none

   /sys/bus/platform/devices/
   /sys/bus/i2c/drivers/
   /sys/class/gpio/
   /sys/devices/platform/

Атрибуты sysfs
==============

Создаются с помощью макросов ядра:

.. code-block:: c

   DEVICE_ATTR(name, mode, show, store);

Пример:

.. code-block:: c

   static ssize_t foo_show(struct device *dev, struct device_attribute *attr, char *buf) {
       return sprintf(buf, "%d\n", foo_value);
   }

   static ssize_t foo_store(struct device *dev, struct device_attribute *attr, const char *buf, size_t count) {
       sscanf(buf, "%d", &foo_value);
       return count;
   }

   static DEVICE_ATTR(foo, 0660, foo_show, foo_store);

   static int my_driver_probe(struct platform_device *pdev) {
       device_create_file(&pdev->dev, &dev_attr_foo);
       return 0;
   }

Удаление атрибута:

.. code-block:: c

   device_remove_file(&pdev->dev, &dev_attr_foo);

Где можно найти это в исходниках Elixir
=======================================

- `sysfs`: https://elixir.bootlin.com/linux/latest/source/fs/sysfs/
- `device_create_file`: https://elixir.bootlin.com/linux/latest/source/drivers/base/core.c#L2163
- `DEVICE_ATTR`: https://elixir.bootlin.com/linux/latest/source/include/linux/device.h#L775

