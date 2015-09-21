"""Interoperability tests for ProvStore.
"""
# Copyright (c) 2015 University of Southampton
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions: 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software. 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE. 

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect
import os

from nose.tools import istest

from prov_interop.interop_tests.test_converter import ConverterTestCase
from prov_interop_provstore.converter import ProvStoreConverter

@istest
class ProvStoreTestCase(ConverterTestCase):
  """Interoperability tests for ProvStore.
  
  Its configuration, loaded via
  :meth:`prov_interop.interop_tests.test_converter.ConverterTestCase.get_configuration`,
  is expected to be in a YAML file: 
  
  - Either provided as the value of a ``ProvStore`` key in the
    :class:`prov_interop.harness.HarnessResource` configuration. 
  - Or, named in an environment variable, 
    ``PROVSTORE_TEST_CONFIGURATION``.
  - Or, ``provstore.yaml``, co-located with this Python file.

  The configuration itself, within this file, is expected to have the
  key `ProvStore``. 

  A valid YAML configuration file is::

    ---
    ProvStore:
      url: https://provenance.ecs.soton.ac.uk/store/api/v0/documents/
      authorization: ApiKey user:12345qwerty
      input-formats: [provn, ttl, trig, provx, json]
      output-formats: [provn, ttl, trig, provx, json]
      skip-tests: []

  An API key can also be provided via an environment variable. If the
  environment variable ``PROVSTORE_API_KEY`` is set then this is
  assumed to hold a ProvStore user name and API key
  e.g. ``user:12345qwert``. If not set, then the user name and API key
  provided in the configuration is used.
  """

  CONFIGURATION_FILE_ENV = "PROVSTORE_TEST_CONFIGURATION"
  """str or unicode: environment variable holding configuration file name  
  """

  API_KEY_ENV = "PROVSTORE_API_KEY"
  """str or unicode: environment variable holding ProvStore API key
  """

  DEFAULT_CONFIGURATION_FILE="provstore.yaml"
  """str or unicode: default configuration file name
  """

  CONFIGURATION_KEY="ProvStore"
  """str or unicode: key for ProvStore configuration in configuration
  file"""

  def setUp(self):
    super(ProvStoreTestCase, self).setUp()
    self.converter = ProvStoreConverter()
    config_file = os.path.join(
      os.path.dirname(os.path.abspath(inspect.getfile(
        inspect.currentframe()))), ProvStoreTestCase.DEFAULT_CONFIGURATION_FILE)
    config = super(ProvStoreTestCase, self).get_configuration(
      ProvStoreTestCase.CONFIGURATION_KEY,
      ProvStoreTestCase.CONFIGURATION_FILE_ENV,
      config_file)
    try:
      config[ProvStoreConverter.AUTHORIZATION] = \
        "ApiKey " + os.environ[ProvStoreTestCase.API_KEY_ENV]
      self.converter.configure(config)
      print("Using API key defined in " + ProvStoreTestCase.API_KEY_ENV)
    except KeyError:
      print("Using default API key defined in configuration file")
    super(ProvStoreTestCase, self).configure(config)

  def tearDown(self):
    super(ProvStoreTestCase, self).tearDown()
