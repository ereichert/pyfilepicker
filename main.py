from argparse import ArgumentParser
import logging
import os
import random
import shutil
import sys

EXTENSIONS_OF_INTEREST = ["JPG", "jpg", "jpeg", "png", "tif", "gif", "TIF"]
DEFAULT_NUM_REQUESTED_FILES = 50
LOGGING_LEVELS = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}


def main(args):
    args = parse_args(args)
    configure_logging(args.verbosity)
    num_requested_files = (
        args.num_requested_files
        if args.num_requested_files
        else DEFAULT_NUM_REQUESTED_FILES
    )
    get_random_files(
        args.source_root_directory, args.destination_directory, num_requested_files
    )


def parse_args(args):
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "source_root_directory",
        help="The directory that will be scanned for files of interest.",
    )
    arg_parser.add_argument(
        "destination_directory",
        help="The directory to which the randomly chosen files will be written.",
    )
    arg_parser.add_argument(
        "-n",
        "--num_requested_files",
        help="The number of random files to copy to the destination directory.",
        type=int,
    )
    arg_parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        action="count",
        default=0,
        help="Verbosity (between 1-4 occurrences with more leading to more "
        "verbose logging). CRITICAL=0, ERROR=1, WARN=2, INFO=3, "
        "DEBUG=4",
    )
    return arg_parser.parse_args(args)


def get_random_files(src_root_dir, dst_dir, num_requested_files):
    file_paths = get_files(src_root_dir)
    random_file_paths = get_random_file_paths(file_paths, num_requested_files)
    copy_files(random_file_paths, dst_dir)


def get_files(path):
    logger = logging.getLogger(__name__)
    logger.critical(f"Scanning '{path}' for pictures.")
    file_paths = []
    extensions = []
    for root, _, files in os.walk(path):
        for file in files:
            filename_split = file.split(".")
            found_extension = filename_split[-1]
            # TODO This may be a separate utility provided by the tool. Consider
            # moving to its own command line flag and function.
            if logger.isEnabledFor(logging.DEBUG):
                if found_extension not in extensions:
                    extensions.append(found_extension)
                    logger.debug(f"found extension: {found_extension}")
            # TODO Read the list of filtered extensions from a config file.
            if found_extension in EXTENSIONS_OF_INTEREST:
                file_paths.append(os.path.join(root, file))

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Filtered file paths:")
        for file_path in file_paths:
            logger.debug(file_path)

    logger.debug("Number of file paths after filtering = %s", len(file_paths))
    return file_paths


def get_random_file_paths(starting_file_paths, num_requested_files):
    logger = logging.getLogger(__name__)
    logger.info("Requested number of files = %s", num_requested_files)
    num_file_paths = len(starting_file_paths)
    # by using a set we ensure the files selected are
    # unique for each run of the tool.
    files_of_interest = set()
    if num_file_paths < num_requested_files:
        num_requested_files = num_file_paths
    random_nums = random.sample(range(0, num_file_paths), num_requested_files)
    # TODO This should probably be a set comprehension
    for n in random_nums:
        files_of_interest.add(starting_file_paths[n])

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Random file paths:")
        for file_path in files_of_interest:
            logger.debug(file_path)
    return files_of_interest


def copy_files(sources, destination):
    logger = logging.getLogger(__name__)
    if not os.path.exists(destination):
        logger.info(f"Directory, '{destination}' does not exist. Creating directory.")
        os.mkdir(destination)
    logger.critical(f"Copying files to '{destination}'.")
    for src in sources:
        logger.debug("Copying %s.", src)
        shutil.copy(src, destination)


def configure_logging(verbosity):
    logging_formatter = logging.Formatter("%(levelname)s: %(message)s")
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging_formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging_handler)
    logger.setLevel(LOGGING_LEVELS[verbosity])


if __name__ == "__main__":
    main(sys.argv[1:])
