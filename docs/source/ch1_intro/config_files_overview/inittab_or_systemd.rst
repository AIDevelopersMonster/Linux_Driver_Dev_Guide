Инициализация: systemd и inittab
================================

Systemd:
- `/lib/systemd/systemd`  главный процесс
- `.target`, `.service`, `journalctl`, `systemctl`

inittab (устарело):
- `/etc/inittab`
- Работает через `init=/sbin/init`
