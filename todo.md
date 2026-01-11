- виправляємо неймінг файлів
- просимо знайти інші пропозиціє для оптимізації
- переходимо на UV
- перевіряємо запуск тестів
- підключаємо лінтер ruff, яка різниця PyCharm

# pip:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# uv

uv venv
uv pip install -r requirements.txt

# або ще простіше з pyproject.toml

uv sync