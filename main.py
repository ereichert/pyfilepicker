import os

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

    for file_path in file_paths:
        print(file_path)
    
    # TODO turn this into a debugging statement
    print(len(file_paths))
    print(extensions)

def main():
    # TODO This should be a command line argument
    path = "/Users/ereichert/Library/CloudStorage/SynologyDrive-household/My Pictures"
    get_files(path)


if __name__ == '__main__':
    main()