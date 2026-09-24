5.12. Exchanging Data Between Kernel and User Spaces
=====================================================

Введение
--------

Одна из важнейших задач при написании драйверов Linux — это организация **безопасного обмена данными между пространствами ядра (kernel space) и пользователя (user space)**.  
Такой обмен необходим, например, для чтения состояния кнопки или установки уровня на GPIO.

В ядре предоставляется несколько стандартных интерфейсов:

- `read()` и `write()` — классический POSIX-способ взаимодействия
- `ioctl()` — для управления и передачи структур
- `poll()` и `select()` — для реактивного ожидания событий
- `mmap()` — отображение памяти между user и kernel
- `sysfs` / `procfs` — файловые интерфейсы без `open()`

---

Классический пример: read()
----------------------------

Рассмотрим простую реализацию `read()` в нашем драйвере `hellokeys_rpi3_misc_dt`:

.. code-block:: c

    static ssize_t hellokeys_read(struct file *file, char __user *buf, size_t count, loff_t *ppos) {
        char msg[64];
        int len;

        // Пример: опрос двух GPIO
        int val1 = gpiod_get_value(key1);
        int val2 = gpiod_get_value(key2);

        len = snprintf(msg, sizeof(msg), "key1: %d\\nkey2: %d\\n", val1, val2);
        return simple_read_from_buffer(buf, count, ppos, msg, len);
    }

Пояснение:

- `char __user *buf` — указатель на буфер в user space
- мы создаём строку в kernel space, затем копируем её через `simple_read_from_buffer()` или `copy_to_user()`

---

Передача данных из userspace: write()
--------------------------------------

Если вы хотите передать данные в ядро (например, установить цвет RGB), реализуется `write()`:

.. code-block:: c

    static ssize_t rgb_write(struct file *file, const char __user *buf, size_t count, loff_t *ppos) {
        char kbuf[32];
        int r, g, b;

        if (count > sizeof(kbuf) - 1) return -EINVAL;

        if (copy_from_user(kbuf, buf, count)) return -EFAULT;
        kbuf[count] = 0;

        // Пример: "255 0 128"
        if (sscanf(kbuf, "%d %d %d", &r, &g, &b) == 3) {
            gpiod_set_value(led_r, r > 0);
            gpiod_set_value(led_g, g > 0);
            gpiod_set_value(led_b, b > 0);
            return count;
        }

        return -EINVAL;
    }

---

Что важно помнить при обмене:
------------------------------

- **User Space → Kernel Space**: используем `copy_from_user()`  
- **Kernel Space → User Space**: используем `copy_to_user()` или `simple_read_from_buffer()`
- Нельзя напрямую разыменовывать указатели из user space
- Следите за безопасностью буфера: проверяйте `count`, добавляйте `0` в строки

---

Когда использовать ioctl()
---------------------------

`ioctl()` подходит для:

- передачи флагов, параметров, структур
- конфигурирования устройств

.. code-block:: c

    static long my_ioctl(struct file *file, unsigned int cmd, unsigned long arg) {
        int kval;

        if (copy_from_user(&kval, (int __user *)arg, sizeof(int)))
            return -EFAULT;

        if (kval == 42) do_something_special();

        return 0;
    }

---

Вывод
-----

Обмен данными между ядром и пользователем — основа интерактивных драйверов.  
Для простых задач (GPIO, флаги, сообщения) достаточно `read()` / `write()`.  
Для более сложных — используем `ioctl()` или `mmap()`.

Реализация этих функций позволяет из user space обращаться к устройству через обычные системные вызовы: `cat`, `echo`, `open()`, `read()`, `write()`.

