import configparser

from keepr.user_config import set_default_user_config_values

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
