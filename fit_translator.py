import re

def open_fit(file: str) -> list:
    '''

    :param file: .fit file to be opened
    :return: list of the stuff in the .fit file
    '''
    fit_file = open(file, 'r')
    file_list = fit_file.readlines()
    return file_list


def itemise_fit(fit: list, qty) -> list:
    shipname = get_ship_type(fit) + " {}".format(qty * 1)
    t2_components_list = [line.replace('\n', '') for line in get_t2_components(fit, qty)]
    t1_components_list = [line.replace('\n', '') for line in get_t1_components(fit, qty)]
    other_comps = [line.replace('\n', '') for line in get_anyothercomponents(fit, qty)]

    itemised_fit = []
    itemised_fit.append(shipname)
    itemised_fit.extend(t2_components_list)
    itemised_fit.extend(t1_components_list)
    itemised_fit.extend(other_comps)
    return itemised_fit

def get_fit_name(fit: list) -> str:
    matches = []
    for line in fit:
        if len(re.findall(r"(\w+])", line)) > 0:
            matches.append(re.findall(r"(\| \w+])", line))
    if len(matches) is 1:
        name = matches[0][0][2:-1]
    return name


def get_ship_type(fit: list) -> str:
    matches = []
    name = "Error"
    for line in fit:
        if len(re.findall(r"(\[\w+)", line)) > 0:
            matches.append(re.findall(r"(\[\w+)", line))
    if len(matches) is 1:
        name = matches[0][0][1:]
    return name


def get_t2_components(fit: list, qty: float) -> list:
    mod_dict = get_components_by_str(fit, " II\n", qty)
    finallist = []
    for key in mod_dict:
        finallist.append("{} {}".format(key.rstrip(), mod_dict[key]))
    return finallist


def get_t1_components(fit: list, qty: float) -> list:
    mod_dict = get_components_by_str(fit, " I\n", qty)
    finallist = []
    for key in mod_dict:
        finallist.append("{} {}".format(key.rstrip(), mod_dict[key]))
    return finallist


def get_anyothercomponents(fit: list, qty: float) -> list:
    mod_dict = {}
    fit.pop(0)  # don't need the name, we already have it!
    for line in fit:
        if not " I\n" in line[1:] and not " II\n" in line[1:] and line is not '\n':
            if line in mod_dict.keys():
                mod_dict[line] += 1 * qty
            else:
                mod_dict[line] = 1 * qty
    finallist = []
    for key in mod_dict:
        finallist.append("{} {}".format(key.rstrip(), mod_dict[key]))
    return finallist


def get_components_by_str(fit: list, search_str: str, qty: float) -> dict:
    '''
    Filters components by string, useful for getting t2,t1 (II,I) components
    :param fit:
    :param search_str:
    :return:
    '''
    mod_dict = {}
    for line in fit:
        if search_str in line:
            if line in mod_dict.keys():
                mod_dict[line] += 1 * qty
            else:
                mod_dict[line] = 1 * qty
    return mod_dict


def get_order(fit: list, qty: float):
    '''
    Gets fit specific total number of mods and ammo required
    :param fit:
    :param qty:
    :return:
    '''
    finalorder_list = []
    return finalorder_list
