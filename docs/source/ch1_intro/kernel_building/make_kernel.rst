Сборка ядра, модулей и dtb
===========================

::

    make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs -j4

Результаты:
-----------

- `zImage`  arch/arm/boot/zImage
- `.dtb`  arch/arm/boot/dts/
- Модули устанавливаются отдельно

Полезно:
--------

- Используйте `ccache`
- `-j$(nproc)`  для полной загрузки CPU
