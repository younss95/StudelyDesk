from datetime import datetime
import click
import studelydesk.models as models
import tabulate


#  FICHIER CLI POUR GERER LES LIGNES DE COMMANDE
@click.group()
def cli():
    pass


@cli.command()
def init_db():
    models.init_db()


@cli.command()
@click.option("-t", "--title", prompt="Title")
@click.option("-de", "--description", prompt="Description")
@click.option("-n", "--name", prompt="Name")
@click.option("-da", "--date", prompt="Date")
@click.option("-s", "--status", prompt="Status")
@click.option("-t", "--title", prompt="Title")
@click.option("-p", "--priority", prompt="Priority")
def create(title: str, description: str, name: str, date: datetime, status: str, priority: str):
    try:
        models.create_entry(title, description, name, date, status, priority)
        click.echo("L'entrée a bien éte créee")
    except Exception as e:
        click.echo(f"Erreur: {e}")


@cli.command()
@click.option("--id", required=True, type=int)
def get(_id: int):
    click.echo(models.get_entry(_id))



@cli.command()
@click.option("--as-csv", is_flag=True, help="Export entries to csv")
def get_entries(as_csv: bool):
    entries = models.get_all_entries()

    if as_csv:
        click.echo(tabulate(entries, headers="keys"))
    else:
        # Display the entries in a table format
        table = [
            [entry.id, entry.name, entry.amount, entry.category] for entry in entries
        ]
        headers = ["ID", "Name", "Amount", "Category"]
        click.echo(tabulate(table, headers=headers, tablefmt="grid"))




@cli.command()
@click.option("--id", required=True, type=int)
def delete(_id: int):
    models.delete_entry(_id)

@cli.command()
@click.option("--id", required=True, type=int)
@click.option("-t", "--title", prompt="Title")
@click.option("-de", "--description", prompt="Description")
@click.option("-n", "--name", prompt="Name")
@click.option("-da", "--date", prompt="Date")
@click.option("-s", "--status", prompt="Status")
@click.option("-t", "--title", prompt="Title")
@click.option("-p", "--priority", prompt="Priority")
def update(_id: int, title: str, description: str, name: str, date: datetime, status: str, priority: str):
    models.update_entry(_id, title, description, name, date, status, priority)



@cli.command()
def init_db():
    """Initialiser la base de données."""
    models.init_db()
    click.echo("Base de données initialisée avec succès.")


if __name__ == "__main__":
    cli()
