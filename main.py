import os
import random

EXTENSIONS_OF_INTEREST = ['JPG', 'jpg', 'jpeg','png', 'tif', 'gif', 'TIF']

def get_files(path):
    print("Gathering file paths.")
    file_paths = []
    extensions = []
    for root, _, files in os.walk(path):
        for file in files:
            filename_split = file.split('.')
            possible_extension = filename_split[-1]
            # TODO Put this behind a command line option
            if possible_extension not in extensions:
                extensions.append(possible_extension)
            # TODO The program should read the list of filtered extensions from a config file.
            if possible_extension in EXTENSIONS_OF_INTEREST:
                file_paths.append(os.path.join(root, file))

    # TODO Turn this into a debugging statement or command line option
    # for file_path in file_paths:
    #     print(file_path)
    
    # TODO turn this into a debugging statement
    # print(len(file_paths))
    # TODO Put this behind a command line option
    # print(extensions)

    return file_paths

def get_random_file_paths(starting_file_paths, number_of_files = 50):
    files_of_interest = []
    for _ in range(number_of_files):
        random_num = random.randrange(0, len(starting_file_paths) + 1)
        files_of_interest.append(starting_file_paths[random_num])

    # TODO Put this behind a command line argument or debugging statement
    # for file_path in files_of_interest:
    #     print(file_path)
    return files_of_interest
        
def main():
    # TODO This should be a command line argument
    path = "/Users/ereichert/Library/CloudStorage/SynologyDrive-household/My Pictures"
    file_paths = get_files(path)
    random_file_paths = get_random_file_paths(file_paths)


if __name__ == '__main__':
    main()