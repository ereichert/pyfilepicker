import pytest
import main
import os

# Filtered files are files that we do not want to copy.
# An example of filtered files are text files stored in the same directories
# as the files of interest.
NUM_FILTERED_FILES = 100

PARAMS_WITHOUT_REQUESTED_NUM_FILES = [
    # num_files_on_disk, expected_files_copied
    (0, 0),  # no files on disk
    (
        main.DEFAULT_NUM_REQUESTED_FILES * 2,
        main.DEFAULT_NUM_REQUESTED_FILES,
    ),  # more files on disk than default
    (
        int(main.DEFAULT_NUM_REQUESTED_FILES / 2),
        int(main.DEFAULT_NUM_REQUESTED_FILES / 2),
    ),  # fewer files on disk than default
    (
        main.DEFAULT_NUM_REQUESTED_FILES,
        main.DEFAULT_NUM_REQUESTED_FILES,
    ),  # same number of files on disk as default
]


@pytest.mark.parametrize(
    "num_files_on_disk, expected_num_files_copied", PARAMS_WITHOUT_REQUESTED_NUM_FILES
)
def test_number_of_files_copied_without_num_files_requested(
    src_dir,
    dst_dir,
    expected_num_files_copied,
):
    """
    Ensure the correct number of files are copied to the destination directory
    given the state of the files on disk and the default number of files requested.
    Each file copied should be unique.
    """
    main.main(
        [
            str(src_dir),
            str(dst_dir),
        ]
    )
    resulting_dst_file_paths = get_resulting_dst_file_paths(dst_dir)

    assert len(resulting_dst_file_paths) == expected_num_files_copied
    # since the set cannot have duplicate files this will ensure the test
    # accounts for duplicate file paths which we do not want.
    assert len(resulting_dst_file_paths) == len(set(resulting_dst_file_paths))


PARAMS_WITH_REQUESTED_NUM_FILES = [
    # num_files_on_disk, num_files_requested, expected_files_copied
    (0, 10, 0),  # no files on disk
    (50, 10, 10),  # more files on disk than requested
    (10, 25, 10),  # fewer files on disk than requested
    (25, 25, 25),  # same number of files on disk as were requested
]


@pytest.mark.parametrize(
    "num_files_on_disk, num_files_requested, expected_num_files_copied",
    PARAMS_WITH_REQUESTED_NUM_FILES,
)
def test_number_of_files_copied_with_all_cli_args(
    src_dir,
    dst_dir,
    num_files_requested,
    expected_num_files_copied,
):
    """
    Ensure the correct number of files are copied to the destination directory
    given the state of the files on disk and the number of files requested by
    the user. Each file copied should be unique.
    """
    main.main(
        [
            str(src_dir),
            str(dst_dir),
            "--num_requested_files",
            str(num_files_requested),
        ]
    )
    resulting_dst_file_paths = get_resulting_dst_file_paths(dst_dir)

    assert len(resulting_dst_file_paths) == expected_num_files_copied
    # since the set cannot have duplicate files this will ensure the test
    # accounts for duplicate file paths which we do not want.
    assert len(resulting_dst_file_paths) == len(set(resulting_dst_file_paths))


@pytest.fixture
def src_dir(tmp_path, num_files_on_disk):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    print(f"src directory is located at {src_dir}")
    write_test_jpg_files(src_dir, num_files_on_disk)
    write_test_filtered_files(src_dir, NUM_FILTERED_FILES)
    return src_dir


@pytest.fixture
def dst_dir(tmp_path):
    dst_dir = tmp_path / "dst"
    dst_dir.mkdir()
    print(f"dst directory is located at {dst_dir}")
    return dst_dir


def write_test_jpg_files(dir, num_files):
    for i in range(num_files):
        file_path = dir / f"black_jpg_{i}.jpg"
        with open(file_path, "wb") as file:
            file.write(SMALL_JPG)


def write_test_filtered_files(dir, num_files):
    for i in range(num_files):
        file_path = dir / f"random_file_{i}.txt"
        with open(file_path, "w") as file:
            file.write("random giberish")


def get_resulting_dst_file_paths(dst_dir):
    resulting_dst_file_paths = []
    for root, _, files in os.walk(dst_dir):
        for file in files:
            resulting_dst_file_paths.append(os.path.join(root, file))
    return resulting_dst_file_paths


# fmt: off
SMALL_JPG = bytes(
    [
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46, 0x49, 0x46, 0x00, 0x01, 
        0x01, 0x01, 0x00, 0x48, 0x00, 0x48, 0x00, 0x00, 0xFF, 0xDB, 0x00, 0x43, 
        0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xC2, 0x00, 0x0B, 0x08, 0x00, 0x01, 
        0x00, 0x01, 0x01, 0x01, 0x11, 0x00, 0xFF, 0xC4, 0x00, 0x14, 0x10, 0x01, 
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        0x00, 0x00, 0x00, 0x00, 0xFF, 0xDA, 0x00, 0x08, 0x01, 0x01, 0x00, 0x01, 
        0x3F, 0x10,
    ]
)
