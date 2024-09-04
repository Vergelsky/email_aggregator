import datetime
import imaplib
import email
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class EmailService:
    _entered = False

    def __init__(self, email_account, folder='INBOX'):
        self.folder = folder
        self.email_account = email_account

    def __enter__(self):
        self._entered = True
        logger.info(f' {self.__class__.__name__}: ' + 'Подключение к почтовой службе')
        try:
            self.mail = imaplib.IMAP4_SSL(self.email_account.provider)
            logger.info(f' {self.__class__.__name__}: ' + f'Подключено: {self.email_account.provider}')
        except Exception as e:
            logger.error(e)
        try:
            self.mail.login(self.email_account.email, self.email_account.password)
            logger.info(f' {self.__class__.__name__}: ' + f'Логин успешно: {self.email_account.email}')
        except Exception as e:
            logger.error(e)

        self.select_folder(self.folder)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._entered = False
        logger.info(f' {self.__class__.__name__}: ' + 'Отключение от почтовой службы')
        if exc_type is None:
            self.mail.logout()
            print("Exiting normally")
        else:
            self.mail.logout()
            print(f"Exiting with exception {exc_type}")
        return False

    def select_folder(self, folder):

        logger.info(f' {self.__class__.__name__}: ' + f'Подключение к {folder} в {self.email_account.email}...')
        try:
            response = self.mail.select(folder, readonly=True)
            logger.info(f' {self.__class__.__name__}: ' + f'Успешно подключено к {folder} в {self.email_account.email}!')
            return response
        except Exception as e:
            logger.info(f' {self.__class__.__name__}: ' + f'Подключение к {folder} в {self.email_account.email} не удалось.')
            logging.error(e)

    def get_emails_uids(self, count: int =0):
        """
        Выбирает идентификаторы последних count писем\n
        В формате [b'921', b'922', b'923', b'924', b'925']
        :param count: Количество идентификаторов. По умолчанию = 0 - выбираются все.
        :return: uids
        """
        if not self._entered:
            raise RuntimeError("Метод должен быть вызван с контекстным менеджером")
        if count < 0:
            raise ValueError('Количество идентификаторов должно быть неотрицательным числом')
        logger.info(f' {self.__class__.__name__}: ' + f'Получение идентификаторов последних {str(count) if count > 0 else "всех"} писем')
        try:
            is_ok, uids = self.mail.uid('search', 'ALL')
            uids = uids[0].split()
            if count == 0:
                return uids
            else:
                uids = uids[-count:]
            logger.info(f' {self.__class__.__name__}: ' + 'Идентификаторы получены')
            return uids
        except Exception as e:
            logging.error(e)

    def get_letter_by_uid(self, uid):
        """
        :param uid: Идентификатор письма
        :return: email_message
        """
        if not self._entered:
            raise RuntimeError("Метод должен быть вызван с контекстным менеджером")
        logger.info(f' {self.__class__.__name__}: ' + 'Получение письма по идентификатору ' + str(uid))
        try:
            is_ok, data = self.mail.uid('fetch', uid, '(RFC822)')
            logger.info(f' {self.__class__.__name__}: ' + 'Письмо получено')
            return data
        except Exception as e:
            logger.error(e)


class ParseLetterService:
    """
    Парсер письма. Инициализируется объектом письма - вторым аргументом из метода get_letter_by_uid.
    Имеет методы для получения следующих атрибутов:
    - uid
    - Тема сообщения
    - Дата отправки
    - Описание или текст сообщения
    - Список прикреплённых файлов к письму
    - А также метод возвращающий всё перечисленное одним кортежем
    """

    def __init__(self, msg):
        logger.info(f' {self.__class__.__name__}: ' + 'Извлечение объекта письма')
        self.msg = email.message_from_bytes(msg[1])

    def get_uid(self):
        logger.info(f' {self.__class__.__name__}: ' + 'Получение идентификатора письма')
        return self.msg['Message-ID']

    def get_subject(self):
        logger.info(f' {self.__class__.__name__}: ' + 'Получение темы письма')
        subject = email.header.decode_header(self.msg['Subject'])[0]
        subject_encoding = subject[1]
        subject = subject.decode(subject_encoding)
        return subject

    def get_date(self):
        logger.info(f' {self.__class__.__name__}: ' + 'Получение даты отправки письма')
        date = email.utils.parsedate_tz(self.msg['Date'])
        return datetime.datetime(*date[:6]).strftime('%d.%m.%Y %H:%M:%S')

    def get_text(self):
        text_content = None
        for part in self.msg.walk():
            if part.get_content_maintype() == 'text':
                if part.get_content_subtype() == 'html':
                    html_content = part.get_payload(decode=True)
                    soup = BeautifulSoup(html_content, "html.parser")
                    text_content = soup.get_text()
                elif part.get_content_subtype() == 'plain':
                    text_content = part.get_payload(decode=True)
        return text_content

    def get_attachments(self):
        logger.info(f' {self.__class__.__name__}: ' + 'Получение списка прикрепленных файлов к письму')
        attachments = {}
        for part in self.msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if filename:
                    attachments[filename] = part.get_payload(decode=True)
        return attachments

    def get_all_attributes(self):
        return self.get_uid(), self.get_subject(), self.get_date(), self.get_text(), self.get_attachments()
