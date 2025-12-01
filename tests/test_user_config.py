import configparser

from keepr.user_config import initialise_user_config, set_default_user_config_values

# --- Arrange: Organise test data  ---
EXPECTED_SECTIONS = [
    "SESSION_CONFIG",
    "PASSWORD_CONFIG",
    "COLOR_SCHEME_CONFIG",
]

EXPECTED_DEFAULT_VALUES = {
    "SESSION_CONFIG": {
        "SESSION_TIMEOUT_SECONDS": "3600",
    },
    "PASSWORD_CONFIG": {
        "PASSWORD_GENERATOR_LENGTH": "20",
        "PASSWORD_GENERATOR_SPECIAL_CHARS": "!@#$^&*",
    },
    "COLOR_SCHEME_CONFIG": {
        "COLOR_ERROR": "red",
        "COLOR_SUCCESS": "green",
        "COLOR_PROMPT": "cyan",
        "COLOR_WARNING": "yellow",
        "COLOR_HEADER": "magenta",
        "COLOR_SENSITIVE_DATA": "green",
        "COLOR_NON_SENSITIVE_DATA": "white",
    },
}


def test_set_default_user_config_structure():
    """
    Test the default user config structure is correct.
    """

    # --- Act: Obtain the default values for user config ---
    user_config = set_default_user_config_values()

    # --- Assert: Check the user_config is a configparser object ---
    assert isinstance(user_config, configparser.ConfigParser), (
        "The function should return a configparser.ConfigParser object."
    )

    # --- Assert: Check the configparser object contains all expected sections ---
    for section in EXPECTED_SECTIONS:
        assert section in user_config, (
            f"The section '{section}' should exist in the user config file."
        )


def test_set_default_user_config_values():
    """
    Test the default values for the user config are set correctly.
    """

    # --- Act: Obtain the default values for user config ---
    user_config = set_default_user_config_values()

    # --- Assert: Check the expected key holds the expected default value ---
    for section, expected_keys in EXPECTED_DEFAULT_VALUES.items():
        for key, expected_value in expected_keys.items():
            actual_value = user_config[section][key]

            assert actual_value == expected_value, (
                f"Mismatch in [{section}] {key}: Expected '{expected_value}', got '{actual_value}'"
            )


def test_initialise_user_config(tmp_path):
    """
    Test if the user config file is correctly initialised.
    """

    # --- Arrange: Set tmp path for test config file ---
    config_file_path = tmp_path / "user_config.ini"

    # --- Assert: The file should not already exist ---
    assert not config_file_path.exists(), "The user config file should not exist."

    # --- Act: Initialise tmp config file ---
    initialise_user_config(config_file_path)

    # --- Assert: The tmp config file should now exist ---
    assert config_file_path.exists(), "The user config file should exist."

    # --- Act: Get the contents of the tmp config file ---
    tmp_config = configparser.ConfigParser()
    tmp_config.read(config_file_path)

    # --- Assert: Check the contents of the tmp config file are correct ---
    for section, expected_keys in EXPECTED_DEFAULT_VALUES.items():
        for key, expected_value in expected_keys.items():
            actual_value = tmp_config[section][key]

            assert actual_value == expected_value, (
                f"Mismatch in [{section}] {key}: Expected '{expected_value}', got '{actual_value}'"
            )


def test_initialise_user_config_skip(tmp_path):
    """
    Test if the user config skips creating a new file, if a config file already exists.
    We can test this by setting placeholder content, and then checking before and
    after the function call if the placeholder content has changed.
    The function call will create a new file with default values, which will change the
     content, if the file creation is not skipped
    """

    # --- Arrange: Setup tmp config file with testable content ---
    config_file_path = tmp_path / "user_config.ini"
    content = "[SESSION_CONFIG]\nsession_timeout_seconds = 9999\n"
    config_file_path.write_text(content)

    # --- Assert: Check the config file exists and contains the placeholder content ---
    assert config_file_path.read_text() == content, (
        "The config file exists and contains the original content."
    )

    # --- Act: Call the initialise function ---
    initialise_user_config(config_file_path)

    # --- Assert: Check if the file contents have been changed ---
    assert config_file_path.read_text() == content, (
        "The config file creation was not skipped."
    )
