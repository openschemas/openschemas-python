#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openschemas` package."""

from openschemas.main.map2model import main
import unittest
import shutil
import tempfile
import os
import sys

test_dir = os.path.abspath(os.path.dirname(__file__))

class TestMap2Model(unittest.TestCase):
    """Tests for `openschemas` map2model package."""

    def setUp(self):
        self.specs = '%s/specifications' % test_dir
        self.config = '%s/configuration.yml' % self.specs
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        shutil.rmtree(self.tmpdir)

    def test_run(self):
        """Test that the markdown is loaded fully"""
        spec_parser = main(config_yml=self.config,
                           folder=self.specs,
                           output=self.tmpdir)

        print("Files produced:")
        folders = os.listdir(self.tmpdir)
        print(folders)
        for folder in ['Container', 'DataCatalog']:
            assert(folder in folders) 

        print("Content Produced in Container")
        contents = os.listdir('%s/Container' % self.tmpdir)
        print(contents)
        for content in ['examples', 'README.md', 
                        'Container.html', 'Container.yml']:
             assert(content in contents) 

