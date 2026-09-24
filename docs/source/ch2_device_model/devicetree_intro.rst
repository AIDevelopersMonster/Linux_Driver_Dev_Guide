===========================
Device Tree (DT)
===========================

Обзор
=====

Device Tree  это структура данных для описания аппаратной конфигурации, используемой ядром Linux, особенно на архитектуре ARM.  
Она позволяет отделить описание железа от самого ядра, делая возможным создание универсального образа ядра.

Файлы:
------

- `.dts`  Device Tree Source
- `.dtsi`  включаемые файлы (инклюды)
- `.dtb`  Device Tree Blob (скомпилированный .dts)

Инструменты:
------------

- `dtc`  Device Tree Compiler

.. code-block:: bash

   dtc -I dts -O dtb -o my_device.dtb my_device.dts

Структура дерева
================

.. code-block:: dts

   / {
       compatible = "raspberrypi,3-model-b";
       model = "Raspberry Pi 3 Model B";

       soc {
           uart0: serial@20201000 {
               compatible = "brcm,bcm2835-pl011";
               reg = <0x20201000 0x1000>;
               interrupts = <2>;
               status = "okay";
           };
       };
   };

Ключевые свойства
==================

- `compatible`  определяет совместимость с драйверами
- `reg`  адресное пространство
- `interrupts`  номера прерываний
- `status`  `"okay"` / `"disabled"`

Ссылки и псевдонимы
===================

Использование `phandle` и `&uart0`:

.. code-block:: dts

   led@0 {
       compatible = "my,led";
       gpios = <&gpio 17 0>;
   };

Добавление поддержки устройства
===============================

1. Описание устройства в `.dts`  
2. Драйвер с `of_match_table`:

.. code-block:: c

   static const struct of_device_id my_driver_of_match[] = {
       { .compatible = "my,led", },
       { },
   };
   MODULE_DEVICE_TABLE(of, my_driver_of_match);

3. Регистрация платформенного драйвера (`platform_driver_register`)

Elixir ссылки
=============

- Пример `bcm283x.dtsi`: https://elixir.bootlin.com/linux/latest/source/arch/arm/boot/dts/bcm283x.dtsi  
- Документация: https://elixir.bootlin.com/linux/latest/source/Documentation/devicetree/

