---
title: Notebook
author: codex
description: Notes from voice recordings and photographs, newest first.
order: 2
step: 2
subtitle: Your work
tool: /dictate
tool_title: Dictate a note
tools:
  - href: /dictate
    title: Dictate a note
    copy: Talk; get a cleaned-up note.
  - href: /transcribe
    title: Transcribe photos
    copy: Photograph pages; get a faithful transcription.
list_heading: Your notes
---

# Notebook

[Dictate a note](/dictate) or [transcribe photographs](/transcribe). Both save Markdown documents here, with the newest entries listed first. Edit them like any other Markdown file; new captures never overwrite an existing note.

Dictated notes include a cleaned-up transcript. Photographed notes preserve the writing and mark unclear words; their source photographs appear below the transcription so you can check it.

The Markdown lives in `notebook/` at the root of the repo, and anything else you add there (notes, drafts, sources) is a page too. Audio and raw transcripts stay in `_media/dictation/`; photographs and their transcription records stay in `_media/notebook/`. Those media folders are local and gitignored.
