from argparse import ArgumentParser
import logging
import os
import random
import shutil
import sys

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
        args.source_root_directory,
        args.destination_directory,
        num_requested_files,
        args.extensions,
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
    arg_parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        help="""List of extensions of interest. If a file having an extension 
        of interest is found it will be considered for the randomized list 
        of files.""",
    )
    return arg_parser.parse_args(args)


def get_random_files(
    src_root_dir, dst_dir, num_requested_files, extensions_of_interest
):
    """Gets a list of files from the source directory,
    selects n random files from that source directory,
    and copies the randomly chosen files to the destination directory.
    All subdirectories in the source directory will be scanned for files.
    If a list of extensions of interest is specified as a command line argument
    only files with those extensions will be selected from source directory.
    The extension filter is applied to the original list of files. That is, before
    random files are selected."""
    file_paths = get_files(src_root_dir, extensions_of_interest)
    random_file_paths = get_random_file_paths(file_paths, num_requested_files)
    copy_files(random_file_paths, dst_dir)


def get_files(src_path, extensions_of_interest):
    """Get all file paths in the src_path directory and its subdirectories.
    If extensions_of_interest is not empty it will only select files with
    extensions in the list.
    If extensions_of_interest is empty, all files will be chosen.

    Returns: List of file paths"""
    logger = logging.getLogger(__name__)
    logger.critical(f"Scanning '{src_path}' for pictures.")
    file_paths = []
    extensions = []
    for root, _, files in os.walk(src_path):
        for file in files:
            filename_split = file.split(".")
            found_extension = filename_split[-1]
            if logger.isEnabledFor(logging.DEBUG):
                if found_extension not in extensions:
                    extensions.append(found_extension)
                    logger.debug(f"found extension: {found_extension}")
            if extensions_of_interest:
                if found_extension in extensions_of_interest:
                    file_paths.append(os.path.join(root, file))
            else:
                file_paths.append(os.path.join(root, file))

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Filtered file paths:")
        for file_path in file_paths:
            logger.debug(file_path)

    logger.debug("Number of file paths after filtering = %s", len(file_paths))
    return file_paths


def get_random_file_paths(starting_file_paths, num_requested_files):
    """Given a list of files via starting_file_paths will return the number of
    requested files paths specified by num_requested_files. The files will be
    will be chosen randomly from starting_file_paths.

    Returns: List of randomly selected file paths."""
    logger = logging.getLogger(__name__)
    logger.info("Requested number of files = %s", num_requested_files)
    num_file_paths = len(starting_file_paths)
    if num_file_paths < num_requested_files:
        num_requested_files = num_file_paths
    random_nums = random.sample(range(0, num_file_paths), num_requested_files)
    # by using a set we ensure the files selected are
    # unique for each run of the tool.
    files_of_interest = {starting_file_paths[n] for n in random_nums}

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Random file paths:")
        for file_path in files_of_interest:
            logger.debug(file_path)
    return files_of_interest


def copy_files(src_file_paths, dst_dir_path):
    """Copies files specified by the list src_file_paths to the directory
    specific by dst_dir_path. If the destination directory does not exist
    it will be created. If the destination direction exists, the files will be
    appended to the existing directory."""
    logger = logging.getLogger(__name__)
    if not os.path.exists(dst_dir_path):
        logger.info(f"Directory, '{dst_dir_path}' does not exist. Creating directory.")
        os.mkdir(dst_dir_path)
    logger.critical(f"Copying files to '{dst_dir_path}'.")
    for src in src_file_paths:
        logger.debug("Copying %s.", src)
        shutil.copy(src, dst_dir_path)


def configure_logging(verbosity):
    logging_formatter = logging.Formatter("%(levelname)s: %(message)s")
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logging_formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(logging_handler)
    logger.setLevel(LOGGING_LEVELS[verbosity])


if __name__ == "__main__":
    main(sys.argv[1:])
