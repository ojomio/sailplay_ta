import re

from django.core.validators import RegexValidator
from django.forms import Form, ChoiceField, Textarea
from django.forms.fields import CharField
from django.views.generic import FormView
from requests.exceptions import RequestException

from .base import SMSGate

tel_re = re.compile(r'^\+\d{11}$')
validate_tel = RegexValidator(tel_re, 'Enter a valid phone number (+xxxxxxxxxxx).', 'invalid')


class SendForm(Form):
    gate_name = ChoiceField(
        choices=[(class_.name, class_.display_name) for class_ in SMSGate.get_options()],
        label='Select gate:'
    )
    login = CharField()
    password = CharField()
    tel = CharField(validators=[validate_tel],
                    label='Enter tel. no')
    text = CharField(widget=Textarea,
                     label='Enter text')


class MainView(FormView):
    template_name = 'sender.html'
    form_class = SendForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'sent_ok' in context:
            if context['sent_ok']:
                context['msg'] = 'Сообщение отправлено успешно'
            else:
                context['msg'] = str(kwargs['error'])
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        '''Called if form is valid'''
        gate_name = form.cleaned_data['gate_name']
        gate_cls = SMSGate.registry[gate_name]
        gate_obj = gate_cls(form.cleaned_data['login'], form.cleaned_data['password'])

        context = {}
        try:
            gate_obj.send(**form.cleaned_data)
        except RequestException as e:
            context['error'] = str(e)
            context['sent_ok'] = False
        else:
            context['sent_ok'] = True
        context = self.get_context_data(**context)
        return self.render_to_response(context)

    def form_invalid(self, form):
        '''Called if validation fails'''
        context = {
            'sent_ok': False,
            'error': form.errors
        }
        context = self.get_context_data(**context)
        return self.render_to_response(context)
