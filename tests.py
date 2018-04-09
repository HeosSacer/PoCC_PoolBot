from unittest import TestCase
from unittest.mock import MagicMock
#from src import pocc_pool_bot
from src.utils import status

class TestStatus(TestCase):

    def test_setup_logger(self):
        self.assertRaises(Exception, status.setup_logger())

    def test_bot(self):
        pass

    def test_pools(self):
        pass

    def test_subscribers(self):
        pass