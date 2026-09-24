===========================
Инфраструктура kobject
===========================

Обзор
=====

`kobject` (kernel object)  это базовая структура, используемая ядром Linux для управления объектами, которые появляются в пространстве `sysfs`.

Располагается в: `include/linux/kobject.h`

Цели:
-----

- Организация иерархии объектов ядра
- Автоматическое управление ссылками
- Интеграция с файловой системой `sysfs`
- Упрощение отслеживания жизненного цикла объектов

Основные структуры
==================

.. code-block:: c

   struct kobject {
       const char *name;
       struct list_head entry;
       struct kobject *parent;
       struct kset *kset;
       struct kobj_type *ktype;
       struct kernfs_node *sd;
       struct kref kref;
   };

- `kref`: счётчик ссылок
- `ktype`: содержит атрибуты и методы show/store
- `kset`: группа `kobject`, объединённая общей логикой

Создание и регистрация kobject
==============================

.. code-block:: c

   struct kobject *kobject_create_and_add(const char *name, struct kobject *parent);

Удаление:

.. code-block:: c

   kobject_put(kobj);

Пример: создание каталога в /sys

.. code-block:: c

   static struct kobject *example_kobj;

   example_kobj = kobject_create_and_add("example", kernel_kobj);

   if (!example_kobj)
       return -ENOMEM;

Добавление атрибутов:

.. code-block:: c

   static ssize_t foo_show(struct kobject *kobj, struct kobj_attribute *attr, char *buf) {
       return sprintf(buf, "%d\n", foo);
   }

   static struct kobj_attribute foo_attr = __ATTR(foo, 0660, foo_show, NULL);

   sysfs_create_file(example_kobj, &foo_attr.attr);

Удаление:

.. code-block:: c

   sysfs_remove_file(example_kobj, &foo_attr.attr);
   kobject_put(example_kobj);

Связь с другими подсистемами
=============================

- `device`, `bus`, `driver`, `class`  все реализованы через `kobject`
- `kobject` создаёт записи в `sysfs` автоматически
- Используется в механизме генерации `uevent`

Полезные ссылки (Elixir)
=========================

- `kobject` структура: https://elixir.bootlin.com/linux/latest/source/include/linux/kobject.h
- Создание `kobject`: https://elixir.bootlin.com/linux/latest/source/lib/kobject.c#L382
- Пример с атрибутами: https://elixir.bootlin.com/linux/latest/source/samples/kobject/kobject-example.c
