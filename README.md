# NeoRef (Telegram bot)

*Neureal Reference*. Бот для Telegram, написанный на Python 3.11.4 (aiogram3). Используется для взаимодействия с ChatGPT через OpenAI API ключ. Язык интерфейса: **Русский**.

## Ограничение доступа

### Описание

Аккаунты, имеющие доступ к боту, разделяются на две категории:

* Администраторы. Могут добавлять и удалять администраторов и пользователей. Имеют функционал пользователей;

* Пользователи. Имеют возможность отправлять запросы к модели ChatGPT.

### Добавление администраторов и пользователей

Новый Telegram ID может быть добавлен в одну из двух категорий с помощью следующих способов:

* Администраторами через **команды бота** (см. раздел <u>Команды</u>)

* Хостером с помощью консольной утилиты **access_editor.py** (см. раздел <u>Консольная утилита для управления доступом</u>)

### Консольная утилита для управления доступом

Консольная утилита **access_editor.py** поставляется вместе с открытым исходным кодом NeoRefBot. Перед сохранением она преобразовывает Telegram ID из соображений приватности. (см. раздел <u>Приватность</u>). Ниже приведена таблица с командами к данному программному обеспечению:

| Аргумент         | Назначение                               | Ожидаемые значения | Пример команды                |
| ---------------- | ---------------------------------------- | ------------------ | ----------------------------- |
| -aa, --add-admin | Добавление администратора                | Telegram ID        | py access_editor.py -aa 12345 |
| -au, --add-user  | Добавление пользователя                  | Telegram ID        | py access_editor.py -au 12345 |
| -d, ---delete    | Удаление пользователя или администратора | Telegram ID        | py access_editor.py -d 12345  |

## Команды

NeorefBot обладает следующими командами внутри Telegram:

| Команда    | Назначение                                                           |
| ---------- | -------------------------------------------------------------------- |
| /start     | Запустить бота                                                       |
| /help      | Отобразить справку                                                   |
| /remember  | Начать сохранять контекст                                            |
| /forget    | Перестать сохранять контекст                                         |
| /clear     | Очистить контекст                                                    |
| /addadmin  | Добавить администратора<u> (для администраторов)</u>                 |
| /adduser   | Добавить пользователя <u>(для администраторов)</u>                   |
| /delaccess | Удалить пользователя или администратора <u>(для администраторов)</u> |

## Размещение

Для запуска NeoRefBot на локальной машине требуется создать файлы **.env** и **config.yaml**. Ниже указаны поля, значения которых должны быть сохранены в данных файлах. Редактирование списка администраторов и пользователей выполнять вручную **<u>не рекомендуется</u>**.

| Переменная         | Расположение | Назначение                                                                  |
| ------------------ | ------------ | --------------------------------------------------------------------------- |
| TELEGRAM_TOKEN     | .env         | Токен для доступа к Вашему боту в Telegram                                  |
| OPENAI_API_KEY     | .env         | Ключ API для доступа к модели ChatGPT                                       |
| admin_ids          | config.yaml  | Список Telegram ID администраторов (в виде хэша <u>Argon2id</u>)            |
| user_ids           | config.yaml  | Список Telegram ID пользователей (в виде хэша <u>Argon2id</u>)              |
| chat_check_timeout | config.yaml  | Максимальное время проверки модели при запуске бота                         |
| chat_ask_timeout   | config.yaml  | Максимальное время получения ответа от модели при запросе пользователя      |
| chat_model         | config.yaml  | Модель ChatGPT                                                              |
| chat_max_tokens    | config.yaml  | Максимальное количество токенов, которые могут быть задействованы в запросе |

## Приватность

Для предотвращения утечки Telegram ID администраторов и пользователей эти данные сохраняются в виде хэшей, полученных по протоколу **Argon2id**.


