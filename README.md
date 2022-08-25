# Get-salary

Это программа, которая выводит среднюю зарплату по популярным языкам программирования с двух сервисов - [HeadHunter](https://hh.ru/) и [SuperJob](https://www.superjob.ru).

### Как установить

1. Создайте файл .env и добавьте токен, полученный из [SuperJob](https://www.superjob.ru). Вот пример:
```
SJ_TOKEN = v3.r.00000.example_token
```

2. Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```powershell
pip install -r requirements.txt
```

### Как запустить

Запустить код можно с помощью команды:
```powershell
python .\get-salary.py
```
В терминале появятся 2 таблички. В одной из них будет информация о вакансиях с HeadHunter, а в другой - с SuperJob.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
 
