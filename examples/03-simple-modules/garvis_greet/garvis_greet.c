#include <linux/init.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Alex Malachevsky");
MODULE_DESCRIPTION("Garvis greeting kernel module");
MODULE_VERSION("1.0");

static int __init garvis_init(void)
{
    pr_info("Garvis говорит: Привет из ядра Linux!\n");
    return 0;
}

static void __exit garvis_exit(void)
{
    pr_info("Garvis уходит: До встречи!\n");
}

module_init(garvis_init);
module_exit(garvis_exit);
