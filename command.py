import argparse
import modules

def command() :
    my_parser = argparse.ArgumentParser(prog='file_order',
                                        description='program to delete duplicates or order file by extention',
                                        usage='%(prog)s [options] folder',
                                        epilog='Enjoy the program! :)')
    my_parser.add_argument('--folder', action='store', type=str, help='the path of the folder', required=False)
    my_parser.add_argument('--test', action='store_true', help='enable testing software functions')
    my_parser.add_argument('-o', '--order', action='store_true', help='order file by extention')
    my_parser.add_argument('-d', '--duplicates', action='store_true', help='remove duplicate files')
    args = my_parser.parse_args()
    return args

def remove_duplicates_decision(folder) :
    remove_duplicates = modules.remove_duplicates(folder)
    remove_duplicates.calculate_all_files()
    remove_duplicates.find_duplicates()
    remove_duplicates.remove_duplicates()

def file_order_decision(folder) :
    forder = modules.order_files(folder)
    forder.create_file_ext()
    forder.create_folders()
    forder.move_files()