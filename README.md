# Конфигурационное управление · Практическая №2 · Вариант 23

Инструмент для исследования зависимостей npm-пакетов. Проект делается
в 5 этапов; текущий коммит соответствует этапу 1.

## Требования

Python 3.11+ (встроенная библиотека `tomllib`). Сторонние Python-пакеты
не требуются.

## Структура

- `src/` — исходный код;
- `tests/` — автоматические тесты;
- `configs/` — примеры настроек TOML;
- `fixtures/` — учебные графы;
- `run.bat`, `run.sh` — скрипты запуска.

## Запуск

Windows PowerShell:

```powershell
.\run.bat configs\test.toml
```

Linux/macOS: `./run.sh configs/test.toml`.

Тесты: `python -m unittest discover -s tests -v`.

## Настройки

В TOML указываются шесть обязательных полей:

- `package` — имя пакета для анализа;
- `repository` — URL npm registry или путь к учебному JSON;
- `test_mode` — `true` для учебного JSON;
- `output` — путь к будущему SVG;
- `ascii_tree` — показывать ли ASCII-дерево;
- `filter_substring` — исключать пакеты, содержащие эту подстроку.

На первом этапе приложение выводит все настройки и проверяет ошибки.

## Этап 2 — прямые зависимости npm

```powershell
.\run.bat configs\npm.toml
```

Программа обращается к публичному HTTP API реестра npm (`/package/latest`),
из поля `dependencies` получает **прямые runtime-зависимости** и выводит их.
Не используется npm CLI или библиотека для анализа зависимостей.
`devDependencies`, `peerDependencies` и `optionalDependencies` не включаются.
Необходим доступ в интернет. Для текущего этапа анализируется релиз
`latest` каждого npm-пакета.
