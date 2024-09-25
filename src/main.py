
from  pprint import pprint
import timeit

from  redis import RedisError

from hw08.database.connect import connect_db
from hw08.database.seeds import seeds,seed_contacts
from hw08.database.search import find_by_name, find_by_tag


commands = ("name", "tag", "help", "exit")

def print_result(records: list):
   
    if records:
        for ind, record in enumerate(records,1 ):
            print(f"[ {ind} ]","-"*100)
            pprint(record)
    else:
        print("Not Found")


def main(seed_on: bool = True):
    if connect_db():
        if seed_on:
            seeds()
            # seed_contacts()

        ##console search

        while True:
            try:
                command = None
                command_args = None
                search_input = input(">>>")
                search_split = search_input.split(":")
                if len(search_split) < 1 :
                    print(f"commands undetected,  please to use ':' as command separator")
                    continue
                command = search_split[0].strip().lower()
                if command not in commands:
                    print(f"command '{command}' - unknown, can use 'help' for list of commands") 
                    continue  
                match command:
                    case "help":
                        print(f"List of commands: {commands},  please to use ':' as argument separator")
                        continue
                    case "exit":
                        print(f"command '{command}'")
                        break

                if  len(search_split) < 2 :
                    print(f"for command '{command}' arguments is undetected,  please to use ':' as argument  separator")
                    continue
                command_args = search_split[1].strip()
                if  not command_args :
                    print(f"for command '{command}' arguments is empty")
                    continue
                start_time = timeit.timeit()
                match command:
                    case "name":
                        print(f"command '{command}' - args: {command_args} ")  
                        print_result(find_by_name(command_args))
                    case "tag":
                        print(f"command '{command}' - args: {command_args} ") 
                        print_result(find_by_tag(command_args))
                    case _:
                        print(f"command '{command}' - unknown, help - list of command")   
                print("Time execution:", timeit.timeit()-start_time)
            except KeyboardInterrupt:
                print("exit")
                break


if __name__ == "__main__":
    try:
        main()
    except RedisError as e:
        print("ERROR Redis connction", e)