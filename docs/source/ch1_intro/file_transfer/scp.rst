Копирование файлов через SSH (scp, sftp, rsync)
===============================================

scp:
----

::

    scp ./module.ko pi@192.168.0.42:/home/pi/

sftp:
-----

::

    sftp pi@192.168.0.42

    put ./file.txt
    get /home/pi/result.txt

rsync:
------

::

    rsync -avz ./build/ pi@192.168.0.42:/home/pi/project/

Устранение ошибок:
------------------

- Убедитесь, что SSH включён (`sudo raspi-config`)
- Проблемы с правами  используйте `sudo chown`
