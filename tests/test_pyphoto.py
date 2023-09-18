import pytest
import main
import os

PARAMS = [
    (0, 10, 0),  # no files on disk
    (50, 10, 10),  # more files on disk than requested
    (10, 25, 10),  # fewer files on disk than requested
    (25, 25, 25),  # same number of files on disk as were requested
]


@pytest.mark.parametrize(
    "num_files_on_disk, num_files_requested, expected_files_copied", PARAMS
)
def test_copy_no_files_when_no_files_exist(
    tmp_path, num_files_on_disk, num_files_requested, expected_files_copied
):
    """
    Ensure the correct number of files are copied to the destination directory
    given the state of the files on disk and the number of files requested by
    the user.
    """
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    print(f"tmp directory is located at {tmp_path}")
    write_test_jpg_files(src_dir, num_files_on_disk)
    write_test_filtered_files(src_dir, 100)
    dst_dir = tmp_path / "dst"
    main.get_random_files(src_dir, num_files_requested, dst_dir)
    resulting_dst_file_paths = []
    for root, _, files in os.walk(dst_dir):
        for file in files:
            resulting_dst_file_paths.append(os.path.join(root, file))

    assert len(resulting_dst_file_paths) == expected_files_copied


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


SMALL_JPG = bytes(
    [
        0xFF,
        0xD8,
        0xFF,
        0xE0,
        0x00,
        0x10,
        0x4A,
        0x46,
        0x49,
        0x46,
        0x00,
        0x01,
        0x01,
        0x01,
        0x00,
        0x48,
        0x00,
        0x48,
        0x00,
        0x00,
        0xFF,
        0xDB,
        0x00,
        0x43,
        0x00,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xC2,
        0x00,
        0x0B,
        0x08,
        0x00,
        0x01,
        0x00,
        0x01,
        0x01,
        0x01,
        0x11,
        0x00,
        0xFF,
        0xC4,
        0x00,
        0x14,
        0x10,
        0x01,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0xFF,
        0xDA,
        0x00,
        0x08,
        0x01,
        0x01,
        0x00,
        0x01,
        0x3F,
        0x10,
    ]
)
