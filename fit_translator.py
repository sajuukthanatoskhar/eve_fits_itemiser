import re


def open_fit(file: str) -> list:
    '''

    :param file: .fit file to be opened
    :return: list of the stuff in the .fit file
    '''
    fit_file = open(file, 'r')
    file_list = fit_file.readlines()
    return file_list


def split_item_qty(eve_item: str) -> [str, int]:
    """
    Splits an eve item.  This is aimed at multiple empty space modules and entities.
    :param eve_item:
        Example "Tritanium 100"
                "Test Free Rifter 20"
    :return: dict, as Montolio intended
    """
    item_qty_dict = {}

    return [eve_item.rpartition(" ")[0], int(eve_item.rpartition(" ")[2])]


def itemise_fit(fit: list, qty) -> list:
    '''
    Gets an itemised fit
    :param fit:
    :param qty:
    :return:
    '''
    itemised_fit = []

    if qty != 0:
        shipname = get_ship_type(fit) + " {}".format(qty * 1)
        itemised_fit.append(shipname)
    t2_components_list = [line.replace('\n', '') for line in get_t2_components(fit, qty)]
    t1_components_list = [line.replace('\n', '') for line in get_t1_components(fit, qty)]
    other_comps = [line.replace('\n', '') for line in get_anyothercomponents(fit, qty)]
    charges = [line.replace('\n', '') for line in get_charges(fit, qty)]  # todo

    itemised_fit.extend(t2_components_list)
    itemised_fit.extend(t1_components_list)
    itemised_fit.extend(other_comps)
    itemised_fit.extend(charges)

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
    if len(matches) > 0:
        name = matches[0][0][1:]
    return name


def get_t2_components(fit: list, qty: float) -> list:
    mod_dict = get_components_by_str(fit, " II\n", qty)
    finallist = []
    for key in mod_dict:
        if mod_dict[key] == 0:
            continue
        finallist.append("{} {}".format(key.rstrip(), mod_dict[key]))
    return finallist


def get_t1_components(fit: list, qty: float) -> list:
    mod_dict = get_components_by_str(fit, " I\n", qty)
    finallist = []
    for key in mod_dict:
        if mod_dict[key] == 0:
            continue
        finallist.append("{} {}".format(key.rstrip(), mod_dict[key]))
    return finallist


def get_anyothercomponents(fit: list, qty: float) -> list:
    mod_dict = {}
    qty = int(qty)
    fit.pop(0)  # don't need the name, we already have it!
    for line in fit:
        if not " I\n" in line[1:] and not " II\n" in line[1:] and "slot]" not in line and line is not '\n' and len(
                re.findall(r" x\d+$", line)) == 0:
            if line in mod_dict.keys():
                mod_dict[line] += 1 * qty
            else:
                mod_dict[line] = 1 * qty
    finallist = []
    for key in mod_dict:
        if mod_dict[key] == 0:
            continue
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
    qty = int(qty)
    for line in fit:
        if search_str in line:
            if line in mod_dict.keys():
                mod_dict[line] += 1 * qty
            else:
                mod_dict[line] = 1 * qty
    return mod_dict


def get_charges(fit: list, qty: float) -> list:
    mod_dict = {}
    finallist = []
    qty = int(qty)
    for line in fit:

        if line != "\n" and "slot]" not in line and len(re.findall(r" \w\d+$", line)) > 0:
            line = re.split(r"( \w\d+$)", line, 2)  # for charges
            if line[0] in mod_dict.keys():
                mod_dict[line[0]] += int(line[1][2:]) * qty
            else:
                mod_dict[line[0]] = int(line[1][2:]) * qty
    for key in mod_dict:
        if mod_dict[key] == 0:
            continue
        finallist.append("{} {}".format(key.rstrip(), mod_dict[key]))
    return finallist


def new_get_fit_name(fit: list) -> str:
    """
    Gets the name of a fit from an EFT block
    :param fit: the fit as a copied EFT fit
    :return: parsed_fit_name
    """
    parsed_fit_name :str = fit[0].split(',')[1].lstrip(' ').rstrip(']').replace(" ", "_")
    return parsed_fit_name


def make_fit_file(fit: list) -> None:
    """
    Makes a fit into a file
    :param fit:  EFT Fitting block
    :return: None
    """

    import os
    print(os.path.isdir('./Fits'))
    try:
        path = "./Fits/{}.fit".format(new_get_fit_name(fit))
        output_fit_file = open(path, 'w')
        for line in fit:
            output_fit_file.write("{}\n".format(line))
    except IndexError:
        print("Either you pressed cancel or didn't enter anything")

def get_order(orderlist: list):
    '''
    Gets fit specific total number of mods and ammo required for all from a list of fits
    :param orderlist:
    :param fitlist: is a list of fits with quantity '<harpyfit location>.fit qty'
    :return: total order of modules and ships required, these ARE NOT collated
    '''
    uncollated_order = []

    for line in orderlist:
        if line != '\n':
            qty = line.split(' ')[1]
            name = "./fits/" + line.split(' ')[0]
            fitlist = open(name, 'r').readlines()
            uncollated_order.extend(itemise_fit(fitlist, int(qty)))

    return uncollated_order


def get_total_order(uncollatedorder: list):
    '''
    Collate the order
    :param uncollatedorder:
    :return:
    '''
    mod_dict = {}
    collated_order = []
    for line in uncollatedorder:
        modline = re.split(r"( \d+$)", line, 2)
        if modline[0] in mod_dict.keys():
            mod_dict[modline[0]] += int(modline[1][1:])
        else:
            mod_dict[modline[0]] = int(modline[1][1:])
    for key in mod_dict:
        collated_order.append("{} {}".format(key.rstrip(), mod_dict[key]))

    return collated_order


def write_total_order_to_file(collated_order, filename):
    orderfile = open("{}.order".format(filename), 'w')
    for line in collated_order:
        orderfile.write(line + "\n")
    orderfile.close()
    return 1


def get_all_fits_as_list_str() -> list:
    """
    Gets all fits in the Fits dir
    :return: fits as a list, stripping the .fit out
    todo : there will be a bug in the actual test, this is unintended and the test needs to be rewritten
    """
    import sys,os
    fits = os.listdir("./Fits/")
    fits = [new_fit_name.rstrip(".fit") for new_fit_name in fits if ".fit" in new_fit_name]

    return fits