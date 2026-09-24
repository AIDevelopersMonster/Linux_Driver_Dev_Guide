.. _bus_core_drivers:

Драйверы шин (Bus Core Drivers)
===============================

Для каждой шины, поддерживаемой ядром Linux, существует соответствующий драйвер шины (bus core driver).
Шина  это канал связи между процессором и одним или несколькими устройствами. С точки зрения модели
устройств Linux, **все устройства подключены через шину**, даже если она виртуальная, внутренняя или
"платформенная" (platform bus).

Описание bus_type
------------------

Каждый драйвер шины выделяет и регистрирует структуру ``bus_type``:

.. code-block:: c

    struct bus_type {
        const char *name;
        const char *dev_name;
        struct device *dev_root;
        struct device_attribute *dev_attrs;
        const struct attribute_group **bus_groups;
        const struct attribute_group **dev_groups;
        const struct attribute_group **drv_groups;
        int (*match)(struct device *dev, struct device_driver *drv);
        int (*uevent)(struct device *dev, struct kobj_uevent_env *env);
        int (*probe)(struct device *dev);
        int (*remove)(struct device *dev);
        void (*shutdown)(struct device *dev);
        int (*online)(struct device *dev);
        int (*offline)(struct device *dev);
        int (*suspend)(struct device *dev, pm_message_t state);
        int (*resume)(struct device *dev);
        const struct dev_pm_ops *pm;
        struct iommu_ops *iommu_ops;
        struct subsys_private *p;
        struct lock_class_key lock_key;
    };

Регистрация новой шины осуществляется с помощью функции ``bus_register()``. Например, для платформенной
шины:

.. code-block:: c

    struct bus_type platform_bus_type = {
        .name = "platform",
        .dev_groups = platform_dev_groups,
        .match = platform_match,
        .uevent = platform_uevent,
        .pm = &platform_dev_pm_ops,
    };

    EXPORT_SYMBOL_GPL(platform_bus_type);

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

После вызова ``bus_register()``, ядро создаёт директорию `/sys/bus/platform/`, содержащую
поддиректории `devices/` и `drivers/`.

subsys_private и списки устройств/драйверов
--------------------------------------------

Один из членов ``struct bus_type``  это указатель на структуру ``subsys_private``, определённую
в ``drivers/base/base.h``:

.. code-block:: c

    struct subsys_private {
        struct kset subsys;
        struct kset *devices_kset;
        struct list_head interfaces;
        struct mutex mutex;
        struct kset *drivers_kset;
        struct klist klist_devices;
        struct klist klist_drivers;
        struct blocking_notifier_head bus_notifier;
        unsigned int drivers_autoprobe:1;
        struct bus_type *bus;
        struct kset glue_dirs;
        struct class *class;
    };

Списки ``klist_devices`` и ``klist_drivers`` содержат, соответственно, все устройства и драйверы,
зарегистрированные на данной шине. Они обновляются функциями:

- ``device_register()``  при добавлении устройства;
- ``driver_register()``  при инициализации драйвера.

Алгоритм привязки устройства к драйверу
----------------------------------------

1. Когда **новое устройство подключается**, драйвер контроллера шины вызывает ``device_register()``.
2. Ядро перебирает список драйверов на шине и вызывает ``match()``, чтобы найти подходящий драйвер.
3. При совпадении вызывается функция ``probe()`` драйвера  происходит **привязка** (binding).

И наоборот:

- Если сначала загружается **драйвер**, то ``driver_register()`` вызывает сопоставление с уже
  существующими устройствами.

Итог: привязка возможна как при появлении устройства, так и при загрузке драйвера.

Назначение драйвера шины
-------------------------

Драйвер шины (bus core driver):

1. Регистрирует шину в системе.
2. Позволяет регистрировать драйверы контроллеров шин (например, PCI, USB контроллеры).
3. Позволяет регистрировать драйверы устройств.
4. Выполняет сопоставление устройств с драйверами с помощью функции ``match()``.

---

**Примечание:** Вы можете исследовать структуру и реализацию этих механизмов в Linux-ядре
через [elixir.bootlin.com](https://elixir.bootlin.com/linux/latest/source)  отличный ресурс
для просмотра исходников с удобной навигацией и кросс-ссылками.
