import sys
import re

def lex(characters, token_exprs, reserved_keywords, RESERVED):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if text == '\n':
                    token = [text, None]
                    tokens.append(token)
                elif tag and text not in reserved_keywords:
                    token = [text, tag]
                    tokens.append(token)
                elif tag:
                    token = [text, RESERVED]
                    tokens.append(token)
                break
        if not match:
            raise Exception('Illegal character: %s\n' % characters[pos])
        else:
            pos = match.end(0)
    return tokens
