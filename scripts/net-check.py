#!/usr/bin/env python3

from Jumpscale import j
import click

@click.command()
@click.option('--listen', '-l', help='Check if port is listening on the system.')
@click.option('--info', '-i', is_flag=True, help='Get network info')
@click.option('--ip', help='Get list of IPs assigned to an interface')
@click.option('--hostname', is_flag=True, help='Get hostname of this machine')
@click.option('--ping', help='Ping a machine to check if it\'s up and accessible')
def netcheck(listen, info, ip, hostname, ping):
    """netstat command using click library and JSX SALS"""
    
    if listen:
        click.echo(j.sal.nettools.checkListenPort(int(listen)))
    elif ip:
        click.echo(j.sal.nettools.getIpAddress(ip))
    elif hostname:
        click.echo(j.sal.nettools.getHostname())
    elif ping:
        ip = j.sal.nettools.getHostByName(ping)
        click.echo(j.sal.nettools.pingMachine(ip))
    else:
        click.echo(j.sal.nettools.networkinfo_get())

if __name__ == "__main__":
    netcheck()