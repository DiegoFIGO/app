import json
import os

from django.conf import settings


from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from core.erp.forms import ClientForm, PublicsForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Publics
from xhtml2pdf import pisa

# List Publics

class PublicsListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Publics
    template_name = 'publics/list.html'
    permission_required = 'view_publics'

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Publics.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proyectos - Compras Públicas'
        context['create_url'] = reverse_lazy('erp:publics_create')
        context['list_url'] = reverse_lazy('erp:publics_list')
        context['entity'] = 'Proyectos - Compras Públicas'
        return context

# Create Publics

class PublicsCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Publics
    form_class = PublicsForm
    template_name = 'publics/create.html'
    success_url = reverse_lazy('erp:publics_list')
    permission_required = 'add_publics'
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
            # elif action == 'create_client':
                
            #     with transaction.atomic():
            #         frmClient = ClientForm(request.POST)
            #         data = frmClient.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Proyecto - Compras Públicas'
        context['entity'] = 'Proyectos - Compras Públicas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['frmClient'] = PublicsForm()
        return context

# Update Publics

class PublicsUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Publics
    form_class = PublicsForm
    template_name = 'publics/create.html'
    success_url = reverse_lazy('erp:publics_list')
    permission_required = 'change_publics'
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
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Proyecto - Compras Públicas'
        context['entity'] = 'Proyectos - Compras Públicas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

# Delete Publics

class PublicsDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Publics
    template_name = 'publics/delete.html'
    success_url = reverse_lazy('erp:publics_list') 
    permission_required = 'delete_publics'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de un Proyecto - Compras Públicas'
        context['entity'] = 'Proyectos - Compras Públicas'
        context['list_url'] = self.success_url
        return context

# PDF Publics

class PublicsInvoicePdfView(LoginRequiredMixin, View):
    
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('publics/invoice.html')
            context = {
                'publics': Publics.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Empresa Pública UPEC-CREATIVA EP', 'ruc': '9999999999999', 'address': 'Tulcán - Ecuador'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logoepd.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:publics_list'))


