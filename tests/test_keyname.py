#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `keyname` package."""


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
        name = "path/seed=100+foobar=20+_hash=asdf+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        name = "~/more=path/+blah/seed=100+foobar=20+_hash=asdf+ext=.txt"
        goal['_'] = name
        assert kn.unpack(name) == goal
        goal.pop('_')
        assert kn.unpack(name, source_attr=False) == goal

        name = "just/a/regular/file.pdf"
        assert kn.unpack(name) == {
            'file.pdf' : '',
            '_' : 'just/a/regular/file.pdf'
        }
        assert kn.unpack(name, source_attr=False) == {
            'file.pdf' : '',
        }

        name = "key/with/no+=value/file+ext=.pdf"
        assert kn.unpack(name) == {
            'file' : '',
            'ext' : '.pdf',
            '_' : 'key/with/no+=value/file+ext=.pdf'
        }
        assert kn.unpack(name, source_attr=False) == {
            'file' : '',
            'ext' : '.pdf',
        }

        name = "multiple/=s/file=biz=blah+ext=.pdf"
        assert kn.unpack(name) == {
            'file' : 'biz=blah',
            'ext' : '.pdf',
            '_' : 'multiple/=s/file=biz=blah+ext=.pdf'
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
             '_' : 'path/seed=100+foobar=20+_hash=asdf+ext=.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : '~/more=path/+blah/seed=100+foobar=20+_hash=asdf+ext=.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kn.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt',
             '_' : '"whatever+=/"'
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
             '_' : '~/more=path/+blah/seed=100+foobar=20+_hash=asdf+ext=.txt'
         })) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        packed = kn.pack({
              'seed' : '100' * 100,
              'foobar' : '20',
              '_hash' : 'asdf',
              'ext' : '.txt',
              '_' : '~/more=path/+blah/seed=100+foobar=20+_hash=asdf+ext=.txt'
          })
        chopped = kn.chop(packed, mkdir=True)

        assert all(len(path_part) < 204 for path_part in chopped.split("/"))
        assert chopped == "foobar=20+seed=10010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010010.../0100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100100+_hash=asdf+ext=.txt"

        assert kn.rejoin(chopped) == packed

        with open(chopped, "w+") as file:
            file.write("should work")

        path_packed = f"{tempfile.mkdtemp()}/{'baz' * 100}/{packed}"
        path_chopped = kn.chop(path_packed, mkdir=True)
        assert all(
            len(path_part) < 204 for path_part in path_chopped.split("/")
        )

        with open(path_chopped, "w+") as file:
            file.write("should work")

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
