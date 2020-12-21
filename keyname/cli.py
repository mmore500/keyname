# -*- coding: utf-8 -*-

"""Console script for keyname."""
import sys
import click
import keyname as kn

@click.group()
def main():
    pass

@main.command()
def version(args=None):
    """Print version information and exit."""
    click.echo( kn.__version__ )
    return 0

@main.command()
@click.argument('keys', nargs=-1)
def keep(keys):
    """Filter stdin keyname string to keep argument keys."""
    click.echo( kn.pack( {
        k : v for k, v in kn.unpack( input() ).items() if k in keys
    } ) )
    return 0

@main.command()
@click.argument('keys', nargs=-1)
def drop(keys):
    """Filter stdin keyname string to drop argument keys."""
    click.echo( kn.pack( {
        k : v for k, v in kn.unpack( input() ).items() if k not in keys
    } ) )
    return 0

@main.command(
    context_settings={
        'ignore_unknown_options' : True,
        'allow_extra_args' : True,
    },
)
@click.pass_context
def pack(ctx):
    """Combine option-argument pairs into a keyname string."""
    # adapted from https://stackoverflow.com/a/32946412
    click.echo( kn.pack({
        ctx.args[i][2:] : ctx.args[i+1]
        for i in range(0, len(ctx.args), 2)
    }) )
    return 0

@main.command()
def keys():
    """Print keys from stdin keyname string."""
    for k, v in kn.unpack( input() ).items():
        if '_' != k:
            click.echo( k )
    return 0

@main.command()
def vals():
    """Print values from stdin keyname string."""
    for k, v in kn.unpack( input() ).items():
        if '_' != k:
            click.echo( v )
    return 0

@main.command()
@click.argument('keys', nargs=-1)
def extract(keys):
    """Print values corresponding to keys in stdin keyname string."""
    keyname_attributes = kn.unpack( input() )
    for k in keys:
        if k in keyname_attributes:
            click.echo( keyname_attributes[ k ] )
    return 0

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
