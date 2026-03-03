---
name: instagram-transcribe
description: Transcribe audio from an Instagram video (reel, post, story). Downloads video, extracts audio, uploads to Yandex Object Storage, and transcribes via Yandex SpeechKit async API.
argument-hint: <instagram-url>
---

Transcribe audio from Instagram URL: $ARGUMENTS

Credentials are read from environment variables set in `~/.bashrc`:
- `YANDEX_API_KEY` — API-ключ сервисного аккаунта (для SpeechKit)
- `YANDEX_KEY_ID` — статический ключ доступа (для Object Storage)
- `YANDEX_SECRET` — секретный ключ (для Object Storage)
- `YANDEX_BUCKET` — имя бакета

Setup instructions: see `SETUP.md` in this skill's directory.

Follow these steps exactly:

## Step 1 — Download audio

```bash
TMPDIR=$(mktemp -d)
yt-dlp --no-playlist -x --audio-format mp3 --audio-quality 0 \
  -o "$TMPDIR/audio.%(ext)s" "$URL"
AUDIO="$TMPDIR/audio.mp3"
```

If yt-dlp fails with an auth error, Instagram may require login cookies. Inform the user.

## Step 2 — Upload to Yandex Object Storage

```bash
FILENAME="transcribe-$(date +%s).mp3"
AWS_ACCESS_KEY_ID="$YANDEX_KEY_ID" \
AWS_SECRET_ACCESS_KEY="$YANDEX_SECRET" \
aws s3 cp "$AUDIO" "s3://$YANDEX_BUCKET/$FILENAME" \
  --endpoint-url=https://storage.yandexcloud.net
```

## Step 3 — Send async transcription request

```bash
RESPONSE=$(curl -s -4 -X POST \
  -H "Authorization: Api-Key $YANDEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"config\": {
      \"specification\": {
        \"languageCode\": \"ru-RU\",
        \"model\": \"general\",
        \"audioEncoding\": \"MP3\",
        \"literature_text\": true
      }
    },
    \"audio\": {
      \"uri\": \"https://storage.yandexcloud.net/$YANDEX_BUCKET/$FILENAME\"
    }
  }" \
  https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize)

OPERATION_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "Operation ID: $OPERATION_ID"
```

## Step 4 — Poll for result

Check every 5 seconds until `done: true`:

```bash
while true; do
  RESULT=$(curl -s -4 \
    -H "Authorization: Api-Key $YANDEX_API_KEY" \
    "https://operation.api.cloud.yandex.net/operations/$OPERATION_ID")
  DONE=$(echo $RESULT | python3 -c "import sys,json; print(json.load(sys.stdin).get('done', False))")
  if [ "$DONE" = "True" ]; then
    break
  fi
  echo "Ждём..."
  sleep 5
done
```

## Step 5 — Extract and print transcription

```bash
echo $RESULT | python3 -c "
import sys, json
data = json.load(sys.stdin)
chunks = data['response']['chunks']
text = ' '.join(alt['text'] for chunk in chunks for alt in chunk['alternatives'][:1])
print(text)
"
```

## Step 6 — Cleanup

```bash
rm -rf "$TMPDIR"
```

Note: файл в Object Storage удалится автоматически через 1 день по lifecycle policy.

**ВАЖНО:** При создании нового бакета для этого скилла — сразу устанавливать lifecycle policy: префикс `transcribe-`, срок истечения **1 день**. Без этого файлы будут накапливаться.

## Notes
- languageCode: `ru-RU` по умолчанию. Если видео на другом языке — укажи пользователю, что можно поменять на `en-US` и т.д.
- Если yt-dlp не может скачать (приватный аккаунт) — сообщи пользователю
- Бакет используется как временное хранилище, файл удаляется через 1 день автоматически
