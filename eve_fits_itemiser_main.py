import sys

import fit_translator

if __name__ == '__main__':
    file = open(sys.argv[1], 'r').readlines()
    orderlist = fit_translator.get_total_order(fit_translator.get_order(file))
    fit_translator.write_total_order_to_file(orderlist, "final_order.ord")
