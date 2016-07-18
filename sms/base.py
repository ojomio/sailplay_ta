import pkgutil
import re
import urllib.parse
import requests
from requests.exceptions import RequestException, HTTPError
from sms.models import MessageLog


class SMSGateMeta(type):
    registry = {}

    def __new__(mcs, object_or_name, bases, dict_):
        abstract = dict_.pop('abstract', False)  # abstract is not inherited
        if not abstract:
            if 'name' not in dict_:
                raise ValueError('You must supply gate name in name class field')
        new_class = super().__new__(mcs, object_or_name, bases, dict_)
        if not abstract:
            mcs.registry[dict_['name']] = new_class
        return new_class

    def get_by_name(cls, gate_name):
        return cls.registry[gate_name]

    def get_options(cls):
        return list(cls.registry.values())

    def __getattr__(cls, item):
        if item == 'display_name':
            return cls.name


class SMSGate(metaclass=SMSGateMeta):
    name = None
    abstract = True
    gate_url_template = None
    # Django tries to call x if x is callable, and class is callable of course, so we suppress this behaviour explicitly
    do_not_call_in_templates = True

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def send(self, **kwargs):
        '''
        Parent method which wraps the real .send() and decide how to handle the outcome
        :param kwargs:
        :return: message id if available
        '''

        try:
            sms_id = self._send(**kwargs)
        except RequestException as e:
            MessageLog.objects.create(
                sms_id=getattr(e, 'sms_id', None),
                via_gate=self.name,
                sender=kwargs['login'],
                recepient=kwargs['tel'],
                sent_ok=False,
                error_description=str(e)
            )
            raise
        else:
            MessageLog.objects.create(
                sms_id=sms_id,
                via_gate=self.name,
                sender=kwargs['login'],
                recepient=kwargs['tel'],
                sent_ok=True,
            )

    def _send(self, **kwargs):
        '''
        Naïve implementation which only fills the URL template in the subclass
        :return: message id if available
        '''
        try:
            resp = requests.get(
                url=self.gate_url_template + '?' + urllib.parse.urlencode(kwargs),
            )  # raises exception in case of some conection/pool failure
            if re.search('^[45]', str(resp.status_code)):
                raise HTTPError(resp.status_code)  # raises exception in case of 4xx or 5xx HTTP response
                # no further error detection and no SMS id extraction
        except HTTPError as e:
            raise


for importer, module_name, is_pkg in pkgutil.iter_modules(['/'.join([__package__, 'gates'])]):
    if not is_pkg:
        pkgutil.importlib.import_module('.gates.' + module_name, __package__)
