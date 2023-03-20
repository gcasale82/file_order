import modules
from time import sleep

def run_test() :
    print(
        """usage: file_order [options] folder

program to delete duplicates or order file by extention

optional arguments:
  -h, --help        show this help message and exit
  --folder FOLDER   the path of the folder
  --test            enable testing software functions
  -o, --order       order file by extention
  -d, --duplicates  remove duplicate files
"""
    )
    sleep(1.5)
    print("Generating testing files and duplicated files")
    generate_test_files = modules.generate_files(50,100)
    generate_test_files.generate_test_files()
    generate_test_files.generate_duplicate_files()
    testDirectory = generate_test_files.test_directory
    all_files = modules.find_files_from_folder(testDirectory)
    sleep(1)
    print("Listing test directory :")
    sleep(0.5)
    for file in all_files : print(file)
    sleep(1)
    print("Removing testing duplicated files")
    sleep(0.5)
    remove_duplicates = modules.remove_duplicates(generate_test_files.test_directory)
    remove_duplicates.calculate_all_files()
    remove_duplicates.find_duplicates()
    sleep(1)
    remove_duplicates.remove_duplicates()
    sleep(1)
    print("Ordering test files by extention , you can check inside testfiles directory created")
    sleep(0.5)
    forder = modules.order_files(generate_test_files.test_directory)
    forder.create_file_ext()
    forder.create_folders()
    forder.move_files()
    sleep(1)
    print("Listing test directory :")
    all_files = modules.find_files_from_folder(testDirectory)
    sleep(0.5)
    for file in all_files : print(file)
    print("if the execution has completed with no errors testing is successfull")