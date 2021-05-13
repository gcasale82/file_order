import os
import shutil
import xxhash
from collections import defaultdict
import sys
import shutil
from random import randint as rand
from progress.bar import FillingSquaresBar


class remove_duplicates():
    def __init__(self,folder):
        self.folder = os.path.abspath(folder)
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

    def compare_hash(file1, file2):
        if calcola_hash(file1) == calcola_hash(file2):
            return True
        else:
            return False
    def calculate_all_files(self):
        self.size_table = defaultdict(list)
        for subdir, dirs, files in os.walk(self.folder):
            for file in files:
                file_path = os.path.join(subdir, file)
                self.size_table[os.path.getsize(file_path)].append(file_path)

    def find_duplicates(self):
        self.duplicates_table = defaultdict(list)
        for size , files in self.size_table.items() :
            if len(files) > 1 :
                for file in files :
                    hash_value = self.calcola_hash(file)
                    self.duplicates_table[hash_value].append(file)
        self.duplicates = list()
        for hash,files in self.duplicates_table.items() :
            if len(files) > 1 :
                for file in files :
                    self.duplicates.append(file)

    def remove_duplicates(self) :
        for hash,files in self.duplicates_table.items() :
            if len(files) > 1 :
                for file in files[1:] :
                    os.remove(file)
                    print(f"File {file} has been deleted duplicated with hash {hash}")

class order_files():
    def __init__(self,folder):
        self.folder = os.path.abspath(folder)

    def create_file_ext(self):
        self.file_ext = defaultdict(list)
        self.extentions = list()
        for subdir, dirs, files in os.walk(self.folder):
            for file in files:
                filepath = os.path.join(subdir, file)
                if os.path.splitext(filepath)[1] != '':
                    ext = os.path.splitext(filepath)[1].strip('.')
                    self.file_ext[ext].append(filepath)
                    self.extentions.append(ext)
        self.extentions = list(set(self.extentions))

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
        self.file_extention = ["pdf", "txt", "jpg", "tmp", "html", "avi", "ova", "mp4", "mp3", "odt", "xls", "html", "sql", "bin"]
    def generate_test_files(self):
        if not os.path.exists(self.test_directory):
            os.makedirs(self.test_directory)
        else :
            shutil.rmtree(self.test_directory)
            os.makedirs(self.test_directory)
        os.chdir(self.test_directory)

        bar = FillingSquaresBar('Processing' , max=self.files_number)
        for i in range(self.files_number) :
            filename = "file" + str(i) + f".{self.file_extention[rand(0,len(self.file_extention) - 1 )]}"
            with open(filename, 'wb') as new_random_file:
                d1 = rand(1, 1000)
                d2 = rand(1, 999)
                dimension = d1 * self.file_size + d2
                new_random_file.write(os.urandom(dimension))
            bar.next()
        bar.finish()
    def generate_duplicate_files(self):
        os.chdir(self.test_directory)
        for i in range(5) :
            filename = "file_source" + str(i)
            with open(filename, 'wb') as new_random_file:
                new_random_file.write(os.urandom(100000))
            shutil.copy(filename, filename + "duplicated")
