import test
import command
from os import path as ospath

def main():
    args = command.command()
    if args.test:
        test.run_test()
        return 0

    if  args.folder is None :
        print("folder is a required argument if not using test option ")
        return 0

    if ospath.exists(args.folder) :
        if args.duplicates :
            command.remove_duplicates_decision(args.folder)
        if args.order :
            command.file_order_decision(args.folder)
    else : print("The folder does not exist")

if __name__ == "__main__" :
    main()