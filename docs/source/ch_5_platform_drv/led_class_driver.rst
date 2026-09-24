Глава 5.26: Подключение RGB LED к LED class через DT и кастомный драйвер
========================================================================

Цель
----

Подключить RGB-светодиод к подсистеме ``LED class`` в Linux без указания GPIO в Device Tree, используя кастомный драйвер, в котором все GPIO определяются внутри кода.

Исходный код драйвера с комментариями
-------------------------------------

.. code-block:: c
   :linenos:

   #include <linux/module.h>
   #include <linux/init.h>
   #include <linux/of.h>
   #include <linux/of_device.h>
   #include <linux/platform_device.h>
   #include <linux/leds.h>
   #include <linux/gpio.h>
   #include <linux/gpio/consumer.h>
   #include <linux/slab.h>
   #include <linux/kernel.h>
   #include <linux/types.h>

   #define MAX_LEDS 3

   struct rgb_led {
       struct led_classdev cdev;
       int gpio;
   };

   struct rgb_led_data {
       struct rgb_led *leds[MAX_LEDS];
       int count;
   };

   static void rgb_brightness_set(struct led_classdev *cdev, enum led_brightness brightness)
   {
       struct rgb_led *led = container_of(cdev, struct rgb_led, cdev);
       gpio_set_value_cansleep(led->gpio, brightness ? 1 : 0);
   }

   static int rgb_led_probe(struct platform_device *pdev)
   {
       struct device_node *np = pdev->dev.of_node;
       struct device_node *child;
       struct rgb_led_data *data;
       const char *label;
       int ret, i;
       int gpios[] = { 16, 20, 21 }; // RED, GREEN, BLUE

       data = devm_kzalloc(&pdev->dev, sizeof(*data), GFP_KERNEL);
       if (!data)
           return -ENOMEM;

       i = 0;
       for_each_child_of_node(np, child) {
           struct rgb_led *led;

           if (i >= MAX_LEDS)
               break;

           led = kzalloc(sizeof(*led), GFP_KERNEL);
           if (!led)
               return -ENOMEM;

           led->gpio = gpios[i];

           ret = gpio_request(led->gpio, "rgb-led");
           if (ret) {
               dev_err(&pdev->dev, "Failed to request GPIO %d\n", led->gpio);
               kfree(led);
               return ret;
           }

           gpio_direction_output(led->gpio, 0);

           if (of_property_read_string(child, "label", &label))
               label = "rgb:unknown";

           led->cdev.name = kstrdup(label, GFP_KERNEL);
           led->cdev.brightness = LED_OFF;
           led->cdev.max_brightness = 1;
           led->cdev.brightness_set = rgb_brightness_set;

           ret = led_classdev_register(&pdev->dev, &led->cdev);
           if (ret) {
               dev_err(&pdev->dev, "Failed to register LED %s\n", label);
               gpio_set_value(led->gpio, 0);
               gpio_free(led->gpio);
               kfree(led->cdev.name);
               kfree(led);
               return ret;
           }

           dev_info(&pdev->dev, "Registered LED: %s on GPIO %d\n", label, led->gpio);
           data->leds[i++] = led;
       }

       data->count = i;
       platform_set_drvdata(pdev, data);

       dev_info(&pdev->dev, "RGB LED driver initialized with %d LED(s)\n", data->count);
       return 0;
   }

   static int rgb_led_remove(struct platform_device *pdev)
   {
       struct rgb_led_data *data = platform_get_drvdata(pdev);
       int i;

       for (i = 0; i < data->count; i++) {
           struct rgb_led *led = data->leds[i];
           if (!led)
               continue;

           pr_info("Unregistering LED: %s from GPIO %d\n", led->cdev.name, led->gpio);
           led_classdev_unregister(&led->cdev);
           gpio_set_value(led->gpio, 0);
           gpio_free(led->gpio);
           kfree(led->cdev.name);
           kfree(led);
       }

       pr_info("RGB LED driver removed\n");
       return 0;
   }

   static const struct of_device_id rgb_led_of_match[] = {
       { .compatible = "myvendor,rgb-led" },
       { /* sentinel */ }
   };
   MODULE_DEVICE_TABLE(of, rgb_led_of_match);

   static struct platform_driver rgb_led_driver = {
       .driver = {
           .name = "rgb-led",
           .of_match_table = rgb_led_of_match,
       },
       .probe = rgb_led_probe,
       .remove = rgb_led_remove,
   };

   module_platform_driver(rgb_led_driver);

   MODULE_LICENSE("GPL");
   MODULE_AUTHOR("Your Name");
   MODULE_DESCRIPTION("Reloadable RGB LED driver with dmesg logging");


---

Фрагмент Device Tree
---------------------

.. code-block:: dts

   rgb-led@0 {
       compatible = "myvendor,rgb-led";
       status = "okay";

       red {
           label = "rgb:red";
       };

       green {
           label = "rgb:green";
       };

       blue {
           label = "rgb:blue";
       };
   };

Комментарии:

- Описывается один узел `rgb-led@0` с подузлами `red`, `green`, `blue`
- Пины GPIO в DT не указываются
- Все LED автоматически получают label и отображаются в `/sys/class/leds/`

Проверка результата
--------------------

.. code-block:: bash

   # Проверка устройств LED class
   ls /sys/class/leds/
   # → должны появиться:
   # rgb:red  rgb:green  rgb:blue

   # Включение красного светодиода
   echo 1 | sudo tee /sys/class/leds/rgb:red/brightness

   # Выключение синего
   echo 0 | sudo tee /sys/class/leds/rgb:blue/brightness

   # Проверка, что узел в DT активен
   ls /proc/device-tree/soc/rgb-led@0/
   # → red green blue compatible status ...

Вывод
-----

Мы реализовали минимальный, понятный, переносимый драйвер для RGB LED, где вся логика и GPIO-привязка находятся внутри модуля. Управление выполняется через стандартный LED class интерфейс, без использования устаревшего sysfs GPIO или userspace-демонов.

