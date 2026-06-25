def build_prompt(c,q):
    return f"""Use context only.
CONTEXT:{c}
QUESTION:{q}
ANSWER:"""
