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
- preserve emoji naturally
- add light emoji when you explicitly ask for it
- run once from the command line with `-m` or `-message`
- adjust rewrite formality with `-t` or `-temperature`
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

To see command-line help:

```bash
python rewrite.py -h
```

Quick one-shot mode:

```bash
python rewrite.py -m "BTW, is the FR will ship out today?"
```

With formality level:

```bash
python rewrite.py -m "please help check this issue" -t 5
```

Formality level range:

- `0` = most casual
- `3` = default / normal engineering communication
- `5` = most formal

If you do not provide `-m` or `-message`, the script keeps the current interactive loop behavior.
If you provide `-t` without `-m`, the selected formality level still applies to the interactive rewrite results.


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


### Quick one-shot rewrite

Command:

```bash
python rewrite.py -m "No.. I dont think we need to be on site today~ do you hear any upates from Shawn?"
```


### Quick one-shot rewrite with higher formality

Command:

```bash
python rewrite.py -m "please help check this issue" -t 5
```


### Interactive mode with custom formality

Command:

```bash
python rewrite.py -t 1
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


### Rewrite with emoji

Input:

```text
Please rewrite with emoji: thanks for your help, we finished the validation today
```


### Preserve existing emoji

Input:

```text
thanks for the update 🙂 we may need to move the onsite plan to next week
```


## Notes

- The tool is intended for engineering and customer communication.
- It is not intended for marketing writing.
- It is not intended for legal writing.
- It is not intended for executive-style writing.
- Technical terms, names, ticket numbers, project names, dates, and acronyms should be preserved.
- Emoji are preserved when they fit naturally.
- Emoji are not added by default unless you ask for them.
- When requested, emoji use should stay light and professional.
- `-t` and `-temperature` are treated as a formality level from 0 to 5.
- If `-m` or `-message` is provided, the script prints one result and exits.


## Current Files

- `rewrite.py` - command-line rewriting and translation tool
- `KEY.txt` - local API key file
- `README.md` - project usage guide


## Future Ideas

Possible next steps if needed:
- a simple local GUI with `tkinter`
- copy-to-clipboard support
- clearer output labels such as `Result:` instead of `Rewritten message:`
