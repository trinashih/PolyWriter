# AGENTS.md

## Project

- **Name:** EnglishReWriter
- **Goal:** Build a simple local Python tool that rewrites user-provided text into clear, natural English for everyday engineering and customer communication.

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

## Product Scope

### Version 1

Start with a simple command-line Python script.

Required behavior:

- Ask the user to paste text
- Allow multi-line input
- Send the text to AMD LLM Gateway
- Print the rewritten result
- Keep running until the user exits, if simple to implement
- Support one-shot mode with `-m` / `-message`
- Support formality level with `-t` / `-temperature` from `0` to `5`
- Treat `-t` as formality level, not model sampling temperature
- Default formality level is `3`
- If `-t` is provided without `-m`, apply it in interactive mode too

### Version 2

Optional simple local GUI using `tkinter`:

- Text input box
- Rewrite button
- Output text box
- Copy output button if easy to add

Do not over-engineer. Start with the CLI first.

## AMD LLM Gateway

Use the OpenAI-compatible SDK.

- **Base URL:** `https://llm-api.amd.com/Unified/v1`
- **Default model:** `GPT-5.4`
- **API key env var:** `LLM_GATEWAY_KEY`

Use this client pattern:

```python
import os
from openai import OpenAI

api_key = os.environ["LLM_GATEWAY_KEY"]

client = OpenAI(
    base_url="https://llm-api.amd.com/Unified/v1",
    api_key=api_key,
    default_headers={
        "Ocp-Apim-Subscription-Key": api_key,
    },
)
```

Do not hard-code, print, log, or commit API keys.

## Prompt Guidance

### System Prompt Intent

The assistant should act as a professional engineering communication assistant.

It should:

- Rewrite user-provided English into clear, natural, grammatically correct English
- Keep the tone friendly, concise, and professional
- Avoid marketing, legal, and executive tone
- Preserve technical terms, names, dates, acronyms, and urgency
- Avoid adding facts not present in the original

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

## Coding Guidance

- Use simple, readable Python
- Prefer clarity over cleverness
- Avoid unnecessary frameworks and dependencies
- Use `tkinter` first if a GUI is needed
- Keep files small and easy to understand

Suggested structure:

```text
EnglishReWriter/
  AGENTS.md
  rewrite.py
  gui.py
  README.md
```

## Security and Privacy

- Do not log or print the API key
- Do not store the API key in source files
- Do not commit API keys to git
- Do not send files automatically unless explicitly requested
- Only rewrite text the user directly provides

## Expected Environment

The script should expect:

```powershell
$env:LLM_GATEWAY_KEY="your-api-key"
```

Show a clear error if `LLM_GATEWAY_KEY` is missing.

## Development Guidance for Cline

- Follow this file when working on the project
- Before making large changes, explain the plan first
- Keep the first implementation simple
- Do not create unnecessary architecture
- Do not add web frameworks, databases, or background services unless explicitly requested
- Do not add Jira, Outlook, or Teams integration unless explicitly requested

## First Goal

Take pasted English text and rewrite it using AMD LLM Gateway.