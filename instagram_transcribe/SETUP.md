# SETUP — instagram-transcribe skill

Created: 2026-02-26

Пошаговая инструкция для настройки скилла транскрибации Instagram видео через Yandex SpeechKit.

---

## Требования

- Ubuntu/Debian Linux
- `sudo` доступ

---

## Шаг 1 — Установить системные зависимости

```bash
sudo apt install ffmpeg awscli
```

Убедиться что `yt-dlp` установлен:

```bash
which yt-dlp || pip install yt-dlp
```

---

## Шаг 2 — Создать аккаунт в Яндекс Облаке

Зарегистрироваться: https://console.yandex.cloud

После входа найти **Folder ID** своего каталога:
- Кликнуть на название каталога вверху слева
- Скопировать **Идентификатор каталога** (формат: `b1g...`)

---

## Шаг 3 — Создать сервисный аккаунт

Прямая ссылка (подставить свой FOLDER_ID):
```
https://console.yandex.cloud/folders/FOLDER_ID/iam/service-accounts/create
```

- Имя: `speechkit-bot` (или любое)
- Роли: `ai.speechkit-stt.user` и `storage.uploader`

Сохрани **ID сервисного аккаунта** (формат: `aje...`).

---

## Шаг 4 — Создать API-ключ сервисного аккаунта

Прямая ссылка (подставить FOLDER_ID и SERVICE_ACCOUNT_ID):
```
https://console.yandex.cloud/folders/FOLDER_ID/iam/service-accounts/SERVICE_ACCOUNT_ID
```

- Вкладка **API-ключи** → **Создать**
- Область действия: `yandex-cloud`
- Скопировать **секретный ключ** — показывается только один раз

---

## Шаг 5 — Создать статические ключи доступа (для Object Storage)

На той же странице сервисного аккаунта:
- Вкладка **Статические ключи доступа** → **Создать**
- Скопировать **Идентификатор ключа** и **Секретный ключ** — оба сразу

---

## Шаг 6 — Создать Object Storage бакет

Прямая ссылка (подставить FOLDER_ID):
```
https://console.yandex.cloud/folders/FOLDER_ID/storage/create
```

- Имя: любое (латиница, цифры, дефис — например `speechkit-audio`)
- Доступ: **Приватный**
- Остальное по умолчанию

---

## Шаг 7 — Установить lifecycle policy на бакете

**ВАЖНО:** сделать сразу после создания бакета, иначе файлы будут накапливаться.

Прямая ссылка (подставить FOLDER_ID и BUCKET_NAME):
```
https://console.yandex.cloud/folders/FOLDER_ID/storage/buckets/BUCKET_NAME
```

- Вкладка **Жизненный цикл** → **Добавить правило**
- Префикс: `transcribe-`
- Истечение срока: **1 день**
- Сохранить

---

## Шаг 8 — Сохранить переменные окружения

Добавить в `~/.bashrc` (заменить значения в угловых скобках на свои):

```bash
# Yandex Cloud SpeechKit
export YANDEX_API_KEY="<секретный API-ключ из шага 4>"
export YANDEX_FOLDER_ID="<Folder ID из шага 2>"
export YANDEX_KEY_ID="<Идентификатор ключа из шага 5>"
export YANDEX_SECRET="<Секретный ключ из шага 5>"
export YANDEX_BUCKET="<имя бакета из шага 6>"
```

Применить:
```bash
source ~/.bashrc
```

---

## Шаг 9 — Проверить подключение

```bash
AWS_ACCESS_KEY_ID="$YANDEX_KEY_ID" \
AWS_SECRET_ACCESS_KEY="$YANDEX_SECRET" \
aws s3 ls s3://$YANDEX_BUCKET --endpoint-url=https://storage.yandexcloud.net
```

Пустой вывод без ошибок = всё работает.

---

## Готово

Теперь можно использовать скилл:
```
/instagram-transcribe https://www.instagram.com/reel/...
```
