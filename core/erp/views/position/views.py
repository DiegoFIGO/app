from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import PositionForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Position


class PositionListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Position
    template_name = 'position/list.html'
    permission_required = 'view_position'

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Position.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cargos'
        context['create_url'] = reverse_lazy('erp:position_create')
        context['list_url'] = reverse_lazy('erp:position_list')
        context['entity'] = 'Cargos'
        return context


class PositionCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'position/create.html'
    success_url = reverse_lazy('erp:position_list')
    permission_required = 'add_position'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creaci??n de un Cargo'
        context['entity'] = 'Cargos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PositionUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'position/create.html'
    success_url = reverse_lazy('erp:position_list')
    permission_required = 'change_position'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opci??n'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edici??n una Cargo'
        context['entity'] = 'Cargos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PositionDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Position
    template_name = 'position/delete.html'
    success_url = reverse_lazy('erp:position_list')
    permission_required = 'delete_position'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminaci??n de un Cargo'
        context['entity'] = 'Cargos'
        context['list_url'] = self.success_url
        return context
