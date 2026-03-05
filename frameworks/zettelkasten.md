# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is an Obsidian vault structured as a Zettelkasten general-purpose knowledge base. Notes are atomic, interlinked units of knowledge — not hierarchical documentation.

## Zettelkasten Principles

- **Atomic notes**: each note covers exactly one idea or concept
- **Permanent notes** (Zettels): processed, rewritten in your own words, linked to other notes
- **Literature notes**: temporary summaries of sources, kept in `Sources/`
- **Index/Map of Content (MOC) notes**: navigational hubs that link to clusters of related notes, kept in `MOCs/`
- **Fleeting notes**: quick captures, kept in `Inbox/` to be processed later

## Vault Structure (intended)

```
Inbox/          ← unprocessed fleeting notes
Sources/        ← literature notes (man pages, articles, books)
MOCs/           ← Maps of Content (e.g., "MOC - Shell Scripting")
<topic>/        ← permanent notes grouped loosely by topic
CLAUDE.md
```

## Note Conventions

**File naming**: русские названия без дефисов, описательные и конкретные.
- Хорошо: `Эффект Зейгарника.md`, `Структура юнит файла systemd.md`
- Плохо: `notes1.md`, `effekt-zeygarnik.md`

**Frontmatter** (YAML at top of each permanent note):
```yaml
---
tags: [topic, subtopic]
created: YYYY-MM-DD
source: "optional - URL or book title"
---
```

**Wikilinks**: вписывать ссылки прямо в текст как живое слово — `[[Эффект Зейгарника|зейгарник]]`. Никаких отдельных секций "Связи" в конце заметок. Не ссылаться на одну заметку несколько раз.

**Tags**: lowercase, singular where possible (`bash`, `networking`, `kernel`, not `Bash`, `Networks`, `kernels`).

## Working with This Vault

- When creating a new note, place fleeting/unprocessed content in `Inbox/`
- When asked to research or document a topic, create an atomic permanent note in the appropriate topic folder and link it from a relevant MOC
- When a topic grows beyond ~5 notes, suggest or create a MOC for it
- Do not duplicate content — link to existing notes instead
- Delete `Welcome.md` when the vault has real content

## AI Outbox

Папка `AI Outbox/` — место для результатов исследований, которые я провожу по запросу пользователя.

**Когда создавать заметку в AI Outbox:**
- Пользователь просит исследовать тему, концепцию, заметку или объект
- Задача подразумевает поиск, анализ, сравнение или синтез информации

**Структура заметки-исследования:**
```yaml
---
tags: [ai-research, <тематический тег>]
created: YYYY-MM-DD
source: "[[Исходная заметка или объект запроса]]"
---
```

- Первый абзац — что было задано для исследования и почему
- Основной текст — результаты: что нашёл, что проанализировал, выводы
- Ссылки на источники и заметки vault вписываются в текст как wikilinks
- Заметка **обязательно ссылается на источник запроса** — ту заметку или объект, с которого пришёл запрос (`[[название заметки]]` в поле `source:` и в тексте)
- Если в ходе исследования создаются новые постоянные заметки — они линкуются из этой заметки

**Именование**: по теме исследования, по-русски, без дефисов. Например: `Исследование эффекта якоря в переговорах.md`.

## Transcriptions

Whenever a transcription is produced (Instagram, YouTube, or any other source), **always** save it as a fleeting note in `Inbox/` using the Write tool. Do not just print the text — saving to Inbox is mandatory.

Format:
```yaml
---
tags: [transcription, <тематический тег по содержанию>]
created: YYYY-MM-DD
source: "<URL источника>"
---

<текст транскрипции>
```

File naming: Russian, no dashes, descriptive based on the content — e.g. `Хак поиска бизнес идей через консалтинг.md`.
