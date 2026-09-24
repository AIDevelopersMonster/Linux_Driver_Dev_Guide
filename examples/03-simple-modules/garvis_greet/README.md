# garvis_greet

Минимальный загружаемый модуль ядра Linux из **Linux Driver Development Guide**.

При загрузке и выгрузке модуль выводит сообщения Garvis в журнал ядра.

## Validation status

**Hardware validation: PENDING**

Следующий шаг — сборка и запуск на реальном Raspberry Pi 3. После проверки статус будет обновлён на подтверждённый с указанием ядра и условий теста.

## Files

- `garvis_greet.c` — исходный код модуля
- `Makefile` — сборка внешнего kernel module
- `demo_garvis_greet.sh` — сборка, загрузка, проверка и выгрузка

## Build

Для ядра запущенной Linux-системы:

```bash
make
```

Для собственного подготовленного дерева ядра:

```bash
make KDIR=/path/to/linux
```

## Run

```bash
./demo_garvis_greet.sh
```

Сценарий уже имеет executable bit в репозитории.

Загрузка и выгрузка kernel module требуют `sudo`.

## Clean

```bash
make clean
```

## Documentation

Учебный раздел:

`docs/source/ch3_drv_simp/ge001_garvis_greet.rst`
