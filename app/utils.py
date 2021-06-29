def truncate(text, length=0):
    if isinstance(text, str):
        text = lambda text: len(text)>length and text[:length]+'...' or text
    else:
        return ""