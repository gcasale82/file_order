import os
import shutil
import xxhash
from collections import defaultdict
import shutil
from random import randint as rand
def find_files_from_folder(folder):
    all_files= []
    for dir , subdirs , files in os.walk(folder):
        all_files.extend([os.path.join(dir,file) for file in files])
    return all_files


class remove_duplicates():
    def __init__(self,folder):
        self.all_files = find_files_from_folder(folder)
    def calcola_hash(self,filename):
        BUF_SIZE = 64000
        hash_file = xxhash.xxh64()
        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                hash_file.update(data)
        return hash_file.hexdigest()

    def calculate_all_files(self):
        self.size_table = defaultdict(list)
        for file in self.all_files:
            self.size_table[os.path.getsize(file)].append(file)

    def find_duplicates(self):
        self.duplicates_table = defaultdict(list)
        size_table_same_size = {k:v for k,v in self.size_table.items() if len(v) > 1}
        for size , files in size_table_same_size.items() :
            for file in files :
                hash_value = self.calcola_hash(file)
                self.duplicates_table[hash_value].append(file)
        self.duplicates = [file for k,v in self.duplicates_table.items() for file in v if len(v) > 1]

    def remove_duplicates(self) :
        final_duplicates_table = {k:v for k,v in self.duplicates_table.items() if len(v) > 1}
        for hash,files in final_duplicates_table.items() :
            for file in files[1:] :
                os.remove(file)
                print(f"File {file} has been deleted duplicated with hash {hash}")

class order_files():
    def __init__(self,folder):
        self.folder = folder
        self.all_files = find_files_from_folder(folder)

    def create_file_ext(self):
        self.file_ext = defaultdict(list)
        self.extentions = list()
        for filepath in self.all_files :
            if os.path.splitext(filepath)[1] != '':
                ext = os.path.splitext(filepath)[1].strip('.')
                self.file_ext[ext].append(filepath)
                self.extentions.append(ext)
        self.extentions = tuple(set(self.extentions))

    def create_folders(self):
        for ext in self.extentions :
            if not os.path.exists(os.path.join(self.folder , ext)) :
                os.mkdir(os.path.join(self.folder , ext))

    def move_files(self):
        for ext,files in self.file_ext.items() :
            for file in files :
                path , filename = os.path.split(file)
                if os.path.exists(os.path.join(path , ext)):
                    shutil.move(file ,os.path.join(path,ext,filename) )
class generate_files() :
    def __init__(self , files_number , files_size ):
        current_directory = os.getcwd()
        self.test_directory = os.path.join(current_directory, 'testfiles')
        self.files_number = files_number
        self.file_size = files_size
        self.file_extention = ("pdf", "txt", "jpg", "tmp", "html", "avi", "ova", "mp4", "mp3", "odt", "xls", "html", "sql", "bin")

    def write_file(self,filename):
        with open(filename, 'wb') as new_random_file:
            d1 = rand(1, 1000)
            d2 = rand(1, 999)
            dimension = d1 * self.file_size + d2
            new_random_file.write(os.urandom(dimension))

    def generate_test_files(self):
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)
        else :
            shutil.rmtree(self.test_directory)
            os.makedirs(self.test_directory)
        os.chdir(self.test_directory)
        setExtention = lambda : f".{self.file_extention[rand(0,len(self.file_extention) - 1 )]}"
        setFname = lambda x : "-".join(("file",str(x),setExtention()))
        files = (setFname(f) for f in range(self.files_number))
        for f in files : self.write_file(f)

    def prepare_file(self,x) :
        filename="".join(("file_source",x))
        with open(filename, 'wb') as new_random_file :
            new_random_file.write(os.urandom(1000))
        shutil.copy(filename, filename + "duplicated")
        print(filename + " is duplicated file of file : "+ filename + "duplicated")

    def generate_duplicate_files(self):
        print("Generating duplicated files ... \n")
        print("Duplicate files listing :  \n")
        os.chdir(self.test_directory)
        for f in range(500) : self.prepare_file(str(f))
