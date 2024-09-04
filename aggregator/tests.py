import os

from django.test import TestCase

from aggregator.models import EmailAccount
from aggregator.servieces import EmailService
from config.settings import AVAILABLE_EMAIL_PROVIDERS, INITIAL_MESSAGE_LOAD_LIMIT
import logging

logging = logging.getLogger(__name__)


class TestEmailService(TestCase):

    def setUp(self):
        for provider in AVAILABLE_EMAIL_PROVIDERS:
            EmailAccount.objects.create(email=f'graf.werger@{provider['url'][5:]}', provider=provider['url'],
                                    password=os.getenv(f'{provider['name'].upper()}_EMAIL_PASSWORD'))

        self.email_services = []
        for account in EmailAccount.objects.all():
            self.email_services.append(EmailService(account))

    def test_connect(self):
        for e_service in self.email_services:
            logging.info("запущен тест подключения к " + e_service.email_account.email)
            with e_service as es:
                self.assertEqual(es.mail.noop()[0], 'OK')

    def test_select_inbox(self):
        for e_service in self.email_services:
            logging.info("запущен тест выбора папки в аккаунте " + e_service.email_account.email)
            with e_service as es:
                res = es.select_inbox()
                logging.info(res[1])
                self.assertEqual(res[0], 'OK')

    def test_get_last_emails(self):
        for e_service in self.email_services:
            logging.info("запущен тест получения последних писем в аккаунте " + e_service.email_account.email)
            with e_service as es:
                es.select_inbox()
                res = es.get_last_emails(INITIAL_MESSAGE_LOAD_LIMIT)
                logging.info(res)
                self.assertEqual(res[0], 'OK')