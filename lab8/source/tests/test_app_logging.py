import logging

import app_logging


def test_configure_logging_creates_log_directory(tmp_path):
    log_file = tmp_path / "log" / "test.log"
    app_logging.configure_logging(log_file=log_file)

    assert log_file.parent.exists()


def test_configure_logging_adds_two_handlers(tmp_path):
    log_file = tmp_path / "log" / "test.log"
    app_logging.configure_logging(log_file=log_file)

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 2


def test_configure_logging_does_not_add_duplicate_handlers(tmp_path):
    log_file = tmp_path / "log" / "test.log"
    app_logging.configure_logging(log_file=log_file)
    app_logging.configure_logging(log_file=log_file)

    root_logger = logging.getLogger()
    assert len(root_logger.handlers) == 2


def test_get_logger_returns_logger_with_correct_name():
    logger = app_logging.get_logger("test_module")

    assert logger.name == "test_module"
