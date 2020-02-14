# Бот помощник.
Бот помощник службы поддержки для vk/telegram.

## Требования
Python 3.5+ <br>
Установка зависимостей:  
```
pip install -r requirements.txt

```
## создать проект dialogflow
Необходимо в папку проекта добавить файл `google-credentials.json` (https://console.developers.google.com/apis/credentials).


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

