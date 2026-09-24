Установка ядра и модулей на Raspberry Pi
========================================

Копирование ядра:
::

    cp arch/arm/boot/zImage /mnt/pi-boot/kernel.img

    cp arch/arm/boot/dts/*.dtb /mnt/pi-boot/
    cp arch/arm/boot/dts/overlays/*.dtb* /mnt/pi-boot/overlays/

Установка модулей:
::

    sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules_install INSTALL_MOD_PATH=/mnt/pi-root

Проверка:
::

    uname -a
    dmesg | grep -i firmware
    ls /lib/modules/
