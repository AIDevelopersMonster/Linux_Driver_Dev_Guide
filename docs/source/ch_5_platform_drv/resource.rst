===============================
5.21: Platform Driver Resources
===============================

В этом разделе мы изучаем, как платформа устройства (Platform Device) описывает аппаратные ресурсы, такие как регистры памяти и прерывания, и как драйвер получает к ним доступ.


struct platform_device
----------------------

В ядре Linux структура `platform_device` представляет собой устройство, не использующее шину с автообнаружением (например, I2C, PCI), и описывает его ресурсы:

.. code-block:: c

    struct platform_device {
        const char *name;
        int id;
        struct device dev;
        u32 num_resources;
        struct resource *resource;
        ...
    };

Платформенные ресурсы задаются через структуру `struct resource`.


struct resource
---------------

Структура описания ресурсов (например, адресов MMIO или IRQ):

.. code-block:: c

    struct resource {
        resource_size_t start;
        resource_size_t end;
        const char *name;
        unsigned long flags;
        struct resource *parent, *sibling, *child;
    };

Пояснение полей `resource`
--------------------------

- ``start`` и ``end`` — начальный и конечный физические адреса или номер IRQ
- ``name`` — удобная строка-идентификатор (например, "mmio", "irq")
- ``flags`` — указывает тип ресурса:
  - `IORESOURCE_MEM` — область памяти (MMIO)
  - `IORESOURCE_IRQ` — номер прерывания (IRQ)
  - и др.

Функции доступа к ресурсам
--------------------------

1. **platform_get_resource()**

.. code-block:: c

    struct resource *platform_get_resource(struct platform_device *pdev,
                                           unsigned int type, unsigned int num);

Получает ресурс типа `IORESOURCE_MEM` или `IORESOURCE_IRQ` с заданным индексом `num`.

Пример:

.. code-block:: c

    struct resource *res;
    res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
    if (res)
        base = ioremap(res->start, resource_size(res));

2. **platform_get_irq()**

.. code-block:: c

    int platform_get_irq(struct platform_device *pdev, unsigned int num);

Получает номер IRQ из ресурсов.

Пример:

.. code-block:: c

    int irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;


Пример использования
--------------------

.. code-block:: c

    static int my_probe(struct platform_device *pdev) {
        struct resource *res;
        void __iomem *base;

        res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
        base = devm_ioremap_resource(&pdev->dev, res);

        int irq = platform_get_irq(pdev, 0);

        return 0;
    }


Заключение
----------

Использование структуры ресурсов и платформенных функций `platform_get_resource()` и `platform_get_irq()` позволяет драйверу быть максимально абстрагированным от конкретной архитектуры и сосредоточиться на логике управления устройством.

