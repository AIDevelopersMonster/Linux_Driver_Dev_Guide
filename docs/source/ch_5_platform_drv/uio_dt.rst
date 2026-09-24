===========================
UIO-драйвер RGB-светодиода
===========================

Описание
--------

Проект реализует UIO-драйвер для управления RGB-светодиодом на реальном железе. Управление цветами осуществляется из user space через ``/dev/uio0`` с использованием интерфейса ``mmap``.

---

Описание узла Device Tree
-------------------------

Добавьте следующий узел в ваш ``.dts`` (например, ``my_rpi3.dts``), **внутрь блока** ``&soc`` или ``soc {}``:

.. code-block:: dts

   rgb_led: rgb_led@0 {
       compatible = "kontakts,rgb-uio";
       status = "okay";
       red-gpios = <&gpio 16 GPIO_ACTIVE_HIGH>;
       green-gpios = <&gpio 20 GPIO_ACTIVE_HIGH>;
       blue-gpios = <&gpio 21 GPIO_ACTIVE_HIGH>;
   };

Убедитесь, что блок ``gpio`` определён. Пример:

.. code-block:: dts

   gpio: gpio@7e200000 {
       compatible = "brcm,bcm2835-gpio";
       reg = <0x7e200000 0x1000>;
       gpio-controller;
       #gpio-cells = <2>;
   };

---

Компиляция Device Tree
----------------------

Скомпилируйте ``.dts`` в ``.dtb``:

.. code-block:: bash

   dtc -I dts -O dtb -o bcm2710-rpi-3-b.dtb bcm2710-rpi-3-b.dts

---

Установка DTB на Raspberry Pi
-----------------------------

1. Команда для декompиляции DTB в DTS (обратное преобразование) — с помощью утилиты dtc (Device Tree Compiler):, например:

   ``dtc -I dtb -O dts -o my_rpi3.dts /boot/bcm2710-rpi-3-b.dtb``

---
    Где:
          -  I dtb — входной формат: DTB (бинарный)
          -  O dts — выходной формат: DTS (текст)
          - o — имя выходного файла
    
input.dtb — путь к бинарному DTB-файлу
Установка dtc:

   .. code-block:: bash

      sudo apt update
      sudo apt install device-tree-compiler

2. Соберите все DTB:

   .. code-block:: bash

      make dtbs

3. Скопируйте обновлённый ``.dtb`` в ``/boot``, предварительно сделав резервную копию:

   .. code-block:: bash

      sudo cp /boot/bcm2710-rpi-3-b.dtb /boot/bcm2710-rpi-3-b.dtb.old.$(date +%Y%m%d_%H%M%S)
      sudo cp bcm2710-rpi-3-b.dtb /boot/

4. Перезагрузите систему:

   .. code-block:: bash

      sudo reboot

.. warning::

   Всегда делайте резервную копию оригинального ``.dtb`` перед заменой, как показано выше!

---

Проверка корректности
---------------------

1. Убедитесь, что узел добавлен:

.. code-block:: bash

   strings /proc/device-tree/soc/rgb_led@0/compatible
   # → kontakts,rgb-uio

2. Проверьте наличие других свойств узла:

.. code-block:: bash

   ls /proc/device-tree/soc/rgb_led@0/
   # → blue-gpios  green-gpios  red-gpios  compatible  name  status

3. Посмотрите имя узла:

.. code-block:: bash

   cat /proc/device-tree/soc/rgb_led@0/name
   # → rgb_led

4. Убедитесь, что строка совместимости задана корректно (в hex-виде):

.. code-block:: bash

   hexdump -C /proc/device-tree/soc/rgb_led@0/compatible
   # → должен содержать строку "kontakts,rgb-uio"

5. (опционально) Проверьте, что правильный DTB-файл применён:

.. code-block:: bash

   dmesg | grep -i dtb
   cat /proc/device-tree/model
   # → Raspberry Pi 3 Model B Rev 1.2 (или другое, в зависимости от модели)

6. (если установлен dtc) Проверьте DTB-файл напрямую:

.. code-block:: bash

   sudo fdtdump /boot/bcm2710-rpi-3-b.dtb | less
   # → Найдите блок rgb_led@0 с compatible = "kontakts,rgb-uio"


---

Заключение
----------

UIO-драйвер RGB-светодиода реализован **без использования оверлеев** и может быть включён в любой кастомный ``.dts`` — как при эмуляции (QEMU), так и на реальном оборудовании (через пересборку и замену ``.dtb``). Такой подход упрощает изучение взаимодействия между UIO, GPIO и Device Tree.
