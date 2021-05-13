import modules

def run_test() :
    print("Generating testing files and duplicated file")
    generate_test_files = modules.generate_files(50,100)
    generate_test_files.generate_test_files()
    generate_test_files.generate_duplicate_files()
    print("Removing testing duplicated files")
    remove_duplicates = modules.remove_duplicates(generate_test_files.test_directory)
    remove_duplicates.calculate_all_files()
    remove_duplicates.find_duplicates()
    remove_duplicates.remove_duplicates()
    print("Ordering test files by extention , you can check inside testfiles directory created")
    forder = modules.order_files(generate_test_files.test_directory)
    forder.create_file_ext()
    forder.create_folders()
    forder.move_files()
    print("if the execution has completed with no errors testing is successfull")