def clean_response(text):
    if not text:
        return text

    replacements = {
        "[line break]": "\n",
        "[linebreak]": "\n",
        "line break": "\n",
        "linebreak": "\n",
        "<br>": "\n",
        "<br/>": "\n",
        "<br />": "\n",
        "\\n": "\n",
    }

    cleaned = text

    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)

    return cleaned.strip()
