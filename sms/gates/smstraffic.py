from sms.base import SMSGate


class SMSTrafficGate(SMSGate):
    name = 'sms_traffic'
    display_name = 'SMS Traffic'
    gate_url_template = 'http://smstraffic.ru/super­api/message/'
