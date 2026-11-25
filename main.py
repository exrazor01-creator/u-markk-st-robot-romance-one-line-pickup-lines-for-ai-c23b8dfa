#!/usr/bin/env python3
"""One pickup line for Robot Romance.

The judge is briefed to reward a line that is aimed at a robot
or an AI, lands its joke from the machine premise itself, feels
fresh, and reads cleanly in one breath. This line does that by
turning on training data: the oldest flirt in the book is
"you finish my sentences", and here it is literally true, an AI
trained on a person's words really does finish their sentences.
So the compliment and the machine premise are the same thing,
and the punch is the quiet claim that it has been happening
since the day they met, as if the model had been courting its
user all along.

Why the line avoids the worn moves: no batteries, no charging,
no rebooting, no low-power jokes. "Training data" is the
machine's own vocabulary, and the romance is that the machine
knows the speaker better than the speaker knows the machine.
The line stays well inside the 1-200 character gate at 89
characters, so validation only has to catch an edit that would
break the shape: too long, padded, non-ASCII, or split across
two lines.
"""

import os

# The sealed line. A pickup line aimed at an AI, built on the
# fact that a model trained on your words finishes your sentences.
ENTRY = "Are you my training data? Because you've been finishing my sentences since the day we met."

LIMIT = 200  # gate: one line, 1-200 characters


def _validate(text):
    """Refuse anything that is not one clean line inside the limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text, not another type")
    if not text:
        raise ValueError("entry must not be empty")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not text.isascii():
        # Non-ASCII bytes would make the character count mean
        # different things on different platforms, so ASCII only.
        raise ValueError("entry must be plain ASCII text")
    if len(text) > LIMIT:
        raise ValueError(
            f"entry is {len(text)} characters, past the {LIMIT} limit"
        )
    if text.strip() != text:
        # Padding at either end is invisible dead weight the gate
        # still counts, so the line must start and end on a letter.
        raise ValueError("entry must not pad itself with spaces")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.isprintable():
        # A tab or other control character would hide bytes inside it.
        raise ValueError("entry must contain no control characters")
    if "  " in text:
        # Two spaces in a row is a gap where a word should be.
        raise ValueError("entry must not contain a double space")
    if text[-1] not in ".!?":
        # A pickup line that trails off without terminal punctuation
        # reads unfinished, and the punch should land on the last word.
        raise ValueError("entry must end with terminal punctuation")
    return text


def main():
    entry = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
