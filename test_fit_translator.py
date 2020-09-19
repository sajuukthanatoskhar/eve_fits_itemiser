import pytest

import fit_translator

'''
This tests the ability of the fit_translator python file
'''


@pytest.fixture()
def get_test_fit_file() -> str:
    test_fit_file = './fits/unittest_hyenafit.fit'

    return test_fit_file


@pytest.fixture()
def get_test_order_file() -> str:
    test_order_file = './orderlist.order'
    return test_order_file

def test_open_fit(get_test_fit_file):
    fitfile = fit_translator.open_fit(get_test_fit_file)
    errors = []

    expected_list = ["[Hyena, TEST | HyenaUnitTest]\n",
                     "\n",
                     "IFFA Compact Damage Control\n",
                     "Signal Amplifier II\n",
                     "Signal Amplifier II\n",
                     "Signal Amplifier I\n",
                     "\n",
                     "5MN Quad LiF Restrained Microwarpdrive"]
    # replace assertions by conditions
    if not isinstance(fitfile, list):
        errors.append("Not a list")
    if not fitfile == expected_list:
        errors.append("Doesn't fit expected list contents")

    # assert no error message has been registered, else print messages
    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_itemise_fit(get_test_fit_file):
    fitfile = fit_translator.itemise_fit(open(get_test_fit_file, 'r').readlines(), 1)
    errors = []
    successful_itemised_fit = ["Hyena 1\n",
                               "Signal Amplifier II 2\n",
                               "Signal Amplifier I 1\n",
                               "5MN Quad LiF Restrained Microwarpdrive 1\n",
                               "IFFA Compact Damage Control 1"]

    for line in successful_itemised_fit:
        if line.rstrip() not in fitfile:
            errors.append("{} not in fit!".format(line))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_ship_type(get_test_fit_file):
    shipname = fit_translator.get_ship_type(open(get_test_fit_file, 'r').readlines())
    assert shipname == "Hyena"


def test_get_fit_name(get_test_fit_file):
    fitname = fit_translator.get_fit_name(open(get_test_fit_file, 'r').readlines())
    assert fitname == "HyenaUnitTest"


# def test_get_t2_component(get_test_fit_file):
#     fitlist = open(get_test_fit_file).readlines()
#
#     # fit_translator.get_t2_components(fitlist)
#
#     fit_translator.check_if_any_t2_comp_exists(fit_translator.get_t2_components(fitlist))
#
#     assert True


def test_get_t1_component(get_test_fit_file):
    fitlist = open(get_test_fit_file, 'r').readlines()
    listfinal = fit_translator.get_t1_components(fitlist, 1)
    errors = []
    expected_list = ["Signal Amplifier I 1"]

    for line in listfinal:
        if line.rstrip() not in expected_list:
            errors.append("{} not in fit!".format(line))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_t2_component(get_test_fit_file):
    fitlist = open(get_test_fit_file).readlines()
    errors = []
    # fit_translator.get_t2_components(fitlist)
    finallist = fit_translator.get_t2_components(fitlist, 1)

    expected_list = ["Signal Amplifier II 2"]

    for line in finallist:
        if line.rstrip() not in expected_list:
            errors.append("{} not in fit!".format(line))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_get_charges(get_test_fit_file):
    errors = []
    expected_list = []
    finallist = fit_translator.get_charges(open(get_test_fit_file, 'r').readlines(), 1)
    for line in finallist:
        if line.rstrip() not in expected_list:
            errors.append("{} not in fit!".format(line))

    assert not errors, "errors occured: \n{}".format("\n".join(errors))


def test_get_order(get_test_order_file):
    errors = []
    expected_list = ["Hyena 2",
                     "Signal Amplifier II 4",
                     "Small Core Defense Field Extender II 2",
                     "Signal Amplifier I 2",
                     "IFFA Compact Damage Control 2",
                     "5MN Quad LiF Restrained Microwarpdrive 2",
                     "Nanite Repair Paste 60",
                     "Multispectrum Shield Hardener II 2",
                     "Damage Control II 2",
                     "Damage Control I 2",
                     "Republic Fleet Titanium Sabot S 480"]
    fitlist = open(get_test_order_file).readlines()
    finallist = fit_translator.get_order(fitlist)

    orderlist = fit_translator.get_total_order(finallist)
    for line in orderlist:
        if line.rstrip() not in expected_list:
            errors.append("{} not in fit!".format(line))

    assert not errors, "errors occured: \n{}".format("\n".join(errors))
