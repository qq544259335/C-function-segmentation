import os
import re
from collections import deque
import json

file_list = os.popen("ls *.c").read().split("\n")[:-1]
# (\w+) # return type
# ((VOID)|(void)|(char)|(short)|(int)|(float)|(long)|(double)) # return type
regular = r'''
            (\s*)   
            ((static)|(extern))?
            (\s*)
            (inline)?
            (\s*)
            (const)?
            (\s*)
            (\w+)                                                        # return type
            ((\s*(\*)*\s+)|(\s+(\*)*\s*))                                # * 
            (\w+)                                                        # funcname
            ((\s*)(\()(\n)?)                                             # (
            '''

pattern = re.compile(regular, re.X)
j = {"segementation" : []}
with open("./raw", 'w') as ff:
    for index, file in enumerate(file_list):
        with open("./" + file) as f:
            j["segementation"].append({file : []})
            text = f.read()
            print("Segementation: file name ", file)
            while True:
                # before (
                match = pattern.search(text)
                if match is None:
                    break
                func = match.group().lstrip()
                text = text[match.span()[1]:]
                # ()
                end = text.find(")")
                check = text.find("(")
                if check < end:
                    cnt_bracket = 1
                    for i in range(len(text)):
                        if text[i] == "(":
                            cnt_bracket += 1
                        elif text[i] == ")":
                            cnt_bracket -= 1
                        if cnt_bracket == 0:
                            end = i
                            break
                param = text[:end + 1]
                text = text[end + 1:]
                # {}
                reg = r'(\s*)\{'
                pt = re.compile(reg, re.X)
                lil_match = pt.match(text)
                if lil_match:
                    start = lil_match.span()[1]
                    cnt_bracket2 = 1
                    for i in range(start, len(text)):
                        if text[i] == "{":
                            cnt_bracket2 += 1
                        elif text[i] == "}":
                            cnt_bracket2 -= 1
                        if cnt_bracket2 == 0:
                            end = i
                            break
                    body = text[:end + 1]
                    text = text[end + 1:]
                    # print("func", func)
                    # print("param", param)
                    # print("body", body)
                    ff.write(func + param + body)
                    ff.write('\n')
                    ff.write('----------end-------------\n')
                    j["segementation"][index][file].append({ "function body": (func + param + body)})
with open("./output.json", "w") as f:
    json.dump(j, f)
print("All done")

