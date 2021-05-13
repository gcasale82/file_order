import test
import command
import os

def main():
    args = command.command()
    if os.path.exists(args.folder) :
        if args.test:
            test.run_test()
        if args.duplicates :
            command.remove_duplicates_decision(args.folder)
        if args.order :
            command.file_order_decision(args.folder)
    else : print("The folder does not exist")

if __name__ == "__main__" :
    main()