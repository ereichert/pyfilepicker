import os
import random
import shutil
import logging

# TODO Add linter to the command line utilities
# TODO Add formatter to the command line utilities

EXTENSIONS_OF_INTEREST = ["JPG", "jpg", "jpeg", "png", "tif", "gif", "TIF"]


def get_files(path):
    logger = logging.getLogger(__name__)
    logger.info(f"Scanning '{path}' for pictures.")
    file_paths = []
    extensions = []
    for root, _, files in os.walk(path):
        for file in files:
            filename_split = file.split(".")
            # TODO Put this behind a command line option or debugging statement
            logger.debug("Found extensions:")
            found_extension = filename_split[-1]
            if found_extension not in extensions:
                extensions.append(found_extension)
                logger.debug(found_extension)
            # TODO The program should read the list of filtered extensions from a config file.
            if found_extension in EXTENSIONS_OF_INTEREST:
                file_paths.append(os.path.join(root, file))

    # TODO Turn this into a debugging statement or command line option
    # for file_path in file_paths:
    #     print(file_path)

    # TODO turn this into a debugging statement
    logger.debug(f"Number of file paths after filtering = {len(file_paths)}")

    return file_paths


# TODO Take the number of files as a command line argument
def get_random_file_paths(starting_file_paths, number_of_files=50):
    logger = logging.getLogger(__name__)
    logger.debug(f"Requested number of files = {number_of_files}.")
    num_file_paths = len(starting_file_paths)
    files_of_interest = []
    if num_file_paths < number_of_files:
        number_of_files = num_file_paths
    random_nums = random.sample(range(0, num_file_paths), number_of_files)
    for n in random_nums:
        files_of_interest.append(starting_file_paths[n])

    # TODO Put this behind a command line argument or debugging statement
    # for file_path in files_of_interest:
    #     print(file_path)
    return files_of_interest


def copy_files(sources, destination):
    logger = logging.getLogger(__name__)
    if not os.path.exists(destination):
        logger.debug(f"Directory, '{destination}' does not exist. Creating directory.")
        os.mkdir(destination)
    logger.info(f"Copying files to '{destination}'.")
    for src in sources:
        logger.debug(f"Copying {src}.")
        shutil.copy(src, destination)


def configure_logging():
    logging_formatter = logging.Formatter("%(levelname)s: %(message)s")
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(logging_formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging_handler)
    # TODO Set the logging level based on command line args.
    logger.setLevel(logging.INFO)


def main():
    configure_logging()
    # TODO This should be a command line argument
    src_root_dir = (
        "/Users/ereichert/Library/CloudStorage/SynologyDrive-household/My Pictures"
    )
    # TODO This should be a command line argument
    dst_dir = "/Users/ereichert/Desktop/photos"
    file_paths = get_files(src_root_dir)
    random_file_paths = get_random_file_paths(file_paths)
    copy_files(random_file_paths, dst_dir)


if __name__ == "__main__":
    main()
