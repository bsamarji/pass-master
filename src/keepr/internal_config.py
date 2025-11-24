import configparser
from pathlib import Path

from keepr.user_config import initialise_user_config

# --- APP FILE PATHS ---
APP_DIR_NAME = ".keepr"
USER_CONFIG_FILE_NAME = "config.ini"
DB_FILE_NAME = "keepr.db"
SECURITY_DIR_NAME = ".security"
SALT_FILE_NAME = "keepr.salt"
PEK_FILE_NAME = "keepr.key"

home_dir = Path.home()
user_config_file_path = home_dir / APP_DIR_NAME / USER_CONFIG_FILE_NAME
initialise_user_config(user_config_file_path)
config = configparser.ConfigParser()
config.read(user_config_file_path)

# --- COLOR SCHEME DEFINITIONS ---
COLOR_ERROR = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_ERROR"], bold=True)  # Critical failure, security warnings, irreversible actions
COLOR_SUCCESS = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_SUCCESS"], bold=True)  # Successful operation, generated passwords
COLOR_PROMPT_BOLD = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_PROMPT"], bold=True)  # Primary prompts (username, password)
COLOR_PROMPT_LIGHT = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_PROMPT"])  # Secondary/optional prompts (URL, note)
COLOR_WARNING = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_WARNING"])  # Non-fatal warnings, operation cancelled, secondary notes
COLOR_HEADER = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_HEADER"], bold=True)  # Table headers, main information headers
COLOR_SENSITIVE_DATA = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_SENSITIVE_DATA"])  # Highly sensitive data (passwords in view)
COLOR_NON_SENSITIVE_DATA = dict(fg=config["COLOR_SCHEME_CONFIG"]["COLOR_NON_SENSITIVE_DATA"])  # Non-sensitive primary data (timestamps, username)

# --- SESSION CONFIG ---
SESSION_FILE_NAME = "keepr.session"
SESSION_TIMEOUT_SECONDS = int(config["SESSION_CONFIG"]["SESSION_TIMEOUT_SECONDS"])

# --- COMMAND CONFIG ---
COMMANDS_VALID_NO_ARGS = ['list', 'login', 'logout', 'help']

# --- PASSWORD GENERATOR CONFIG ---
PASSWORD_GENERATOR_LENGTH = int(config["PASSWORD_CONFIG"]["PASSWORD_GENERATOR_LENGTH"])
PASSWORD_GENERATOR_SPECIAL_CHARS = config["PASSWORD_CONFIG"]["PASSWORD_GENERATOR_SPECIAL_CHARS"]
