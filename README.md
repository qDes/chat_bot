# Бот помощник.
Бот помощник службы поддержки для vk/telegram.

## Требования
Python 3.5+ <br>
Установка зависимостей:  
```
pip install -r requirements.txt

```
Бот работает с использованием dialogflow.
## Настройка dialogflow

Создать проект в [DialogFlow](https://cloud.google.com/dialogflow/docs/quick/setup).<br>
В папку проекта добавить json-ключ в файл `google-credentials.json` (https://console.developers.google.com/apis/credentials).

Для обучения бота поместите фразы в файл 'questions.json' с следующей структурой и запустите `python3 dialog.py`:
```json
    "%title%": {
        "questions": [
            "%question1%",
            "%question2%",
        ],
        "answer": "%answer%"
    },
```
Например:
```json
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
```
### Переменные окружения
Для запуска необходимо указать переменные окружения в файле `.env`:

`TG_TOKEN` = %token% - токен вашего телеграм бота <br>
`TELEGRAM_CHAT_ID` = %chat_id% - ваш телеграм ID <br>
`VK_TOKEN` = %token% - токен вашего вк бота <br>
`GOOGLE_PROJECT_ID` = %project_id% - ID google проекта с dialogflow <br>

## Обучение 

## Использование
Запуск ботов:
```
python3 tg_bot.py
python3 vk_bot.py
```

