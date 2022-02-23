import json
import os

from django.conf import settings
from django.views.generic import TemplateView


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

from core.erp.forms import ClientForm, ProductiveForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Productive
from xhtml2pdf import pisa

# List Services U

class ProductiveListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Productive
    template_name = 'productive/list.html'
    permission_required = 'view_productive'

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Productive.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proyectos - Sector Productivo'
        context['create_url'] = reverse_lazy('erp:productive_create')
        context['list_url'] = reverse_lazy('erp:productive_list')
        context['entity'] = 'Proyectos - Sector Productivo'
        return context

# Create Services U

class ProductiveCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Productive
    form_class = ProductiveForm
    template_name = 'productive/create.html'
    success_url = reverse_lazy('erp:productive_list')
    permission_required = 'add_productive'
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
        context['title'] = 'Creación de un Proyecto - Sector Productivo'
        context['entity'] = 'Proyectos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['frmClient'] = ProductiveForm()
        return context

# Update Services U

class ProductiveUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Productive
    form_class = ProductiveForm
    template_name = 'productive/create.html'
    success_url = reverse_lazy('erp:productive_list')
    permission_required = 'change_productive'
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
        context['title'] = 'Edición de un Proyecto - Sector Productivo'
        context['entity'] = 'Proyectos - Sector Productivo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

# Delete  Services U

class ProductiveDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Productive
    template_name = 'productive/delete.html'
    success_url = reverse_lazy('erp:productive_list') 
    permission_required = 'delete_productive'
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
        context['title'] = 'Eliminación de un Proyecto - Sector Productivo'
        context['entity'] = 'Proyectos - Sector Productivo'
        context['list_url'] = self.success_url
        return context

# PDF Services U

class ProductiveInvoicePdfView(LoginRequiredMixin, View):
    
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
            template = get_template('productive/invoice.html')
            context = {
                'productive': Productive.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('erp:productive_list'))

# PDF Services U Report
class ProductivedetInvoicePdfView(LoginRequiredMixin, View):
    
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
            template = get_template('productive/invoicedet.html')
            context = {
                'productive': Productive.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Empresa Pública UPEC-CREATIVA EP', 'ruc': 'SECTOR PRODUCTIVO', 'address': 'Tulcán - Ecuador'},
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
        return HttpResponseRedirect(reverse_lazy('erp:productive_list'))

# PDF Services U Report Projects Productivs
# class ProductiveReportView(TemplateView):
    
#     model = Productive
#     template_name = 'productive/report.html'


#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'search_report':
#                 data = []
#                 start_date = request.POST.get('start_date', '')
#                 end_date = request.POST.get('end_date', '')
#                 search = Productive.objects.all()
#                 if len(start_date) and len(end_date):
#                     search = search.filter(date_joined__range=[start_date, end_date])
#                 for s in search:
#                     data.append([
#                         s.id,
#                         s.name,
#                         s.representative.full_name,
#                         s.type_project,
#                         s.organization,
#                         s.quantity,
#                         s.desing,
#                         # s.id,
#                         # s.cli.names,
#                         # s.cli.surnames,
#                         # s.date_joined.strftime('%Y-%m-%d'),
#                         # format(s.subtotal, '.2f'),
#                         # format(s.iva, '.2f'),
#                         # format(s.total, '.2f'),
#                     ])

#                 # subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
#                 # subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
#                 # iva = search.aggregate(r=Coalesce(Sum('iva'), 0, output_field=DecimalField())).get('r')
#                 # total = search.aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')

#                 # data.append([
#                 #     '---',
#                 #     '---',
#                 #     '---',
#                 #     '---',
#                 #     format(subtotal, '.2f'),
#                 #     format(iva, '.2f'),
#                 #     format(total, '.2f'),
#                 # ])
#             else:
#                 data['error'] = 'Ha ocurrido un error'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Reporte de Ventas'
#         context['entity'] = 'Reportes'
#         context['list_url'] = reverse_lazy('productive_report')
#         context['form'] = ProductiveReportForm()
#         return context

