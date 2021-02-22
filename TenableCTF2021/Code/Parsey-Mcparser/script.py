import re
import json

'''
:param blob: blob of data to parse through (string)
:param group_name: A single Group name ("Green", "Red", or "Yellow",etc...)

:return: A list of all user names that are part of a given Group
'''
def ParseNamesByGroup(blob, group_name):
    users = []
    field_lists = re.finditer(r'\[.*?\]', blob)
    
    for field_list in field_lists:
        field = field_list.group(0)
        field = "{"+field[1:len(field)-1]+"}"

        if json.loads(field)["Group"] == group_name:
            users.append( str(json.loads(field)["user_name"]) )
    return users


data = raw_input()
group_name = data.split('|')[0]
blob = data.split('|')[1]
result_names_list = ParseNamesByGroup(blob, group_name)
print result_names_list
