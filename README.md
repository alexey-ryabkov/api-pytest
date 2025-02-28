# Итоговая работа по курсу "Тестирование. Проектирование тестов" в ITHub

В рамках итоговой работы протестирован REST API [Petstore](https://petstore.swagger.io/).

## Подготовка и запуск тестов

Для развертывания проекта в системе должен быть установлен Python 3

### Развертывание окружения

Выполнить последовательно
```bash
python3 -m venv api-pytest
source api-pytest/bin/activate
pip install -r requirements.txt
```

### Запуск тестов

```bash
# запустить все тесты
pytest 
# запустить тест конкретной сущности
python -m pytest test_pet.py 
# запуск тестов с генерацией отчета (должен быть установлен Allure)
pytest --alluredir=allure_results && allure generate allure_results -o report --clean
```

## Отчет 

Отчет сгенерирован с помощью Allure, см. по [этой ссылке](https://alexey-ryabkov.github.io/api-pytest/report/)

## Диаграмма сущностей и связей

![Диаграмма сущностей и связей](/docs/petstore.png)
