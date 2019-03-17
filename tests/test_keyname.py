#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `keyname` package."""


import unittest
from click.testing import CliRunner

from keyname import keyname as kf
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
        assert kf.unpack("seed=100+foobar=20+_hash=asdf+ext=.txt") == goal

        # reorderings
        assert kf.unpack("foobar=20+seed=100+_hash=asdf+ext=.txt") == goal
        assert kf.unpack("_hash=asdf+foobar=20+seed=100+ext=.txt") == goal

        # missing and extra
        assert kf.unpack("seed=100+_hash=asdf+ext=.txt") != goal
        assert kf.unpack("seed=100+bz=bp+foobar=20+_hash=asdf+ext=.txt") != goal

        # changed values
        assert kf.unpack("seed=10+foobar=20+_hash=asdf+ext=.txt") != goal
        assert kf.unpack("sed=100+foobar=20+_hash=asdf+ext=.txt") != goal
        assert kf.unpack("sed=100+foobar=20+hash=asdf+ext=.txt") != goal

        # should ignore path
        assert kf.unpack("path/seed=100+foobar=20+_hash=asdf+ext=.txt") == goal
        assert kf.unpack(
            "~/more=path/+blah/seed=100+foobar=20+_hash=asdf+ext=.txt") == goal

    def test_001_pack(self):
        """Test packing."""

        # reorderings
        assert kf.pack({
             'seed' : '100',
             'foobar' : '20',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kf.pack({
             '_hash' : 'asdf',
             'seed' : '100',
             'foobar' : '20',
             'ext' : '.txt'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        assert kf.pack({
             '_hash' : 'asdf',
             'foobar' : '20',
             'ext' : '.txt',
             'seed' : '100'
         }) == "foobar=20+seed=100+_hash=asdf+ext=.txt"

        # different values
        assert kf.pack({
             'seed' : '100',
             'foobar' : 'blip',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "foobar=blip+seed=100+_hash=asdf+ext=.txt"

        assert kf.pack({
             'seed' : 'a100',
             'foobar' : 'blip',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "foobar=blip+seed=a100+_hash=asdf+ext=.txt"

        assert kf.pack({
             'aseed' : 'a100',
             'foobar' : 'blip',
             '_hash' : 'asdf',
             'ext' : '.txt'
         }) == "aseed=a100+foobar=blip+_hash=asdf+ext=.txt"

        # missing extension
        assert kf.pack({
             '_hash' : 'asdf',
             'foobar' : '20',
             'seed' : '100',
         }) == "foobar=20+seed=100+_hash=asdf+ext=None"



    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'keyname.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
