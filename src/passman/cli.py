import click
import db
import tabulate


@click.group()
def cli():
    """
    PassMaster - A secure CLI password manager.
    """

    try:
        db.initialise_db()
    except Exception as e:
        click.echo(f"DB ERROR: {e}. Exiting program.", err=True)
        raise click.Abort()


@cli.command()
@click.argument("service_name", type=str)
@click.option(
    "-g",
    "--generate",
    is_flag=True,
    help="Generate a strong password instead of prompting for manual entry.",
)
def add(service_name, generate):
    """
    Creates a new entry in the database.
    Prompts user for username/email, password, url and note.
    Prompts user to confirm the new entry and save it into database.
    """
    username = click.prompt("Enter username/email", type=str)

    if generate:
        password = "generatedTestPassword123"
        click.echo(f"Generated password for '{service_name}': {password}")
    else:
        password = click.prompt(
            "Enter password", hide_input=True, confirmation_prompt=True
        )

    url = click.prompt(
        "Enter url (optional)", type=str, default="null", show_default=False
    )
    note = click.prompt(
        "Enter note (optional)", type=str, default="null", show_default=False
    )

    if click.confirm(f"Ready to securely save the entry for '{service_name}'?"):
        try:
            db.add_entry(service_name, username, password, url, note, 1)
            click.echo(f"Entry for '{service_name}' saved successfully.")
        except Exception as e:
            print(f"DB ERROR: {e}")
            click.Abort()
    else:
        click.echo("Operation cancelled.")


@cli.command()
@click.argument("service_name", type=str)
def view(service_name):
    """
    Retrieve an entry with sensitive info from the database.
    Display the entry in a beautiful table.
    """
    try:
        click.echo(f"Retrieving credentials for: {service_name}")
        row = db.view_entry(service_name)
        display_table = tabulate.tabulate(
            row,
            headers=[
                "service_name",
                "username",
                "password",
                "url",
                "note",
                "created_at",
                "updated_at",
            ],
            tablefmt="rounded_grid",
        )
        click.echo(display_table)
    except Exception as e:
        click.echo(f"DB ERROR: {e}")
        click.Abort()


@cli.command()
@click.argument("search_term", type=str)
def search(search_term):
    """
    Retrieve entries with non-sensitive info matching on a search term from the database.
    Display entries in a beautiful table.
    Usernames and passwords are not retrieved. 
    User must use the 'view' command to retrieve sensitive information.
    """
    try:
        click.echo(
            f"Retrieving entries with service names that contain the search term: {search_term}"
        )
        rows = db.search(search_term)
        display_table = tabulate.tabulate(
            rows,
            headers=[
                "service_name",
                "url",
                "note",
                "created_at",
                "updated_at",
            ],
            tablefmt="rounded_grid",
        )
        click.echo(display_table)
    except Exception as e:
        click.echo(f"DB ERROR: {e}")
        click.Abort()


@cli.command()
def list():
    """
    Retrieve all entries with non-sensitive info from the database.
    Display entries in a beautiful table.
    Usernames and passwords are not retrieved. 
    User must use the 'view' command to retrieve sensitive information.
    """
    try:
        click.echo(
            f"Retrieving all entries."
        )
        rows = db.list()
        display_table = tabulate.tabulate(
            rows,
            headers=[
                "service_name",
                "url",
                "note",
                "created_at",
                "updated_at",
            ],
            tablefmt="rounded_grid",
        )
        click.echo(display_table)
    except Exception as e:
        click.echo(f"DB ERROR: {e}")
        click.Abort()


@cli.command()
@click.argument("service_name", type=str)
@click.option(
    "-g",
    "--generate",
    is_flag=True,
    help="Generate a strong password instead of prompting for manual entry.",
)
def update(service_name, generate):
    """
    Update the password for an entry in the database.
    Prompts user to confirm password update.
    """

    if generate:
        password = "updatedPassword123"
        click.echo(f"Generated new password for '{service_name}': {password}")
    else:
        password = click.prompt(
            f"Enter new password for {service_name}",
            hide_input=True,
            confirmation_prompt=True,
        )

    if click.confirm(f"Ready to securely save the new password for '{service_name}'?"):
        try:
            db.update_entry(service_name, password)
            click.echo(f"Password for '{service_name}' saved successfully.")
        except Exception as e:
            print(f"DB ERROR: {e}")
            click.Abort()
    else:
        click.echo("Operation cancelled.")


@cli.command()
@click.argument("service_name", type=str)
def delete(service_name):
    """
    Delete an entry in the database.
    Prompts user to confirm deletion.
    """

    if click.confirm(f"Ready to securely delete the entry for: {service_name}?"):
        try:
            db.delete_entry(service_name)
            click.echo(f"{service_name} successfully deleted.")
        except Exception as e:
            print(f"DB ERROR: {e}")
            click.Abort()
    else:
        click.echo("Operation cancelled.")


cli()
