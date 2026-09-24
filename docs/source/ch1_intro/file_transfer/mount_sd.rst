Монтирование SD-карты напрямую на хосте
========================================

Устройства:
-----------

::

    lsblk
    dmesg | tail

Монтирование:
-------------

::

    sudo mount /dev/sdb1 /mnt/pi-boot
    sudo mount /dev/sdb2 /mnt/pi-root

Отключение:
-----------

::

    sudo umount /mnt/pi-boot
    sudo umount /mnt/pi-root

 Не извлекайте карту без `umount`, иначе возможна потеря данных.
