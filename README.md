# Linux Driver Development Guide

Практическое руководство по разработке драйверов Linux на примере Raspberry Pi 3.

Проект включает исходную документацию Sphinx, примеры кода и лабораторные материалы по устройству Linux, модели устройств, модулям ядра, символьным и platform-драйверам, Device Tree, GPIO, MMIO и UIO.

## Documentation

Исходники документации находятся в:

    docs/source/

Локальная сборка:

    .\.venv\Scripts\sphinx-build.exe -b html docs\source docs\_build\html

Результат:

    docs\_build\html\index.html

Для локального просмотра под Windows используется:

    .\.venv\Scripts\python.exe tools\serve_docs.py

После запуска документация доступна по адресу:

    http://127.0.0.1:8001/

## Current status

- Sphinx source restored from the original 2025 project
- 100 documentation pages
- Python 3.14 compatible
- Sphinx 9.1.0
- sphinx-rtd-theme 3.1.0
- clean documentation build: 0 warnings
- GitHub Pages deployment: active

## Online documentation

https://aidevelopersmonster.github.io/Linux_Driver_Dev_Guide/

## Repository structure

    docs/       Sphinx documentation
    examples/   standalone source-code examples and labs
    tools/      development and documentation utilities

## Author

Alex Malachevsky  
GitHub: AIDevelopersMonster

