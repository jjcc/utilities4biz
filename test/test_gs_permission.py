# create a test file for gs_permission module
import unittest
from unittest.mock import patch

from gs_permission import get_gs_files, SERVICE_ACCOUNT_FILE, SCOPES
"""
Unit tests for gs_permission module
"""

class TestGSPermission(unittest.TestCase):
    def setUp(self):
        self.service_account_file = SERVICE_ACCOUNT_FILE
        self.scopes = SCOPES



    def test_get_gs_files_no_files(self):
        files = get_gs_files(SERVICE_ACCOUNT_FILE, SCOPES)
        
        print("Accessible files:")
        for file in files:
            print(f"Name: {file['name']}, ID: {file['id']}")
