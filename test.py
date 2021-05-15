import modules
import subprocess
import time

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
    time.sleep(1.5)
    print("Generating testing files and duplicated file")
    generate_test_files = modules.generate_files(50,100)
    generate_test_files.generate_test_files()
    generate_test_files.generate_duplicate_files()
    time.sleep(1)
    print("Listing test directory :")
    time.sleep(0.5)
    list_files = subprocess.run(["ls", "-l", generate_test_files.test_directory])
    time.sleep(1)
    print("Removing testing duplicated files")
    time.sleep(0.5)
    remove_duplicates = modules.remove_duplicates(generate_test_files.test_directory)
    remove_duplicates.calculate_all_files()
    remove_duplicates.find_duplicates()
    time.sleep(1)
    remove_duplicates.remove_duplicates()
    time.sleep(1)
    print("Ordering test files by extention , you can check inside testfiles directory created")
    time.sleep(0.5)
    forder = modules.order_files(generate_test_files.test_directory)
    forder.create_file_ext()
    forder.create_folders()
    forder.move_files()
    time.sleep(1)
    print("Listing test directory :")
    time.sleep(0.5)
    list_files = subprocess.run(["ls", "-l", generate_test_files.test_directory])
    print("if the execution has completed with no errors testing is successfull")