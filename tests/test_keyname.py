#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests for `keyname` package."""


import os
from pathlib import Path
import tempfile
import unittest
from click.testing import CliRunner

from keyname import keyname as kn
from keyname import cli


class TestKeyname(unittest.TestCase):
    """Tests for `keyname` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_unpack(self):
        """Test unpacking."""
        goal = {
            'seed' : '100',
            'foobar' : '20',
            '_hash' : 'asdf',
            'ext' : '.txt'
        }

        name = "seed=100+foobar=20+_hash=asdf+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        # reorderings
        name = "foobar=20+seed=100+_hash=asdf+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        name = "_hash=asdf+foobar=20+seed=100+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        # should ignore path
        name = f"path{os.sep}seed=100+foobar=20+_hash=asdf+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        name = f"~{os.sep}more=path{os.sep}+blah{os.sep}seed=100+foobar=20+_hash=asdf+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        name = f"just{os.sep}a{os.sep}regular{os.sep}file.pdf"
        assert kn.unpack(name) == {
            'file.pdf' : '',
            '_' : f'just{os.sep}a{os.sep}regular{os.sep}file.pdf'
        }
        assert kn.unpack(name, source_attr=False) == {
            'file.pdf' : '',
        }

        name = f"key{os.sep}with{os.sep}no+=value{os.sep}file+ext=.pdf"
        assert kn.unpack(name) == {
            'file' : '',
            'ext' : '.pdf',
            '_' : f'key{os.sep}with{os.sep}no+=value{os.sep}file+ext=.pdf'
        }
        assert kn.unpack(name, source_attr=False) == {
            'file' : '',
            'ext' : '.pdf',
        }

        name = f"multiple{os.sep}=s{os.sep}file=biz=blah+ext=.pdf"
        assert kn.unpack(name) == {
            'file' : 'biz=blah',
            'ext' : '.pdf',
            '_' : f'multiple{os.sep}=s{os.sep}file=biz=blah+ext=.pdf'
        }
        assert kn.unpack(name, source_attr=False) == {
            'file' : 'biz=blah',
            'ext' : '.pdf',
        }


    def test_001_pack(self):
        """Test packing."""

        # reorderings
        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             '_hash' : 'asdf',
             'seed' : '100',
             'foobar' : '20',
             'ext' : '.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             '_hash' : 'asdf',
             'foobar' : '20',
             'ext' : '.txt',
             'seed' : '100'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        # different values
        assert kn.pack({
             'seed' : '100',
             'foobar' : 'blip',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "foobar=blip+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'seed' : 'a100',
             'foobar' : 'blip',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "foobar=blip+seed=a100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'aseed' : 'a100',
             'foobar' : 'blip',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "aseed=a100+foobar=blip+_hash=asdf+ext=.txt"

        # should ignore '_' key
        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : 'foobar=20+seed=100+_hash=asdf+ext=.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : f'path{os.sep}seed=100+foobar=20+_hash=asdf+ext=.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : f'~{os.sep}more=path{os.sep}+blah{os.sep}seed=100+foobar=20+_hash=asdf+ext=.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : f'"whatever+={os.sep}"'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        # missing extension
        assert kn.pack({
             '_hash' : 'asdf',
             'foobar' : '20',
             'seed' : '100',
         }) == "foobar=20+seed=100+_hash=asdf"

    def test_002_demote(self):
        """Test demoting."""

        assert kn.demote(
            "foobar=20+seed=100+_hash=asdf+ext=.txt"
        ) == "foobar%20~seed%100~_hash%asdf~ext%.txt"


    def test_003_promote(self):
        """Test promoting."""

        assert kn.promote(
            "foobar%20~seed%100~_hash%asdf~ext%.txt"
        ) == "foobar=20+seed=100+_hash=asdf+ext=.txt"


    def test_004_chop_rejoin(self):
        """Test chopping."""

        assert kn.chop(kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt'
         })) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.chop(kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : f'~{os.sep}more=path{os.sep}+blah{os.sep}seed=100+foobar=20+_hash=asdf+ext=.txt'
         })) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        packed = kn.pack({
              'seed' : '100' * 100,
              'foobar' : '20',
              '_hash' : 'asdf',
              'ext' : '.txt',
              '_' : f'~{os.sep}more=path{os.sep}+blah{os.sep}seed=100+foobar=20+_hash=asdf+ext=.txt'
          })
        chopped = kn.chop(packed, mkdir=True)
        assert not os.sep * 2 in chopped

        assert all(len(path_part) < 204 for path_part in chopped.split(os.sep))
        assert chopped == f"foobar=20+seed=10010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010{kn._ellipses()}{os.sep}0100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100+_hash=asdf+ext=.txt"

        assert kn.rejoin(chopped) == packed

        dirname = f"foobar=20+seed=10010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010{kn._ellipses()}"
        assert os.path.isdir(dirname)

        Path(dirname).touch()  # check file in dirmane
        Path(Path(dirname)/"example.txt").touch()  # check file in dirmane
        Path(os.path.basename(chopped)).touch()  # check basename is legal
        Path(chopped).touch()
        Path(chopped).unlink()
        Path(chopped).write_text("should work")
        assert Path(chopped).read_text() == "should work"

        path_packed = f"{tempfile.mkdtemp()}{os.sep}{'baz' * 100}{os.sep}{packed}"
        path_chopped = kn.chop(path_packed, mkdir=True)
        assert all(
            len(path_part) < 204 for path_part in path_chopped.split(os.sep)
        )

        Path(path_chopped).touch()
        Path(path_chopped).unlink()
        Path(path_chopped).write_text("should work")
        assert Path(chopped).read_text() == "should work"

        assert kn.rejoin(path_chopped) == path_packed


        packed = kn.pack(
            {**{'seed' : '100' * 60}, **{"ext" : ".buzzzz.baz.gz"}}
        )
        chopped = kn.chop(packed)
        assert chopped.endswith("+ext=.buzzzz.baz.gz")

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Usage' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
