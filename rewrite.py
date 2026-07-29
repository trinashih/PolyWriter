import argparse
import re

from openai import OpenAI


BASE_URL = "https://llm-api.amd.com/Unified/v1"
DEFAULT_MODEL = "GPT-5.4"
KEY_FILE = "KEY.txt"
DEFAULT_FORMALITY_LEVEL = 3

SYSTEM_PROMPT = """You are a professional engineering communication assistant.

Your job is to help with rewriting and translation for engineering communication.

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

The user may include extra instructions in the same input, such as:
- make it more formal
- make it less formal
- make it shorter
- make it more polite
- translate to Japanese
- translate to English

If the user includes those instructions, follow them.
If the user asks for translation, translate the message to the requested language.
If the user asks for rewriting only, rewrite it.
If the user input already contains both the message and the instruction together, interpret it naturally.

Emoji handling:
- Preserve emojis that are already in the user's message when they fit naturally.
- Do not remove emojis unless they make the message unclear.
- Do not add emojis by default.
- If the user asks for emoji, you may add a small number of natural, professional emojis.
- Keep emoji use light and suitable for engineering or customer communication.
"""


def get_formality_instruction(level: int) -> str:
    if level <= 0:
        return "Use a very casual, relaxed tone while still keeping the message clear."
    if level == 1:
        return "Use a casual and natural tone."
    if level == 2:
        return "Use a slightly casual but still professional tone."
    if level == 3:
        return "Use a balanced professional tone suitable for normal engineering communication."
    if level == 4:
        return "Use a more polished and formal professional tone without sounding stiff."
    return "Use a very formal and polished professional tone suitable for sensitive customer-facing communication."


def build_user_prompt(user_text: str, formality_level: int = DEFAULT_FORMALITY_LEVEL) -> str:
    return f"""Rewrite the following message.

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
- If the user includes extra instructions such as tone, formality, brevity, politeness, or translation, follow them.
- The user may put those instructions in parentheses or inline in the message.
- Preserve emojis that are already present if they fit naturally.
- Do not add emojis unless the user asks for them.
- If the user asks for emoji, use only a small number and keep them natural and professional.
- Formality level: {formality_level} out of 5.
- {get_formality_instruction(formality_level)}

User input:
{user_text}
"""


def load_api_key() -> str:
    try:
        with open(KEY_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
    except FileNotFoundError as error:
        raise RuntimeError("Missing KEY.txt.") from error

    match = re.search(r'"([^"]+)"', content)
    if match:
        return match.group(1).strip()

    raise RuntimeError('Could not find an API key inside quotes in KEY.txt.')


def create_client() -> OpenAI:
    api_key = load_api_key()

    return OpenAI(
        base_url=BASE_URL,
        api_key=api_key,
        default_headers={"Ocp-Apim-Subscription-Key": api_key},
    )


def rewrite_text(
    client: OpenAI,
    user_text: str,
    model: str = DEFAULT_MODEL,
    formality_level: int = DEFAULT_FORMALITY_LEVEL,
) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(user_text, formality_level=formality_level),
            },
        ],
    )
    content = response.choices[0].message.content or ""
    return normalize_output_text(content)


def normalize_output_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()

    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    normalized = re.sub(r"([^\n])\n([\U00010000-\U0010ffff])", r"\1 \2", normalized)
    normalized = re.sub(r"([\U00010000-\U0010ffff])\n([^\n])", r"\1 \2", normalized)

    return normalized


def format_rewrite_error(error: Exception) -> str:
    message = str(error)
    if "401" in message or "invalid subscription key" in message.lower():
        return (
            "Rewrite failed: the AMD LLM Gateway rejected the API key. "
            "Please check that KEY.txt contains a valid active gateway key."
        )
    return f"Rewrite failed: {error}"


def read_multiline_input() -> str:
    print("Paste your text below.")
    print("Type // or /. on a new line to submit.")
    print("Type /exit on a new line to quit.")
    print("/send and /done also work.")
    print("Blank lines will be kept in your message.")

    lines = []
    while True:
        line = input()
        command = line.strip()

        if not lines and command == "/exit":
            return "/exit"

        if command in {"//", "/.", "/send", "/done"}:
            break

        lines.append(line)

    return "\n".join(lines).strip()


def print_exit_message() -> None:
    print("\nGoodbye.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Rewrite or translate engineering communication text. "
            "Use -m for one-shot mode, or run without -m for interactive mode."
        ),
        epilog=(
            "Examples: python rewrite.py -m \"please help check this issue\" | "
            "python rewrite.py -m \"please help check this issue\" -t 5 | "
            "python rewrite.py -t 1"
        ),
    )
    parser.add_argument(
        "-m",
        "-message",
        dest="message",
        help="Run once with the provided message, print the result, and exit.",
    )
    parser.add_argument(
        "-t",
        "-temperature",
        dest="formality_level",
        type=int,
        default=DEFAULT_FORMALITY_LEVEL,
        help="Formality level from 0 to 5. 0 is most casual, 3 is default, 5 is most formal.",
    )

    args = parser.parse_args()

    if not 0 <= args.formality_level <= 5:
        parser.error("-t / -temperature must be an integer from 0 to 5.")

    return args


def main() -> None:
    try:
        args = parse_args()
    except KeyboardInterrupt:
        print_exit_message()
        return

    try:
        client = create_client()
    except RuntimeError as error:
        print(f"Error: {error}")
        return
    except KeyboardInterrupt:
        print_exit_message()
        return

    print("English ReWriter")
    print("Enter text to rewrite or translate.\n")
    print("Using API key from KEY.txt.\n")

    if args.message:
        try:
            rewritten = rewrite_text(
                client,
                args.message,
                formality_level=args.formality_level,
            )
        except KeyboardInterrupt:
            print_exit_message()
            return
        except Exception as error:
            print(format_rewrite_error(error))
            return

        print(rewritten)
        return

    while True:
        try:
            user_text = read_multiline_input()
        except KeyboardInterrupt:
            print_exit_message()
            break

        if user_text == "/exit":
            print("Goodbye.")
            break

        if not user_text:
            print("No text entered. Please try again.\n")
            continue

        try:
            print("Waiting for LLM response...\n")
            rewritten = rewrite_text(
                client,
                user_text,
                formality_level=args.formality_level,
            )
        except KeyboardInterrupt:
            print_exit_message()
            break
        except Exception as error:
            print(f"{format_rewrite_error(error)}\n")
            continue

        print("\nResult:")
        print(rewritten)
        print()


if __name__ == "__main__":
    main()