#!/usr/bin/env python3

from Jumpscale import j
import click

@click.command()
@click.option('--pid', '-p', help='Get PID of process with this name')
@click.option('--name', '-n', help='Check whether a process with this name exists or not')
def list_processes(pid, name):
    """ps command using click library and JSX SALS"""
    
    if not pid and not name:
        rc, out, err = j.sal.process.execute("ps ax")
        click.echo(out)
    elif name:
        click.echo(j.sal.process.psfind(name))
    elif pid:
        click.echo(j.sal.process.getProcessPid(pid))

if __name__ == "__main__":
    list_processes()