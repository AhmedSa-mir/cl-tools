#!/usr/bin/env python3

from Jumpscale import j
import click

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--lines', '-l', is_flag=True, default=False, help='Get number of lines in the file')
@click.option('--words', '-w', is_flag=True, default=False, help='Get number of words in the file')
@click.option('--chars', '-c', is_flag=True, default=False, help='Get number of characters in the file')
def wordcount(path, lines, words, chars):
    """wc command using click library and JSX SALS"""
    
    file_content = j.sal.fs.readFile(path)
    no_options = False

    if not lines and not words and not chars:
        no_options = True
    if no_options or lines:
        # the trailing 1 is the last line (doesn't have \n at the end)
        lines_cnt = file_content.count('\n') + 1
        click.echo(f"Lines: {lines_cnt}")
    if no_options or words:
        # the trailing 1 is the last word
        words_cnt = file_content.count(" ") + file_content.count('\n') + 1
        click.echo(f"Words: {words_cnt}")
    if no_options or chars:
        click.echo(f"Characters: {len(file_content)}")

if __name__ == "__main__":
    wordcount()