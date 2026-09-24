rc.local: собственные команды при старте
========================================

Файл `/etc/rc.local` позволяет выполнять кастомные действия при загрузке.

Пример:
::

    /usr/bin/python3 /home/pi/startup_led.py &
    exit 0

В systemd требуется вручную включить службу:
::

    sudo systemctl enable rc-local.service
