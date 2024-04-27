import time
import pytest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

from accounting.management.commands.command_filter_query import FILTER_TICKETS
from accounting.models import Ticket
from tests.conftest import TEST_USERNAME, TEST_PASSWORD, TEST_EMAIL


@pytest.mark.usefixtures('driver_init', 'add_ticket_filter', 'user')
class TestLiveServer(LiveServerTestCase):
    def test_open_admin_url(self):
        self.driver.get(('%s%s' % (self.live_server_url, '/admin/')))
        assert 'Log in | Django site admin' in self.driver.title

    def log_in(self):
        self.driver.get(('%s%s' % (self.live_server_url, '/user/login/')))

        self.driver.find_element(By.NAME, 'username').send_keys(TEST_USERNAME)
        self.driver.find_element(By.NAME, 'password').send_keys(TEST_PASSWORD)
        self.driver.find_element(By.NAME, 'login').click()

        assert 'Tickets' == self.driver.title
        assert 'user' in self.driver.page_source
        for ticket in FILTER_TICKETS:
            assert ticket.get('color') in self.driver.page_source
        time.sleep(0.2)

    def add_ticket(self):
        self.log_in()
        self.driver.get(('%s%s' % (self.live_server_url, '/add/')))
        self.driver.get(f'{self.live_server_url}/add/')
        self.driver.find_element(By.NAME, 'title').send_keys('test ticket')
        self.driver.find_element(By.NAME, 'bought').send_keys(5.67)
        self.driver.find_element(By.NAME, 'add_ticket').click()
        time.sleep(1)

    def check_added_ticket(self):
        self.add_ticket()
        self.driver.get(f'{self.live_server_url}')
        assert 'test ticket' in self.driver.page_source

    def test_update_added_ticket(self):
        self.check_added_ticket()
        ticket_pk = Ticket.objects.filter(title='test ticket').first().pk
        self.driver.get(f'{self.live_server_url}/update/{ticket_pk}')
        self.driver.find_element(By.NAME, 'sold').send_keys(6.64)
        self.driver.find_element(By.NAME, 'add_ticket').click()
        time.sleep(1)


