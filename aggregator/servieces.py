import imaplib
import email
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, email_account):
        self.email_account = email_account

    def __enter__(self):
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

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.info('Отключение от почтовой службы')
        if exc_type is None:
            print("Exiting normally")
        else:
            print(f"Exiting with exception {exc_type}")
        return False

    def select_inbox(self):

        logging.info('Подключение к INBOX в '+ self.email_account.email +'...')
        try:
            resp = self.mail.select("INBOX")
            logging.info('Успешно подключено к INBOX в '+ self.email_account.email)
        except e as e:
            logging.info('Подключение к INBOX в ' + self.email_account.email + ' не удалось')
            logging.error(e)

        return self.mail.select("INBOX")


