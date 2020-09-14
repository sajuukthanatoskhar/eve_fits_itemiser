import pytest
import fit_translator

'''
This tests the ability of the fit_translator python file
'''
@pytest.fixture()
def get_test_fit_file() -> list:
    test_fit_file = './fits/unittest_hyenafit.fit'

    return test_fit_file

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
    fitfile = fit_translator.open_fit(get_test_fit_file)


    successful_itemised_fit = ["Hyena 1\n",
                               "Signal Amplifier II 2\n",
                               "Signal Amplifier I 1\n",
                               "5MN Quad LiF Restrained Microwarpdrive 1\n",
                               "IFFA Compact Damage Control 1"]

    assert successful_itemised_fit == fit_translator.itemise_fit(fitfile)

def test_get_ship_type(get_test_fit_file):
    shipname = fit_translator.get_ship_type(get_test_fit_file)
    assert shipname is "Hyena"

def test_get_fit_name(get_test_fit_file):
    fitname = fit_translator.get_fit_name(get_test_fit_file)
    assert fitname == "HyenaUnitTest"