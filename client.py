import requests
import click

@click.group()
def cli():
    pass

@click.command()
def hello():
    click.echo("Hello World!")

@click.command()
def connect():
    click.echo("Connecting to bootstrap...")
    r = requests.get("http://192.168.0.2/test")
    click.echo("Returned this:")
    click.echo(r.text)

cli.add_command(hello)
cli.add_command(connect)

if __name__ == '__main__':
    cli()