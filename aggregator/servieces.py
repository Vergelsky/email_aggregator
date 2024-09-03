import imaplib
import email
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, email_account):
        logger.info('Инициализация')
        self.email_account = email_account

    def __enter__(self):
        logger.info('Подключение к почтовой службе')
        try:
            self.mail = imaplib.IMAP4_SSL(self.email_account.provider)
        except Exception as e:
            logger.error(e)
            logger.info(f'Подключено: {self.email_account.provider}')
        try:
            self.mail.login(self.email_account.email, self.email_account.password)
            logger.info(f'Логин: {self.email_account.email}')
        except Exception as e:
            logger.error(e)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.info('Отключение от почтовой службы')
        if exc_type is None:
            print("Exiting normally")
        else:
            print(f"Exiting with exception {exc_type}")
        return False


