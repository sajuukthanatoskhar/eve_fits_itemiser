import re

def open_fit(file: str) -> list:
    '''

    :param file: .fit file to be opened
    :return: list of the stuff in the .fit file
    '''
    fit_file = open(file, 'r')
    file_list = fit_file.readlines()
    return file_list

def itemise_fit(fit: list) -> list:
    '''
    Itemises the fit

    :param fit:
    :return: itemised list for fit
    '''

    itemised_fit = None
    return itemised_fit

def get_fit_name(fit: list) -> str:
    matches = []
    for line in open_fit(fit):
        if len(re.findall(r"(\w+])", line)) > 0:
            matches.append(re.findall(r"(\| \w+])", line))
    if len(matches) is 1:
        name = matches[0][0][2:-1]
    return name

def get_ship_type(fit:list) -> str:
    ship_name = "rifter"
    return ship_name

def get_t2_components(fit:list) -> list:
    pass

def get_t1_components(fit:list) -> list:
    pass

def get_anyothercomponents(fit:list) -> list:
    pass
