import click

@click.group()
def cli():
    """A secure password manager CLI tool."""
    pass


@cli.command()
@click.argument("service_name", type=str)
@click.option("-g", "--generate", is_flag=True, 
              help="Generate a strong password instead of prompting for manual entry.")
def add(service_name, generate):
    """
    Creates a new entry in the database. 
    Prompts user for username/email and if they want to generate a password or enter one themselves.
    """
    username = click.prompt("Enter username/email", type=str)

    if generate:
        password = "generatedTestPassword123"
        click.echo(f"Generated password for '{service_name}': {password}")
    else:
        password = click.prompt("Enter password", hide_input=True, confirmation_prompt=True)
    
    url = click.prompt("Enter url (optional)", type=str, default="null", show_default=False)
    note = click.prompt("Enter note (optional)", type=str, default="null", show_default=False)
    
    if click.confirm(f"Ready to securely save the entry for '{service_name}'?"):
        #db.add(username, password, url, note)
        click.echo(f"Entry for '{service_name}' saved successfully.")
    else:
        click.echo("Operation cancelled.")

@cli.command()
@click.argument("service_name", type=str, required=False)
@click.option("-l", "--list", "list-all", help="List all stored entry names.", is_flag=True)
def view(service_name, list_all):
    """
    Retrieve an entry using the service name or list all service names stored in the database.
    """
    
    if list_all:
        click.echo(f"Retrieving all entry names.")
        #db.view_all()
    else:
        click.echo(f"Retrieving credentials for: {service_name}")
        #db.view(service_name)


@cli.command()
@click.argument("service_name", type=str)
@click.option("-g", "--generate")
def update(service_name, generate):
    """
    Update the password for an entry. Option to generate a new password.
    """
    
    if generate:
        password = "updatedPassword123"
        click.echo(f"Generated password for '{service_name}': {password}")
    else:
        password = click.prompt("Enter password", hide_input=True, confirmation_prompt=True)
    
    if click.confirm(f"Ready to securely save the new password for '{service_name}'?"):
        #db.update(service_name, password)
        click.echo(f"Password for '{service_name}' saved successfully.")
    else:
        click.echo("Operation cancelled.")
    
@cli.command()
@click.argument("service_name", type=str)
def delete(service_name):
    """
    Delete an entry.
    """

    if click.confirm(f"Ready to securely delete the entry for: {service_name}?"):
        #db.delete(service_name)
        click.echo(f"{service_name} successfully deleted.")
    else:
        click.echo("Operation cancelled.")

cli()

