#!/usr/bin/env python3
# -*- coding: utf8 -*-


import hashlib
import os
import sys
from pathlib import Path

import click


class UIDFieldExistsError(ValueError):
    pass


class VERSIONFieldMissingError(ValueError):
    pass


def vd(*,
       ctx,
       verbose: bool,
       debug: bool,
       ):

    ctx.ensure_object(dict)
    if verbose:
        ctx.obj['verbose'] = verbose
    try:
        verbose = ctx.obj['verbose']
    except KeyError:
        ctx.obj['verbose'] = verbose

    if debug:
        ctx.obj['debug'] = debug
    try:
        debug = ctx.obj['debug']
    except KeyError:
        ctx.obj['debug'] = debug

    return verbose, debug


def insert_uid(record: str,
               verbose: bool,
               debug: bool,
               ):

    uid = getattr(hashlib, 'sha3_256')(record.encode('utf8')).digest().hex()
    if verbose:
        print(f"{uid=}", file=sys.stderr)

    version_index = None
    record_list = record.splitlines()
    for item in record_list:
        if item.startswith('UID:'):
            raise UIDFieldExistsError(record)

        if item.startswith('VERSION:'):
            if item.split(':')[-1] == "2.1":
                print("WARNING: VERSION 2.1 VCard detected, it is recommended to convert the input file to version 3 with https://github.com/jowave/vcard2to3 before using this tool.", file=sys.stderr)
            version_index = record_list.index(item)

    if version_index is None:
        raise VERSIONFieldMissingError(record)

    record_list.insert(version_index + 1, "UID:{}".format(uid))

    return '\n'.join(record_list)


def vcf_split(*,
              path: Path,
              output_dir: Path,
              verbose: bool,
              debug: bool,
              ):

    path = Path(path).resolve()
    output_dir = Path(output_dir).resolve()

    if verbose:
        print(f"{path=}", file=sys.stderr)
        print(f"{output_dir=}", file=sys.stderr)

    if not output_dir.exists():
        raise ValueError('output_dir: {} does not exist'.format(output_dir))

    if not output_dir.is_dir():
        raise ValueError('output_dir: {} exists but is not a directory'.format(output_dir))

    with open(path, 'r', encoding='utf8') as vcfh:
        vcf_content = vcfh.read()

    record_list = ''.join(list(vcf_content)).split('BEGIN:VCARD')
    record_list = [record for record in record_list if record]
    record_count = len(record_list)
    if verbose:
        print(f"{record_count=}", file=sys.stderr)

    os.chdir(output_dir)
    for index, record in enumerate(record_list):
        try:
            record = insert_uid(record, verbose=verbose, debug=debug)
        except UIDFieldExistsError:
            pass
        output_file = path.name + '__' + str(index + 1).zfill(len(str(record_count + 1))) + '.vcf'
        with open(output_file, 'x', encoding='utf8') as fh:
            fh.write('BEGIN:VCARD' + record)


@click.group()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.pass_context
def cli(ctx,
        verbose: bool,
        debug: bool,
        ):

    verbose, debug = vd(ctx=ctx,
                        verbose=verbose,
                        debug=debug,)


@cli.command()
@click.argument("vcf_file",
                type=click.Path(exists=True,
                                dir_okay=False,
                                file_okay=True,
                                allow_dash=False,
                                path_type=Path,),
                nargs=1,
                required=True,)
@click.argument("output_dir",
                type=click.Path(exists=True,
                                dir_okay=True,
                                file_okay=False,
                                allow_dash=False,
                                path_type=Path,),
                nargs=1,
                required=True,)
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.pass_context
def split(ctx,
          vcf_file: Path,
          output_dir: Path,
          verbose: bool,
          debug: bool,
          ):

    verbose, debug = vd(ctx=ctx,
                        verbose=verbose,
                        debug=debug,)

    vcf_split(path=vcf_file,
              output_dir=output_dir,
              verbose=verbose,
              debug=debug,)

# todo add convert() https://github.com/jowave/vcard2to3
