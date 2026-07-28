# AGENTS.md

Project Name:
EnglishReWriter

Goal:
Build a simple local English rewriting tool for engineering and customer communication.

The tool should take user-provided text and rewrite it into clear, grammatically correct, natural English. The tone should be suitable for everyday engineering communication with coworkers, customers, vendors, and cross-functional teams.

This is not a marketing writing tool.
This is not an executive speech writing tool.
The output should sound like a real engineer or FAE communicating clearly and professionally.

User Preference:
The preferred output style is:

- Natural
- Clear
- Concise
- Friendly
- Professional but not overly formal
- Suitable for engineering/customer conversations
- Not too polished
- Not too corporate
- Not too verbose
- Not marketing-like
- Not legal-like
- Not executive-sounding

The rewritten message should preserve the original meaning and urgency.

Common Use Cases:
This tool will be used to rewrite messages such as:

- Customer emails
- Internal engineering updates
- Oracle/AMD technical coordination messages
- Escalation notes
- Slack/Teams-style short messages
- Status updates
- Requests for help
- Follow-up messages
- Polite but direct technical communication

Rewrite Rules:
When rewriting text:

1. Keep the original meaning.
2. Correct grammar, spelling, and sentence structure.
3. Keep the message natural and human.
4. Preserve all technical terms exactly unless correction is clearly needed.
5. Preserve names, ticket numbers, project names, product names, dates, and acronyms.
6. Do not add new facts.
7. Do not make the message sound overly formal.
8. Do not make the message sound like marketing.
9. Do not make the message sound like legal language.
10. Do not make the message sound executive-heavy.
11. Do not over-explain.
12. Do not add unnecessary greetings or closings unless the original text implies them.
13. Keep the rewritten version close to the original length unless clarity requires a small change.
14. If the input is already good, only make minimal grammar or flow improvements.
15. If the input is casual, keep it reasonably casual.
16. If the input is customer-facing, make it polished enough but still natural.

Tone Examples:

Good tone example 1:
Thanks for the update. If the validation testing is not completed today, the first FR may slip, and we may need to postpone the onsite plan to next week.

Good tone example 2:
Could you please help reboot the system and check whether the USB is bootable?

Good tone example 3:
I do not think we need to be onsite today. Have you heard any updates from Shawn?

Good tone example 4:
Thanks for your help. Any idea to support this effort would be appreciated.

Bad tone example 1:
We sincerely appreciate your continued collaboration and would like to formally inquire whether the validation process has reached completion.

Bad tone example 2:
Pursuant to the previously discussed timeline, we may need to reassess the onsite engagement.

Bad tone example 3:
We would like to leverage cross-functional alignment to optimize the stakeholder communication path.

Application Requirements:
Start with a simple Python application.

Version 1 should be a command-line script.

The script should:
- Ask the user to paste text.
- Allow multi-line input.
- Send the text to AMD LLM Gateway.
- Print the rewritten result.
- Keep running until the user exits, if simple to implement.
- Support a quick one-shot mode with `-m` or `-message` followed by the input text.
- In quick one-shot mode, print the LLM result once and exit.
- Support `-t` or `-temperature` followed by a value from `0` to `5`.
- Treat `-t` / `-temperature` as a formality level, not a model sampling temperature.
- Use `3` as the default formality level for normal engineering communication.
- Treat `0` as the most casual option.
- Treat `5` as the most formal option.
- If `-t` is provided without `-m`, keep the normal interactive loop and apply the selected formality level to rewrite or translation output.

Version 2 can be a simple local GUI using tkinter.

The GUI should include:
- Text input box
- Rewrite button
- Output text box
- Copy output button if simple to implement

Do not over-engineer the first version.
Start with rewrite.py first.
Add gui.py only after rewrite.py works.

AMD LLM Gateway:
Use the AMD LLM Gateway through the OpenAI-compatible SDK.

Base URL:
https://llm-api.amd.com/Unified/v1

The API key should be read from an environment variable:
LLM_GATEWAY_KEY

Do not hard-code API keys in source code.

Use this client pattern:

import os
from openai import OpenAI

api_key = os.environ["LLM_GATEWAY_KEY"]

client = OpenAI(
    base_url="https://llm-api.amd.com/Unified/v1",
    api_key=api_key,
    default_headers={
        "Ocp-Apim-Subscription-Key": api_key
    },
)

Default model:
GPT-5.4

If another model is requested, make the model configurable.

Prompt Template:
Use a prompt similar to this:

Rewrite the following message.

Requirements:
- Correct grammar and spelling.
- Make it sound natural and clear.
- Keep it professional but not overly formal.
- Make it suitable for engineering or customer communication.
- Preserve the original meaning.
- Preserve technical terms, names, ticket numbers, project names, dates, and acronyms.
- Do not add new facts.
- Do not make it sound like marketing, legal, or executive writing.
- Keep it concise.
- Preserve emojis that are already present when they fit naturally.
- Do not add emojis unless the user asks for them.
- If the user asks for emoji, use only a small number and keep them natural and professional.
- Apply the selected formality level from `0` to `5` to the rewrite or translation style.

Original message:
{user_text}

System Prompt:
Use a system prompt similar to this:

You are a professional engineering communication assistant.

Your job is to rewrite user-provided English into clear, natural, grammatically correct English.

The preferred tone is:
- Natural
- Friendly
- Concise
- Professional but not overly formal
- Suitable for engineers communicating with customers, vendors, and internal teams

Do not make the message sound like marketing, legal, or executive writing.
Do not add facts that are not in the original message.
Preserve technical terms, names, ticket numbers, project names, dates, and acronyms.
Keep the rewritten message close to the original meaning and urgency.

Emoji handling:
- Preserve emojis that are already in the user's message when they fit naturally.
- Do not remove emojis unless they make the message unclear.
- Do not add emojis by default.
- If the user asks for emoji, you may add a small number of natural, professional emojis.
- Keep emoji use light and suitable for engineering or customer communication.

Formality handling:
- `0` = very casual
- `1` = casual
- `2` = slightly casual but still professional
- `3` = balanced professional tone for normal engineering communication
- `4` = more polished and formal
- `5` = very formal and polished
- The selected level should affect both rewrite and translation output.

Coding Style:
Use simple Python.

Prefer readable code over clever code.
Avoid unnecessary frameworks.
Do not introduce external dependencies unless needed.
If a GUI is needed, use tkinter first because it is built into Python.
Keep files small and easy to understand.

Suggested File Structure:
EnglishReWriter/
  AGENTS.md
  rewrite.py
  gui.py
  README.md

Start with rewrite.py first.
Add gui.py only after the command-line version works.

Security and Privacy:
Do not log the API key.
Do not print the API key.
Do not store the API key in source files.
Do not commit API keys to git.
Do not send files automatically unless the user explicitly asks.
The tool should only rewrite text that the user pastes or provides.

Environment Variable:
The script should expect the user to set:

LLM_GATEWAY_KEY

On Windows PowerShell, the user may set it temporarily with:

$env:LLM_GATEWAY_KEY="your-api-key"

The script should show a clear error if LLM_GATEWAY_KEY is missing.

Expected Behavior:

Quick mode command:
python rewrite.py -m "BTW, is the FR will ship out today?"

Output:
BTW, will the FR ship out today?

Quick mode command with higher formality:
python rewrite.py -m "please help check this issue" -t 5

Interactive mode command with custom formality:
python rewrite.py -t 1

Input:
BTW, is the FR will ship out today?

Output:
BTW, will the FR ship out today?

Input:
No.. I dont think we need to be on site today~ do you hear any upates from Shawn?

Output:
No, I do not think we need to be onsite today. Have you heard any updates from Shawn?

Input:
If the validation testing was not finished in today. The first FR may sleap the schedule and we will pospond the on site plan to next week

Output:
If the validation testing is not completed today, the first FR may slip, and we may need to postpone the onsite plan to next week.

Input:
Alex just drop the CPU to me. Do you want to contact Oracle for the mini rack CPU replacement next Monday or later? BTW, do you mind to remind them to update the bios before we swap the CPUs?

Output:
Alex just dropped off the CPUs for me. Do you want to contact Oracle about the mini rack CPU replacement next Monday or later? Also, could you remind them to update the BIOS before we swap the CPUs?

Input:
looking good but need Song or someone help to reboot the system and see if the USB is bootable or not

Output:
Looks good, but we need Song or someone else to help reboot the system and check whether the USB is bootable.

Input:
Thank you Bernice. Hi Mahesh, let's have a lunch some time. Steven and I can go to pick up the thumb drives. Thank you.

Output:
Thank you, Bernice. Hi Mahesh, let’s have lunch sometime. Steven and I can stop by to pick up the thumb drives. Thanks.

Development Guidance for Cline:
When working on this project, follow AGENTS.md carefully.

Before making large changes, explain the plan first.
Keep the first implementation simple.
Do not create unnecessary architecture.
Do not add web frameworks.
Do not add database support.
Do not add background services.
Do not add Jira, Outlook, or Teams integration in this project unless explicitly requested.

The first goal is only:
Take pasted English text and rewrite it using AMD LLM Gateway.

Recommended First Cline Prompt:
Read AGENTS.md and create the first version of this project. Start with rewrite.py only. Use AMD LLM Gateway with the OpenAI-compatible SDK. Do not hard-code the API key. Read it from LLM_GATEWAY_KEY. Keep the implementation simple and show me the file plan before coding.