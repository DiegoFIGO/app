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

from core.erp.forms import AcquisitionbForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Acquisitionbs
from xhtml2pdf import pisa

# List Services U

class AcquisitionbListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Acquisitionbs
    template_name = 'acquisitionb/list.html'
    permission_required = 'view_acquisitionb'

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Acquisitionbs.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de  Proyectos - Adquisición de Bienes'
        context['create_url'] = reverse_lazy('erp:acquisitionb_create')
        context['list_url'] = reverse_lazy('erp:acquisitionb_list')
        context['entity'] = 'Adquisición de Bienes'
        return context

# Create Services U

class AcquisitionbCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Acquisitionbs
    form_class = AcquisitionbForm
    template_name = 'acquisitionb/create.html'
    success_url = reverse_lazy('erp:acquisitionb_list')
    permission_required = 'add_acquisitionb'
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
        context['title'] = 'Creación de un Proyecto - Adquisición de Bienes'
        context['entity'] = 'Adquisición de Bienes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

# Update Services U

class AcquisitionbUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Acquisitionbs
    form_class = AcquisitionbForm
    template_name = 'acquisitionb/create.html'
    success_url = reverse_lazy('erp:acquisitionb_list')
    permission_required = 'change_acquisitionb'
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
        context['title'] = 'Edición de un Proyecto - Adquisición de Bienes'
        context['entity'] = 'Adquisición de Bienes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

# Delete  Services U

class AcquisitionbDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Acquisitionbs
    template_name = 'acquisitionb/delete.html'
    success_url = reverse_lazy('erp:acquisitionb_list') 
    permission_required = 'delete_acquisitionb'
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
        context['title'] = 'Eliminación de un Proyecto - Adquisición de Bienes'
        context['entity'] = 'Adquisición de Bienes'
        context['list_url'] = self.success_url
        return context

# PDF Services U

class AcquisitionbInvoicePdfView(LoginRequiredMixin, View):
    
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
            template = get_template('acquisitionb/invoice.html')
            context = {
                'acquisitionb': Acquisitionbs.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('erp:acquisitionb_list'))
