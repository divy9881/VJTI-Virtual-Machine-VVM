from .rig_lexer import *

def optimize_tokens(tokens):
    optimized_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index][1] != None and tokens[index][0] not in comment_tokens:
            optimized_tokens.append(tokens[index])
            index += 1
            continue
        elif tokens[index][1] != None and tokens[index][0] == '*/':
            return None
        elif tokens[index][1] != None and tokens[index][0] == '/*':
            index += 1
            flag = 0
            while index < len(tokens):
                if tokens[index][0] == '*/':
                    flag = 1
                    break
                index += 1
            if flag == 0:
                return None
        elif tokens[index][1] != None and tokens[index][0] == '//':
            index += 1
            while index < len(tokens):
                if tokens[index][0] == '\n':
                    break
                index += 1
        index += 1
    return optimized_tokens