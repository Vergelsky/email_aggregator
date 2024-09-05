import os
import unittest

from django.test import TestCase

from aggregator.models import EmailAccount
from aggregator.servieces import EmailService, ParseLetterService
from config.settings import AVAILABLE_EMAIL_PROVIDERS, INITIAL_MESSAGE_LOAD_LIMIT
import logging

logger = logging.getLogger(__name__)


@unittest.skip
class TestEmailService(TestCase):

    def setUp(self):
        for provider in AVAILABLE_EMAIL_PROVIDERS:
            EmailAccount.objects.create(email=f'graf.werger@{provider['url']}', provider=provider['url_imap'],
                                        password=os.getenv(f'{provider['name'].upper()}_EMAIL_PASSWORD'))

        self.email_services = []
        for account in EmailAccount.objects.all():
            self.email_services.append(EmailService(account))

    def test_connect(self):
        for e_service in self.email_services:
            logger.info(f' {self.__class__.__name__}: ' + "запущен тест подключения к " + e_service.email_account.email)
            with e_service as es:
                self.assertEqual(es.mail.noop()[0], 'OK')

    def test_select_folder(self):
        for e_service in self.email_services:
            logger.info(
                f' {self.__class__.__name__}: ' + "запущен тест выбора папки в аккаунте " + e_service.email_account.email)
            with e_service as es:
                res = es.select_folder("INBOX")
                logger.info(f' {self.__class__.__name__}: ' + res[1])
                self.assertEqual(res[0], 'OK')

    def test_get_emails_uids(self):
        for e_service in self.email_services:
            logger.info(
                f' {self.__class__.__name__}: ' + "запущен тест получения uid писем в аккаунте " + e_service.email_account.email)
            with e_service as es:
                res = es.get_emails_uids(INITIAL_MESSAGE_LOAD_LIMIT)
                logger.info(f' {self.__class__.__name__}: {res}')
                self.assertEqual(type(res), list)

    def test_get_letter_by_uid(self):
        for e_service in self.email_services:
            logger.info(
                f' {self.__class__.__name__}: ' + "запущен тест получения письма в аккаунте " + e_service.email_account.email)
            with e_service as es:
                uids = es.get_emails_uids(INITIAL_MESSAGE_LOAD_LIMIT)
                logger.info(f' {self.__class__.__name__}: {uids[1]}')
                res = es.get_letter_by_uid(uids[1][0])
                logger.info(f' {self.__class__.__name__}: ' + res)
                self.assertEqual(type(res), tuple)


class TestParseLetterService(TestCase):
    def setUp(self):
        self.email_services = []
        self.letters = []
        for provider in AVAILABLE_EMAIL_PROVIDERS:
            EmailAccount.objects.create(email=f'graf.werger@{provider['url']}', provider=provider['url_imap'],
                                        password=os.getenv(f'{provider['name'].upper()}_EMAIL_PASSWORD'))

        for account in EmailAccount.objects.all():
            email_service = EmailService(account)
            with email_service as es:
                uid = es.get_emails_uids(5)[-1]
                logger.info(f' {self.__class__.__name__}: ' + f'Получен uid письма: {uid}')
                msg = es.get_letter_by_uid(uid)
                self.letters.append(ParseLetterService(msg))
                logger.info(f' {self.__class__.__name__}: ' + f'Получено письмо по идентификатору: {uid}.')

    def test_get_uid(self):
        logger.info('2>>>>>>>>>>>>>>>>>>>>>>>>>')
        for letter in self.letters:
            uid = letter.get_uid()
            logger.info(f' {self.__class__.__name__}: ' + f'Получен идентификатор письма: {uid}.')
            self.assertEqual(type(uid), str)

    def test_get_subject(self):
        logger.info('3>>>>>>>>>>>>>>>>>>>>>>>>>')
        for letter in self.letters:
            subject = letter.get_subject()
            logger.info(f' {self.__class__.__name__}: ' + f'Получена тема письма: {subject}.')
            self.assertEqual(type(subject), str)

    def test_get_date(self):
        logger.info('4>>>>>>>>>>>>>>>>>>>>>>>>>')
        for letter in self.letters:
            date = letter.get_date()
            logger.info(f' {self.__class__.__name__}: ' + f'Получена дата письма: {date}.')
            self.assertEqual(type(date), str)

    def test_get_text(self):
        logger.info('5>>>>>>>>>>>>>>>>>>>>>>>>>')
        for letter in self.letters:
            text = letter.get_text()
            logger.info(f' {self.__class__.__name__}: ' + f'Получен текст письма: {text}.')
            self.assertEqual(type(text), str)
