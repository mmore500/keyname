#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `keyname` package."""


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


    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'Usage' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
