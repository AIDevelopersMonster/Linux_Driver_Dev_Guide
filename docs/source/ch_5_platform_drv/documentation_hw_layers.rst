5.5: Документация по взаимодействию с оборудованием
===================================================

Обзор уровней описания аппаратуры в Linux
------------------------------------------

Linux использует многоуровневую модель представления оборудования, начиная от описания в Device Tree до структуры ``struct device`` в драйвере.

Основные уровни:

1. **Аппаратный уровень (SoC)**  
   - Физические устройства: GPIO, UART, I2C, SPI, таймеры и пр.  
   - Представлены в ядре как «узлы» Device Tree (``&gpio``, ``&uart0``, ``&i2c1`` и т.д.)

2. **Device Tree (DT)**  
   - Текстовый `.dts` описывает структуру оборудования.  
   - Свойства: ``compatible``, ``reg``, ``gpios``, ``status``, ``label``, ``phandle``.  
   - Пример:

.. code-block:: dts

   hellokeys@0 {
       compatible = "arrow,hellokeys";
       gpios = <&gpio 17 0>, <&gpio 27 0>;
       status = "okay";
   }

3. **Шины и драйверы (bus + driver)**  
   - Linux определяет устройство через шину: ``platform``, ``i2c``, ``spi`` и др.  
   - Регистрация драйвера через ``platform_driver``, ``i2c_driver``, ``spi_driver``.  
   - Поиск соответствий осуществляется через ``of_match_table``.

4. **`struct device` и `struct driver`**  
   - Когда вызывается ``probe()``, ядро передаёт ``struct platform_device``, включающий ``struct device``.  
   - Через него можно получить доступ к DT-свойствам: ``pdev->dev.of_node``.

5. **SysFS — представление устройств в userspace**  
   - Каталоги: ``/sys/class``, ``/sys/bus``, ``/sys/devices``  
   - Показывают связи между устройствами, драйверами и их DT-описанием.

Примеры путей в sysfs:
-----------------------

.. code-block:: bash

   /sys/bus/platform/devices/hellokeys@0
   /sys/bus/platform/drivers/hellokeys
   /sys/class/misc/mydev
   /proc/device-tree/soc/hellokeys@0

Назначение поля compatible и связь с драйвером
----------------------------------------------

В драйвере:

.. code-block:: c

   static const struct of_device_id hellokeys_of_match[] = {
       { .compatible = "arrow,hellokeys" },
       {},
   };
   MODULE_DEVICE_TABLE(of, hellokeys_of_match);

   static struct platform_driver hellokeys_driver = {
       .probe = hellokeys_probe,
       .remove = hellokeys_remove,
       .driver = {
           .name = "hellokeys",
           .of_match_table = hellokeys_of_match,
       },
   };

Таким образом, если ``compatible = "arrow,hellokeys"`` в DT, то ядро автоматически вызывает ``probe()`` при загрузке модуля.

Названия и идентификация устройств
----------------------------------

- ``label`` — имя, отображаемое в user space или логах
- ``name`` — системное имя (например, в ``/sys/class/misc/mydev`` → `mydev`)
- ``unit address`` — часть DT-имени после ``@`` (например, `hellokeys@0`), нужна для уникальности, но не влияет на поиск.

Итог
----

Linux строит связку:  
**Device Tree → Bus (platform) → Driver → Device → SysFS**

Это позволяет драйверам и ядру динамически определять оборудование и связывать его с нужным кодом.

Следующий шаг: изучим работу с ``class``, ``uevent``, ``ioctl``, ``sysfs`` и ``UIO`` в следующих разделах главы 5.
