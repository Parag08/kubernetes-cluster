from cluster_management.src import resource_manager
from cluster_management.core import db
from cluster_management import app

import unittest
import datetime
import time

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestResourceManager(unittest.TestCase):
    db.create_all()



if __name__ == '__main__':
    unittest.main()
