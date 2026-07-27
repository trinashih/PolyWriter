# PolyWriter

PolyWriter is a simple local Python tool for rewriting and translating messages for everyday engineering communication.

It is designed for practical use in messages such as:
- customer emails
- internal engineering updates
- short Slack or Teams messages
- status updates
- follow-up notes
- technical coordination messages

The output style is intended to be:
- natural
- clear
- concise
- friendly
- professional but not overly formal


## Current Version

This version is a simple command-line script:

- `rewrite.py`

It can:
- rewrite English text
- adjust tone based on your instructions
- translate when you ask for it
- accept multi-line input
- keep running until you exit


## Requirements

- Python 3.9+ recommended
- `openai` Python package installed
- AMD LLM Gateway access


## Install Dependency

Install the OpenAI-compatible SDK:

```bash
pip install openai
```


## API Key Setup

This project reads the API key from `KEY.txt`.

Expected format:

```txt
API_KEY = "your-api-key-here"
```

Only the value inside the double quotes is used.


## Run the Tool

From the project folder, run:

```bash
python rewrite.py
```


## How Input Works

When the script starts:

1. Paste your text
2. Press **Enter on an empty line** to submit
3. Type `/exit` on a new line to quit

The script will show:

```text
Waiting for LLM response...
```

while it is waiting for the AMD LLM Gateway reply.


## Example Usage

### Basic rewrite

Input:

```text
BTW, is the FR will ship out today?
```

Possible output:

```text
BTW, will the FR ship out today?
```


### Rewrite with tone instruction

Input:

```text
please help check this issue (make it more formal)
```


### Rewrite with less formal tone

Input:

```text
No.. I dont think we need to be on site today~ do you hear any upates from Shawn? (make it less formal)
```


### Translate to English

Input:

```text
幫我翻成英文：今天我們會晚一點提供更新
```


### Translate to Japanese

Input:

```text
Translate this to Japanese: please help reboot the system and check whether the USB is bootable.
```


### Rewrite and shorten

Input:

```text
Rewrite this and make it shorter: Thanks for your help, we may need to postpone the onsite plan to next week.
```


## Notes

- The tool is intended for engineering and customer communication.
- It is not intended for marketing writing.
- It is not intended for legal writing.
- It is not intended for executive-style writing.
- Technical terms, names, ticket numbers, project names, dates, and acronyms should be preserved.


## Current Files

- `rewrite.py` - command-line rewriting and translation tool
- `KEY.txt` - local API key file
- `README.md` - project usage guide


## Future Ideas

Possible next steps if needed:
- a simple local GUI with `tkinter`
- copy-to-clipboard support
- clearer output labels such as `Result:` instead of `Rewritten message:`
