import pytest
import main


def test_parse_args_returns_correct_verbosity_when_a_long_multiple():
    returned_args = main.parse_args(
        [
            "/some/directory",
            "/another_directory",
            "--verbosity",
            "--verbosity",
            "--verbosity",
        ]
    )

    assert returned_args.verbosity == 3


def test_parse_args_returns_correct_verbosity_when_a_multiple():
    returned_args = main.parse_args(
        [
            "/some/directory",
            "/another_directory",
            "-vvv",
        ]
    )

    assert returned_args.verbosity == 3


def test_parse_args_returns_correct_verbosity_when_long():
    returned_args = main.parse_args(
        [
            "/some/directory",
            "/another_directory",
            "--verbosity",
        ]
    )

    assert returned_args.verbosity == 1


def test_parse_args_returns_correct_verbosity_when_present():
    returned_args = main.parse_args(
        [
            "/some/directory",
            "/another_directory",
            "-v",
        ]
    )

    assert returned_args.verbosity == 1


def test_parse_args_returns_correct_default_verbosity():
    returned_args = main.parse_args(["/some/directory", "/another_directory"])

    assert returned_args.verbosity == 0


def test_parse_args_returns_num_requested_files_when_short():
    returned_args = main.parse_args(
        ["/some/directory", "/another/directory", "-n", "10"]
    )

    assert returned_args.num_requested_files == 10


def test_parse_args_returns_num_requested_files_when_long():
    returned_args = main.parse_args(
        ["/some/directory", "/another/directory", "--num_requested_files", "25"]
    )

    assert returned_args.num_requested_files == 25


def test_parse_args_returns_none_num_requested_files_when_not_present():
    returned_args = main.parse_args(
        [
            "/some/directory",
            "/another/directory",
        ]
    )

    assert returned_args.num_requested_files is None


def test_parse_args_returns_when_src_and_dst_directories_are_present():
    main.parse_args(
        [
            "/some/directory",
            "/another/directory",
        ]
    )


def test_parse_args_fails_when_source_root_directory_is_missing():
    with pytest.raises(SystemExit):
        main.parse_args({"destination_directory": "/another/directory"})


def test_parse_args_fails_when_destination_directory_is_missing():
    with pytest.raises(SystemExit):
        main.parse_args({"source_root_directory": "/some/directory"})


def test_parse_args_fails_when_all_cli_args_are_missing():
    with pytest.raises(SystemExit):
        main.parse_args({})
