import json

def remove_prefix(s, prefix):
    return s[len(prefix):] if s.startswith(prefix) else s

# find locations within a city
def citySearch(dict, search_loc):
    res = []
    for key, value in dict.items():
        if value == search_loc:
            res.append(key)
    return res

input_file = open ('static/json/pddlout.json')
json_array = json.load(input_file)

# This is the list of dicts that will be made into a new json file
list_d = []

# hub list
hub_list = []

# # location list
# loc_list = []

# Find the hierarchy relation of the json file
relation_set = set()
contain_list = []
for item in json_array['in']:
    containee = item[0].rstrip(item[0][-1])
    container = item[1].rstrip(item[1][-1])
    containee_spe = item[0]
    container_spe = item[1]
    contain_list.append((containee_spe,container_spe))
    relation_set.add((containee, container))

# this dictionary store containee as key and container as value
relation_dict = dict(relation_set)

# this dic store specific containing logic
contain_dict = dict(contain_list)


for hub in json_array['is-hub']:
    hub_list.append(hub[0])

# for location in json_array['is-location']:
#     if location[0].startswith('location'):
#         loc_list.append(location[0])

for location in json_array['is-location']:
    if location[0].startswith('city'):
        new_d = {"size": 400}
        new_d['name'] = "location."+location[0]
        list_d.append(new_d)
    else:
        new_d = {"size": 100}
        new_d['name'] = "location." + contain_dict[location[0]]+"."+location[0] 
        new_d['imports'] = [n for n in (citySearch(contain_dict, contain_dict[location[0]])) if n != location[0]]
        if location[0] in hub_list:
            new_d['imports'] += [n for n in hub_list if n != location[0]]
        newl = []
        for i in new_d['imports']:
            newl.append("location."+contain_dict[i]+"."+i)
        new_d['imports'] = newl
        list_d.append(new_d)

for package in json_array['is-package']:

    new_d = {"name": package[0], "size": 50, "location": "location."+contain_dict[contain_dict[package[0]]]+"."+contain_dict[package[0]]}
    list_d.append(new_d)

for truck in json_array['is-truck']:
    new_d = {"name": truck[0],"size": 50, "location": "location."+contain_dict[contain_dict[truck[0]]]+"."+contain_dict[truck[0]]}
    list_d.append(new_d)

for airplane in json_array['is-airplane']:
    new_d = {"name": airplane[0],"size": 50, "location": "location."+contain_dict[contain_dict[airplane[0]]]+"."+contain_dict[airplane[0]]}
    list_d.append(new_d)

js_out = json.dumps(list_d)
print(js_out)
