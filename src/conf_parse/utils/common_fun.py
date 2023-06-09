def check_str_is_url(s: str):
    prefix = ("http://", "https://", "$scheme")
    return s.startswith(prefix)