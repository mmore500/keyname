# -*- coding: utf-8 -*-

"""Console script for keyname."""
import sys
import subprocess
import click
try:
    # "myapp" case
    from . import keyname as kn
    from . import version as knversion
except:
    # "__main__" case
    import keyname as kn
    import version as knversion


@click.group()
def main():
    pass

@main.command()
def version(args=None):
    """Print version information and exit."""
    click.echo( knversion.__version__ )
    return 0

@main.command()
@click.option('--mkdir', is_flag=True)
def chop(mkdir):
    """Combine option-argument pairs into a keyname string."""
    click.echo( kn.chop(input(), mkdir=mkdir) )
    return 0

@main.command()
def rejoin():
    """Combine option-argument pairs into a keyname string."""
    click.echo( kn.rejoin(input()) )
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

@main.command()
@click.option('--copy/--move', default=True)
@click.option('--keep/--drop', default=True)
@click.argument('target', nargs=1)
@click.argument('keys', nargs=-1)
def stash(copy, keep, target, keys):
    """Rename target, writing dropped key-value pairs to a metadata file."""
    dest = subprocess.run(
        " ".join([
            "echo", target,
            "|",
            "keyname", "keep" if keep else "drop",
        ] + list(keys)),
        shell=True,
        stdout=subprocess.PIPE,
    ).stdout.decode('utf-8').rstrip("\n")
    stash = subprocess.run(
        " ".join([
            "echo", target,
            "|",
            "keyname", "keep" if not keep else "drop",
        ] + list(keys)),
        shell=True,
        stdout=subprocess.PIPE,
    ).stdout.decode('utf-8').rstrip("\n")

    subprocess.run([
        "cp" if copy else "mv", target, dest
    ], stdout=subprocess.DEVNULL)
    click.echo("created data file " + dest)

    subprocess.run(" ".join([
        "echo", stash,
        ">", dest + ".meta"
    ]), shell=True, stdout=subprocess.DEVNULL)
    click.echo("created metadata file " + dest + ".meta")

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
