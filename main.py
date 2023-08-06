import os

def get_files(path):
    print("Gathering file paths.")
    file_paths = []
    for root, _, files in os.walk(path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    for file_path in file_paths:
        print(file_path)

    print(len(file_paths))

def main():
    path = "/Users/ereichert/Library/CloudStorage/SynologyDrive-household/My Pictures"
    get_files(path)


if __name__ == '__main__':
    main()