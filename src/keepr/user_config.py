import configparser
import sys

import click


def set_default_user_config_values():
    """
    Sets default user config values.
    """
    user_config = configparser.ConfigParser()
    # --- SESSION CONFIG ---
    user_config["SESSION_CONFIG"] = {}
    user_config["SESSION_CONFIG"]["SESSION_TIMEOUT_SECONDS"] = "3600"

    # --- PASSWORD CONFIG ---
    user_config["PASSWORD_CONFIG"] = {}
    user_config["PASSWORD_CONFIG"]["PASSWORD_GENERATOR_LENGTH"] = "20"
    user_config["PASSWORD_CONFIG"]["PASSWORD_GENERATOR_SPECIAL_CHARS"] = "!@#$^&*"

    # --- COLOR SCHEME CONFIG ---
    user_config["COLOR_SCHEME_CONFIG"] = {}
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_ERROR"] = "red"
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_SUCCESS"] = "green"
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_PROMPT"] = "cyan"
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_WARNING"] = "yellow"
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_HEADER"] = "magenta"
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_SENSITIVE_DATA"] = "green"
    user_config["COLOR_SCHEME_CONFIG"]["COLOR_NON_SENSITIVE_DATA"] = "white"

    return user_config


def initialise_user_config(user_config_file_path):
    """
    Initialise the user config file.
    """
    user_config = set_default_user_config_values()
    if not user_config_file_path.exists():
        try:
            with open(user_config_file_path, "w") as config_file:
                user_config.write(config_file)
        except Exception as e:
            click.secho(
                f"Critical error: Failed to initialise user configuration file '{user_config_file_path}'. Details: {e}",
                fg="red",
                bold=True,
            )
            sys.exit(1)
