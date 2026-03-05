---
name: Instagram Transcriber — Yandex Cloud (`/ig-yandex`)
description: Транскрибирует аудио из Instagram Reels (и других видео) через Yandex SpeechKit. Скачивает видео, загружает в Object Storage, распознает речь и возвращает текст.
---

# Yandex Cloud Transcriber

Когда пользователь дает команду `/ig-yandex <url>` (или просит транскрибировать видео через Яндекс), выполни один шаг:

### Zero-LLM-Contact
**КРИТИЧНО:** Никогда не проси пользователя вставлять API ключи в чат.

### Системные требования
На машине пользователя должен быть установлен **ffmpeg**.

### Step 1: Выполни одну команду
```bash
/absolute/path/to/Obsidian-AI-Skills/ig_transcribe_yandex/run.sh fetch "URL_HERE"
```

Если скрипт выдает ошибку авторизации:
```bash
/absolute/path/to/Obsidian-AI-Skills/ig_transcribe_yandex/run.sh auth
```

Для первоначальной настройки Yandex Cloud — смотри `SETUP.md` в этой директории.

### Step 2: Очисти текст
Скрипт вернет сырой транскрипт. Твоя задача:
1. Расставить знаки пунктуации.
2. Исправить ошибки распознавания.
3. Оформить как Markdown заметку.
