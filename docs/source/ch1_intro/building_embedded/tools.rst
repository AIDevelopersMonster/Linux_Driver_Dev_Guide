Инструменты для сборки Embedded Linux
=====================================

Чтобы собрать ядро, утилиты и rootfs под Raspberry Pi 3, нужны кросс-компиляторы и сборочные системы.

Кросс-компиляторы:
------------------

- `arm-none-eabi-gcc`  для bare metal (без ОС)
- `arm-linux-gnueabihf-gcc`  для Linux (glibc + kernel)
- `aarch64-linux-gnu-gcc`  для 64-битных ARM

Проверка:
::

    arm-linux-gnueabihf-gcc -v

Сборочные системы:
------------------

- `make`, `cmake`  ручные C/C++ проекты
- `meson`, `ninja`  современные быстрые сборки
- `buildroot`, `yocto`  автоматическая сборка rootfs + ядра + приложений

Полезные пакеты:
::

    sudo apt install build-essential gcc-arm-linux-gnueabihf qemu-user-static
