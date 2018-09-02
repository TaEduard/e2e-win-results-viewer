import xml.etree.ElementTree as ET
import utils
import os


def merge_test_cases(test_cases, dest, show_skipped=False):
    if len(test_cases) == 0:
        return

    xmlElem = ET.Element("testsuite")
    for test_case_path in test_cases:
        testTree = ET.parse(test_case_path)
        root = testTree.getroot()
        for testcase in root.findall("testcase"):
            if not show_skipped and len(testcase.findall("skipped")) > 0:
                continue
            xmlElem.append(testcase)
    xmlTree = ET.ElementTree(xmlElem)
    xmlTree.write(dest)