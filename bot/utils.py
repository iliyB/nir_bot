import csv

import requests
from fuzzywuzzy import process


def read_names_file():
    with open('names.txt', encoding="utf8") as f:
        list_of_names = f.read().splitlines()
    return list_of_names


def recovery_fios(without_firstname, remember_strings):
    unique_fios = []
    for name in without_firstname:
        if without_firstname[name] != '':
            unique_fios.append(
                without_firstname[name][:remember_strings[without_firstname[name]][0]] + remember_strings[without_firstname[name]][1] +
                without_firstname[name][remember_strings[without_firstname[name]][0]:])
        else:
            unique_fios.append(name)
    return unique_fios


def get_without_firstname(sorted_names):
    remember_strings = {}

    for first_name in sorted_names:
        new_names = []
        for name_from_dict in sorted_names[first_name]:

            if name_from_dict.startswith(first_name) and (first_name + ' ' in name_from_dict):
                replaced_name = name_from_dict.replace(first_name + ' ', '')
                new_names.append(replaced_name)
                remember_strings[replaced_name] = [name_from_dict.index(first_name + ' '), first_name + ' ']
            elif ' ' + first_name + ' ' in name_from_dict:
                replaced_name = name_from_dict.replace(first_name + ' ', '')
                new_names.append(replaced_name)
                remember_strings[replaced_name] = [name_from_dict.index(' ' + first_name + ' '), ' ' + first_name]
            elif (' ' + first_name in name_from_dict) and name_from_dict.endswith(first_name):
                replaced_name = name_from_dict.replace(' ' + first_name, '')
                new_names.append(replaced_name)
                remember_strings[replaced_name] = [name_from_dict.index(' ' + first_name), ' ' + first_name]
        sorted_names[first_name] = new_names

    return sorted_names, remember_strings


def get_unique_firstname(names):
    list_of_names = read_names_file()
    sorted_names = {}

    for name in names:
        for name_from_list in list_of_names:
            if (name.startswith(name_from_list) and (name_from_list + ' ' in name)) \
                    or (' ' + name_from_list in name and name.endswith(name_from_list)) \
                    or (' ' + name_from_list + ' ' in name) \
                    or (name.startswith(name_from_list) and name.endswith(name_from_list)):
                if name_from_list not in sorted_names:
                    sorted_names[name_from_list] = [name]
                elif name_from_list in sorted_names:
                    list_var = sorted_names.get(name_from_list)
                    list_var.append(name)
                    sorted_names[name_from_list] = list_var

    all_sorted_names = []
    for sorted_name in sorted_names:
        for name in sorted_names[sorted_name]:
            if sorted_names[sorted_name] != '':
                all_sorted_names.append(name)
    print(all_sorted_names)

    for name in names:
        if name not in all_sorted_names:
            sorted_names[name] = []

    return sorted_names

def get_unique_names(names):
    sorted_names = {}
    for name in names:
        sorted_names[name] = [name]
    return sorted_names


def string_compare(names):
    total = {}
    total_count = 0
    for name in names:
        matching = process.extract(name, names, limit=len(names))
        for score in matching:
            total_count += score[1]
        total[name] = total_count
        total_count = 0


    count_max = 0
    str_max = ''
    for name in total:
        if total[name] > count_max or (total[name] == count_max and len(name) > len(str_max)):
            count_max = total[name]
            str_max = name

    return str_max


def generate_priority_address(address, addresses):
    priority_address = address + '\nПанорама: https://yandex.ru/maps/?panorama[point]='
    priority_address = priority_address + str(addresses[address][0])+','+str(str(addresses[address][1]))
    return priority_address


def generate_midpoint(coord):
    supporting_list = coord
    lat = []
    long = []
    for coord in supporting_list:
        lat.append(coord[0])
        long.append(coord[1])

    return [round(sum(lat) / len(lat), 6), round(sum(long) / len(long), 6)]


def generate_map_link(dict_with_adressess):

    link_dynamic = 'https://yandex.ru/maps/?ll='
    link_static = 'https://static-maps.yandex.ru/1.x/?ll='
    coordinates = []
    for address in dict_with_adressess:
        coordinates.append(dict_with_adressess[address])

    center_of_map = generate_midpoint(coordinates)
    link_dynamic = link_dynamic+str(center_of_map[0])+','+str(center_of_map[1])+'&l=map&pt='
    link_static = link_static + str(center_of_map[0]) + ',' + str(center_of_map[1]) + '&l=map&pt='
    for coord in coordinates:
        link_dynamic = link_dynamic + str(coord[0]) + ',' + str(coord[1]) + '~'
        link_static = link_static + str(coord[0]) + ',' + str(coord[1]) + '~'

    response = requests.get(link_static[:-1])

    with open("map.png", "wb") as file:
        file.write(response.content)

    return link_dynamic[:-1]


def get_priority_dict(obj):
    copy_dict = {}
    for value in obj.addresses_analyze:
        copy_dict[value] = 0

    for address in obj.order_addresses_full:
        for count in copy_dict:
            if address == count:
                copy_dict[count] = copy_dict[count] + 1

    obj.priority_address = max(copy_dict, key=copy_dict.get)
    return copy_dict


def work_with_addresses(obj):
    priority_dict = get_priority_dict(obj)
    #my_file.write(str(priority_dict)+'\n')
    analyze_dict = obj.addresses_analyze.copy()
   # my_file.write(str(analyze_dict))

    list_for_del = []
    for address in analyze_dict:
        for zxc in analyze_dict:
            if (abs((analyze_dict[address][0] - analyze_dict[zxc][0]) +
                    (analyze_dict[address][1] - analyze_dict[zxc][1])))<0.0005\
                    and len(address) > len(zxc) and address != zxc:
                list_for_del.append(zxc)
                if zxc in priority_dict:
                    priority_dict[address] = priority_dict[address] + priority_dict[zxc]
                    priority_dict.pop(zxc)

    list_for_del = list(set(list_for_del))
    for address in list_for_del:
        obj.addresses_analyze.pop(address)

    priority_address = generate_priority_address(max(priority_dict, key=priority_dict.get), obj.addresses_analyze)

    obj.priority_address = priority_address

    obj.link_with_addresses = generate_map_link(obj.addresses_analyze)


def work_with_names(obj):

    names = list(set(obj.fios))
    remember_strings = None

    unique_firstnames = get_unique_firstname(names)

    if len(unique_firstnames) == 0:
        without_firstname = get_unique_names(names)
    else:
        without_firstname, remember_strings = get_without_firstname(unique_firstnames)

    for name in without_firstname:
        without_firstname[name] = string_compare(without_firstname[name])

    print(without_firstname)

    if remember_strings is not None:
        unique_names = recovery_fios(without_firstname, remember_strings)
    else:
        unique_names = without_firstname

    obj.unique_names = unique_names

def work_with_number(obj):
    with open("for_numbers.csv", encoding="utf8") as file:
        reader = csv.DictReader(file, delimiter=";")

        phones_info = []

        for phone in obj.phones:
            zone = phone[1:4]
            second_part = phone[4:]

            info = phone + ' - Оператор: '

            for line in reader:
                if line['\ufeffzone'] == zone and line['start'] < second_part < line['end']:
                    info = info + line['operator'] + ' Регион: ' + line['region']

            print(info)
            phones_info.append(info)

        obj.phones_info = phones_info





