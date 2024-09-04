import imaplib
import email
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, email_account, folder='INBOX'):
        self.folder = folder
        self.email_account = email_account

    def __enter__(self):
        self._entered = True
        logger.info('Подключение к почтовой службе')
        try:
            self.mail = imaplib.IMAP4_SSL(self.email_account.provider)
            logger.info(f'Подключено: {self.email_account.provider}')
        except Exception as e:
            logger.error(e)
        try:
            self.mail.login(self.email_account.email, self.email_account.password)
            logger.info(f'Логин успешно: {self.email_account.email}')
        except Exception as e:
            logger.error(e)

        self.select_folder(self.folder)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._entered = False
        logger.info('Отключение от почтовой службы')
        if exc_type is None:
            self.mail.logout()
            print("Exiting normally")
        else:
            self.mail.logout()
            print(f"Exiting with exception {exc_type}")
        return False

    def select_folder(self, folder):

        logging.info(f'Подключение к {folder} в {self.email_account.email}...')
        try:
            response = self.mail.select(folder, readonly=True)
            logging.info(f'Успешно подключено к {folder} в {self.email_account.email}!')
            return response
        except Exception as e:
            logging.info(f'Подключение к {folder} в {self.email_account.email} не удалось.')
            logging.error(e)

    def get_emails_uids(self, count=0):
        """
        Выбирает идентификаторы последних count писем
        :param count: Количество идентификаторов. По умолчанию = 0 - выбираются все.
        :return: (is_ok, uids)
        """
        if not self._entered:
            raise RuntimeError("Метод должен быть вызван с контекстным менеджером")
        if count < 0 or not type(count) is int:
            raise ValueError('Количество идентификаторов должно быть неотрицательным числом')
        logging.info(f'Получение идентификаторов последних {str(count) if count > 0 else "всех"} писем')
        try:
            is_ok, uids = self.mail.uid('search', 'ALL')
            uids = uids[0].split()
            if count == 0:
                return is_ok, uids
            else:
                uids = uids[-count:]
            logging.info('Идентификаторы получены')
            return is_ok, uids
        except Exception as e:
            logging.error(e)

    def get_letter_by_uid(self, uid):
        """
        :param uid: Идентификатор письма
        :return: (is_ok, email_message)
        """
        if not self._entered:
            raise RuntimeError("Метод должен быть вызван с контекстным менеджером")
        logging.info('Получение письма по идентификатору ' + str(uid))
        try:
            is_ok, data = self.mail.uid('fetch', uid, '(RFC822)')
            logger.info('Письмо получено')
            return is_ok, data
        except Exception as e:
            logger.error(e)

class ParseLetterService(EmailService):
    pass
