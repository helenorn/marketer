#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import unittest
from typing import List


def build_test_suite(test_cases: List[str]) -> unittest.TestSuite:
    import tests
    suite = unittest.TestSuite()

    for test_case in test_cases:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(getattr(tests, test_case)))
    return suite

def extraxt_property_data_suite() -> unittest.TestSuite:
    return build_test_suite(['NounCategories','TestAProperty', 'TestAllProperties', 'TestExtractPropertyData', 'PropertyData'])


def property_similarity_matrix_suite() -> unittest.TestSuite:
    return build_test_suite(["TestPropertySimilarityMatrix"])


def main():
    tests = {"extract": extraxt_property_data_suite,
             "matrix": property_similarity_matrix_suite,}

    targets = sys.argv[1:] or tests.keys()
    suite = unittest.TestSuite()

    for target in targets:
        suite.addTests(tests[target.lower()]())
    if suite.countTestCases() > 0:
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)

if __name__=='__main__':
    main()
