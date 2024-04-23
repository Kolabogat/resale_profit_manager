import time
import pytest
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

from accounting.management.commands.command_filter_query import FILTER_TICKETS


@pytest.mark.usefixtures('driver_init', 'add_ticket_filter', 'user')
class TestURLChrome(LiveServerTestCase):
    def test_open_admin_url(self):
        self.driver.get(('%s%s' % (self.live_server_url, '/admin/')))
        assert 'Log in | Django site admin' in self.driver.title

    def test_log_in(self):
        self.driver.get(('%s%s' % (self.live_server_url, '/user/login/')))

        self.driver.find_element(By.NAME, 'username').send_keys('user')
        self.driver.find_element(By.NAME, 'password').send_keys('a9Jd2o9gLe2axs')
        self.driver.find_element(By.NAME, 'login').click()

        assert 'Tickets' == self.driver.title
        assert 'user' in self.driver.page_source
        for ticket in FILTER_TICKETS:
            assert ticket.get('color') in self.driver.page_source
        time.sleep(0.3)
