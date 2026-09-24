
5.10. GPIOs Mapped to IRQs
==========================

Введение
--------

Многие GPIO-линии могут использоваться не только для ввода/вывода, но и для генерации прерываний (IRQ).  
Это позволяет драйверам эффективно реагировать на события, такие как нажатие кнопки, без постоянного опроса состояния пина.

Linux предоставляет механизм привязки GPIO к IRQ с помощью `gpiod_to_irq()` и регистрации обработчика прерывания через `request_irq()`.

Поддержка в Device Tree
------------------------

Пример описания GPIO с поддержкой IRQ в `.dts`:

.. code-block:: dts

    hellokeys@0 {
        compatible = "arrow,hellokeys";
        gpios = <&gpio 17 0>;
        gpio-names = "key1";
        interrupt-parent = <&gpio>;
        interrupts = <17 2>;  // GPIO 17, falling edge
        status = "okay";
    };

Здесь:
- `interrupts = <gpio_num flags>` — описание линии и триггера;
- флаг `2` соответствует falling edge (`IRQ_TYPE_EDGE_FALLING`);
- `interrupt-parent` указывает на контроллер.

Пример использования в драйвере
-------------------------------

.. code-block:: c

    struct gpio_desc *key_gpio;
    int irq;

    key_gpio = devm_gpiod_get(&pdev->dev, "key1", GPIOD_IN);
    irq = gpiod_to_irq(key_gpio);

    ret = devm_request_irq(&pdev->dev, irq, key_isr,
                           IRQF_TRIGGER_FALLING, "key1_irq", NULL);

    if (ret) {
        dev_err(&pdev->dev, "Failed to request IRQ\n");
        return ret;
    }

    static irqreturn_t key_isr(int irq, void *dev_id) {
        pr_info("Interrupt from key1\n");
        return IRQ_HANDLED;
    }

Объяснение ключевых компонентов
-------------------------------

- `gpiod_to_irq()` — преобразует дескриптор GPIO в номер IRQ;
- `request_irq()` или `devm_request_irq()` — регистрация обработчика;
- `IRQF_TRIGGER_FALLING` и др. — флаги триггера: edge/level, high/low;
- `gpio-keys` — стандартный драйвер, который тоже использует IRQ.

Важные замечания
----------------

- Убедитесь, что в DT описан `interrupt-parent`;
- Некоторые пины не поддерживают IRQ — зависит от SoC;
- Нельзя одновременно использовать `poll()` и IRQ на одном GPIO.

Вывод
-----

Привязка GPIO к IRQ — важный инструмент для драйверов, где требуется мгновенная реакция на внешние события.  
Интерфейс `gpiod_to_irq()` делает это безопасным и переносимым способом, интегрированным в подсистему gpio + irq.