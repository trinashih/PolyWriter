# AGENTS.md

## Project

- **Name:** PolyWriter
- **Goal:** Build a simple local Python tool that rewrites or translates user-provided text into clear, natural language for everyday engineering and customer communication.

## Writing Style

Preferred output should be:

- Natural
- Clear
- Concise
- Friendly
- Professional but not overly formal
- Suitable for engineers, FAEs, customers, vendors, and internal teams
- Not too polished or corporate
- Not marketing-like
- Not legal-like
- Not executive-sounding

Preserve the original meaning, urgency, and technical intent.

## Rewrite Rules

When rewriting:

1. Keep the original meaning.
2. Correct grammar, spelling, and sentence structure.
3. Keep the message natural and human.
4. Preserve technical terms unless correction is clearly needed.
5. Preserve names, ticket numbers, project names, product names, dates, and acronyms.
6. Do not add new facts.
7. Do not make the message overly formal.
8. Do not make it sound like marketing, legal, or executive writing.
9. Do not over-explain.
10. Keep the rewritten version close to the original length unless clarity needs a small change.
11. If the input is already good, make only minimal improvements.
12. If the input is casual, keep it reasonably casual.
13. If the input is customer-facing, polish it slightly but keep it natural.

## Typical Use Cases

- Customer emails
- Internal engineering updates
- Oracle/AMD technical coordination messages
- Escalation notes
- Slack/Teams-style short messages
- Status updates
- Requests for help
- Follow-up messages

## Current Product Scope

The current implementation is a simple command-line Python script:

- `polywriter.py`

Current behavior:

- Ask the user to paste text in interactive mode
- Allow multi-line input
- Submit interactive input with `//` or `/.`
- Exit interactive mode with `/exit`
- Send the text to AMD LLM Gateway
- Print the rewritten or translated result
- Keep running until the user exits
- Support one-shot mode with `-m` / `-message`
- Support formality level with `-t` / `-temperature` from `0` to `5`
- Treat `-t` as formality level, not model sampling temperature
- Default formality level is `3`
- Apply `-t` in interactive mode too when provided without `-m`
- Support target output language with `-l` / `--language`
- Default output language is `English`
- Normalize common language aliases such as English, Japanese, and Chinese
- Default Chinese output to Traditional Chinese
- Support rewrite requests, translation requests, and mixed inline instructions
- Preserve existing emoji when they fit naturally
- Add light emoji only when the user explicitly asks for it
- Try to copy the final result to the clipboard automatically
- Show the application version with `--version`

Possible next step if requested:

- Optional simple local GUI using `tkinter`

Do not over-engineer. Keep the CLI simple and practical first.

## AMD LLM Gateway

Use the OpenAI-compatible SDK.

- **Base URL:** `https://llm-api.amd.com/Unified/v1`
- **Default model:** `GPT-5.4`
- **Current local key source:** `KEY.txt`

Current client pattern:

```python
from openai import OpenAI

api_key = load_api_key()

client = OpenAI(
    base_url="https://llm-api.amd.com/Unified/v1",
    api_key=api_key,
    default_headers={
        "Ocp-Apim-Subscription-Key": api_key,
    },
)
```

Do not hard-code, print, log, or commit API keys.

If the project is later changed to use an environment variable instead of `KEY.txt`, update this file to match the implementation.

## Prompt Guidance

### System Prompt Intent

The assistant should act as a professional engineering communication assistant.

It should:

- Rewrite user-provided English into clear, natural, grammatically correct English
- Translate when the user asks for translation or when the application requests a target output language
- Keep the tone friendly, concise, and professional
- Avoid marketing, legal, and executive tone
- Preserve technical terms, names, dates, acronyms, and urgency
- Avoid adding facts not present in the original
- Follow extra inline instructions when they are clearly part of the user input, such as making the message shorter, more polite, less formal, or translating it

### Emoji Handling

- Preserve emojis already present when they fit naturally
- Do not add emojis by default
- If the user asks for emoji, keep usage light and professional

### Formality Handling

- `0` = very casual
- `1` = casual
- `2` = slightly casual but still professional
- `3` = balanced professional tone for normal engineering communication
- `4` = more polished and formal
- `5` = very formal and polished

The selected level should affect both rewrite and translation output.

### Output Language Handling

- Default output language is `English`
- Support explicit output language selection from the CLI
- Normalize common aliases for English, Japanese, and Chinese
- If the user asks for Chinese, default to Traditional Chinese
- If the requested language is unsupported or unclear, return an English unsupported-language message

## Coding Guidance

- Use simple, readable Python
- Prefer clarity over cleverness
- Avoid unnecessary frameworks and dependencies
- Use `tkinter` first if a GUI is needed
- Keep files small and easy to understand

Suggested structure:

```text
PolyWriter/
  AGENTS.md
  polywriter.py
  README.md
  KEY.txt
```

Keep guidance aligned with the actual repository contents. Do not refer to files that do not exist unless you are proposing a future addition.

## Security and Privacy

- Do not log or print the API key
- Do not store the API key in source files
- Do not commit API keys to git
- Do not send files automatically unless explicitly requested
- Only rewrite text the user directly provides
- Treat `KEY.txt` as a local secret file and keep it out of version control

## Expected Environment

The current script expects a local `KEY.txt` file.

Expected format:

```txt
API_KEY = "your-api-key"
```

Only the value inside the double quotes is used.

Show a clear error if `KEY.txt` is missing or malformed.

## Development Guidance for Cline

- Follow this file when working on the project
- Before making large changes, explain the plan first
- Keep the first implementation simple
- Do not create unnecessary architecture
- Do not add web frameworks, databases, or background services unless explicitly requested
- Do not add Jira, Outlook, or Teams integration unless explicitly requested
- Keep `AGENTS.md`, `README.md`, and the actual code behavior consistent with each other
- When updating guidance, verify it against `polywriter.py` and `README.md` instead of assuming older plans are still current
- Prefer small, direct edits over broad rewrites unless the user asks for a larger restructure

## First Goal

Take pasted text and rewrite or translate it using AMD LLM Gateway in a way that stays natural, clear, and useful for engineering communication.