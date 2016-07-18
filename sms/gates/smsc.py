import re
import urllib.parse
import requests
from requests.exceptions import RequestException, HTTPError
from sms.base import SMSGate


class SMSCGate(SMSGate):
    name = 'smsc'
    display_name = 'SMSC'
    gate_url_template = 'http://smsc.ru/sys/send.php'

    error_descr = {
        1: 'Ошибка в параметрах.',
        2: 'Неверный логин или пароль.',
        3: 'Недостаточно средств на счете Клиента.',
        4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
        5: 'Неверный формат даты.',
        6: 'Сообщение запрещено (по тексту или по имени отправителя).',
        7: 'Неверный формат номера телефона.',
        8: 'Сообщение на указанный номер не может быть доставлено.',
        9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты.',
    }

    def _send(self, **kwargs):

        params = {
            'login': kwargs['login'],
            'psw': kwargs['password'],
            'phones': kwargs['tel'],
            'mes': kwargs['text'],
            'fmt': 3,
        }
        try:
            resp = requests.get(
                url=self.gate_url_template + '?' + urllib.parse.urlencode(params)
            )  # raises exception in case of some conection/pool failure
            if re.search('^[45]', str(resp.status_code)):
                raise HTTPError(resp.status_code)  # raises exception in case of 4xx or 5xx HTTP response
            json = resp.json()
            if 'error' in json:
                e = HTTPError(  # raises exception if 200 OK but there is a problem in business logic
                    '%s:\n%s' % (
                        self.error_descr.get(json['error_code']),
                        json.get('error')
                    )
                )
                e.sms_id = json.get('id')  # supply the message id if any
                raise e
            else:
                return json['id']
        except HTTPError as e:
            raise
