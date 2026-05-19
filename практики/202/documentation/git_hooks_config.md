# Конфигурация Git Hooks (pre-commit)

## Установленные хуки

| Хук | Источник | Что делает | Почему полезен |
| --- | -------- | ---------- | -------------- |
| `black` | psf/black | Автоформатирует Python-код | Единый стиль кода без споров в ревью |
| `flake8` | pycqa/flake8 | Проверяет PEP8, неиспользуемые импорты, сложность | Ловит очевидные ошибки до пуша |
| `detect-secrets` | Yelp/detect-secrets | Ищет токены, пароли, ключи в коде | Предотвращает случайный коммит секретов |
| `check-yaml` | pre-commit-hooks | Валидирует синтаксис YAML-файлов | Битый `ci.yml` не сломает пайплайн |
| `check-json` | pre-commit-hooks | Валидирует синтаксис JSON-файлов | Ловит забытые запятые и кавычки |
| `trailing-whitespace` | pre-commit-hooks | Удаляет пробелы в конце строк | Чистые диффы в PR |
| `end-of-file-fixer` | pre-commit-hooks | Добавляет перенос строки в конец файла | Соответствие POSIX-стандарту |

## Настройка окружения для новых контрибьюторов

```bash
# 1. Клонировать репозиторий
git clone https://github.com/MrLobotomist/special-barnacle.git
cd special-barnacle

# 2. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Установить pre-commit хуки
pip install pre-commit
pre-commit install

# 5. Проверить, что всё работает
pre-commit run --all-files
```

После `pre-commit install` хуки будут запускаться автоматически при каждом `git commit`. Если хук упал — коммит не создаётся.

## Лог `pre-commit run --all-files`

```text
(.venv) (base) PS D:\PI\2\project> pre-commit run --all-files
black....................................................................Passed
flake8...................................................................Passed
Detect secrets...........................................................Passed
check yaml...............................................................Passed
check json...........................................(no files to check)Skipped
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
```
