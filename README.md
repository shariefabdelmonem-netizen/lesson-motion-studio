# Lesson Motion Studio

Reusable educational video skill for whiteboard animation in Arabic or English

## Download and use

Download `lesson-motion-studio.zip` from this repository and extract it
The archive contains the complete `lesson-motion-studio` skill folder
Load that folder with the skill mechanism supported by your assistant environment
Then provide the lesson topic or screenshot and answer the missing intake questions

## Features

- Grade or age country learning goal duration language and video orientation intake
- Arabic or English narration and age appropriate explanations
- Landscape 16:9 or portrait 9:16
- Cairo typography with correct Arabic RTL and English LTR
- Whiteboard illustrations and progressive pen writing
- Circles arrows and highlighting tied to the explanation
- Social and cultural adaptation based on the country without stereotypes
- Retrieval question with a thinking interval before the answer
- MP4 export and explicit content visual audio and timing checks

## Archive contents

- SKILL.md with the full workflow instructions
- agents/openai.yaml
- references/style-and-subjects.md
- references/timeline.md
- references/whiteboard.md
- scripts/validate_timeline.py
- scripts/encode_video.py
- Cairo fonts with their Open Font License
- Skill icon

## Requirements and limits

Use an assistant environment supporting skills image generation speech generation and local code execution
The helper scripts require Python Pillow ffmpeg and ffprobe
This is an assistant workflow with validation and encoding helpers rather than a standalone automatic video renderer
The host environment implements scene rendering and chooses available media tools
Do not treat unperformed full listening or motion review as passed

The bundled Cairo font license applies to those fonts
