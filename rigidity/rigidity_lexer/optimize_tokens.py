from .rig_lexer import *

def optimize_tokens(tokens):
    optimized_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index][1] != None and tokens[index][1] == 'STRING':
            tokens[index][0] = tokens[index][0][1:-1]
            optimized_tokens.append(tokens[index])
        elif tokens[index][1] != None and tokens[index][0] not in comment_tokens and tokens[index][0] not in list_tokens and tokens[index][0] not in function_tokens:
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
        elif tokens[index][1] != None and tokens[index][0] == ']':
            return None
        elif tokens[index][1] != None and tokens[index][0] == '[':
            index += 1
            l = []
            flag = 0
            while index < len(tokens):
                if tokens[index][0] == ']':
                    flag = 1
                    optimized_tokens.append([l, LIST])
                    break
                if tokens[index][1] == 'INT':
                    l.append(int(tokens[index][0]))
                elif tokens[index][1] == 'FLOAT':
                    l.append(float(tokens[index][0]))
                elif tokens[index][1] == 'STRING':
                    l.append(str(tokens[index][0][1:-1]))                    
                index += 1
            if flag == 0:
                return None
        elif tokens[index][1] != None and tokens[index][0] == ')':
            return None
        elif tokens[index][1] != None and tokens[index][0] == '(':
            f = []
            f.append(tokens[index - 1][0])
            optimized_tokens.pop()
            index += 1
            flag = 0
            p = []
            while index < len(tokens):
                if tokens[index][0] == ')':
                    flag = 1
                    f.append(p)
                    optimized_tokens.append([f, FUNC])
                    break    
                if tokens[index][1] == 'INT':
                    p.append(int(tokens[index][0]))
                elif tokens[index][1] == 'FLOAT':
                    p.append(float(tokens[index][0]))
                elif tokens[index][1] == 'STRING':
                    p.append(str(tokens[index][0][1:-1]))
                else:
                    if tokens[index][0] != ',':
                        p.append(tokens[index])                    
                index += 1
            if flag == 0:
                return None
        index += 1
    return optimized_tokens