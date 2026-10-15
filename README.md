# Lesson Motion Studio

A reusable educational video skill for whiteboard animation in Arabic or English

## Features

- Intake covering age or grade country learning goal duration language and landscape or portrait orientation
- Cairo typography with Arabic RTL and English LTR
- Detailed whiteboard illustrations with progressive pen writing circles arrows and highlighting
- Age appropriate explanations and country sensitive examples
- Google AI Studio narration handoff: a timed script for the user, then scene timing aligned to the returned audio, plus a retrieval question with a thinking interval
- MP4 delivery and explicit quality checks

## Contents

The editable source of truth is in [`skills/lesson-motion-studio`](skills/lesson-motion-studio)
It includes `SKILL.md` references Cairo fonts with their OFL license and timeline validation and encoding scripts

## Requirements

Use an assistant environment that supports skills image generation and local code execution
The user generates the narration in Google AI Studio and returns the audio file
The bundled scripts require Python Pillow ffmpeg and ffprobe
This is an assistant workflow with validation and encoding helpers rather than a standalone automatic video renderer
The host environment selects and implements the scene rendering tools

## Use

Load or install `skills/lesson-motion-studio` using the skill mechanism supported by your assistant
Then provide the lesson topic or screenshot and answer any missing intake questions
The assistant supplies a narration script with target timestamps and a ready-to-paste Google AI Studio prompt; generate the audio there and return the WAV or MP3 file so the assistant can align and finish the MP4
The target timestamps are estimates until the returned recording is measured
Do not treat unperformed listening or visual checks as passed

## Edit and update

Edit files directly in `skills/lesson-motion-studio` using GitHub's file editor or clone this repository locally

```bash
git clone https://github.com/shariefabdelmonem-netizen/lesson-motion-studio.git
cd lesson-motion-studio
```

Commit source changes normally and use `git pull` to retrieve updates
No re-zipping or re-uploading is needed for future edits

The root `lesson-motion-studio.zip` is an optional original snapshot and is not automatically updated
Use the source folder for the current version
GitHub's Code → Download ZIP downloads the current repository including its source files
