# Copyright 2018 Google Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""App Engine local test runner example.

This program handles properly importing the App Engine SDK so that test modules
can use google.appengine.* APIs and the Google App Engine testbed.

Example invocation:

  $ python runtests.py ~/google-cloud-sdk

"""

import argparse
import os
import sys
import unittest

from absl import flags
from absl.testing import absltest

FLAGS = flags.FLAGS


def main(test_path, test_pattern, unparsed_args):
  # Set test env vars.
  os.environ['GAE_APPLICATION_ID'] = 'crmint-dev'

  # Parses FLAGS from the unparsed arguments, needed to mimick
  # `absltest.main()` behavior.
  FLAGS([sys.argv[0]] + unparsed_args)

  # Discover and run tests.
  suite = absltest.TestLoader().discover(test_path, test_pattern)
  return unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument(
      '--test-path',
      help='The path to look for tests, defaults to the current directory.',
      default=os.path.join(os.getcwd(), 'tests/unit/workers'))
  parser.add_argument(
      '--test-pattern',
      help='The file pattern for test modules, defaults to *_tests.py.',
      default='*_tests.py')

  args, unparsed = parser.parse_known_args()
  result = main(args.test_path, args.test_pattern, unparsed)
  sys.exit(0 if result.wasSuccessful() else 1)
