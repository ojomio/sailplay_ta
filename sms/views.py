from django.views.generic.base import TemplateView
from requests.exceptions import RequestException

from .base import SMSGate


class MainView(TemplateView):
    template_name = 'sender.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gate_class_list'] = SMSGate.get_options()
        if 'sent_ok' in context:
            if context['sent_ok']:
                context['msg'] = 'Сообщение отправлено успешно'
            else:
                context['msg'] = str(kwargs['exception'])

        return context

    def post(self, request, *args, **kwargs):
        gate_name = request.POST['gate_name']
        gate_cls = SMSGate.registry[gate_name]
        gate_obj = gate_cls(request.POST['login'], request.POST['password'])

        context = {}
        try:
            gate_obj.send(**{k: request.POST[k] for k in request.POST})  # get rid of QueryDict one-element arrays
        except RequestException as e:
            context['exception'] = e
            context['sent_ok'] = False
        else:
            context['sent_ok'] = True
        context = self.get_context_data(**context)
        return self.render_to_response(context)


