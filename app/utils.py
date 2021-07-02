def truncate(text, length=0):
    if isinstance(text, str):
        if len(text) > length:
            return text[:length]
        else:
            return text
    else:
        return ""