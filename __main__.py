import click
import piman


@click.group()
def cli():
    pass


@cli.command()
def server():
    piman.server()


@cli.command()
@click.argument('switch_address')
@click.argument('ports', nargs=-1)
def restart(switch_address, ports):
    piman.restart(switch_address, ports)


@cli.command()
@click.argument('switch_address')
@click.argument('port')
def reinstall(switch_address, port):
    piman.reinstall(switch_address, port)
    
@cli.command()
@click.argument('port', nargs = -1)
def mapper(port):
    piman.mapper(port)

@cli.command()
def power_cycle():
    power_cycle.power_cycle(10)
    server()


@cli.command()
@click.argument('name')
@click.argument('configpath')
@click.argument('hostcsvpath')
def config(name, configpath, hostcsvpath):
    piman.config_ui(name, configpath, hostcsvpath)


if __name__ == "__main__":
    cli()
