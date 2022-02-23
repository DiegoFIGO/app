from core.erp.views.category.views import CategoryCreateView, CategoryDeleteView, CategoryListView, CategoryUpdateView
from django.urls import path
from core.erp.views.client.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.represent.views import *
from core.erp.views.product.views import *
from core.erp.views.project.views import *
from core.erp.views.servicesp.views import *
from core.erp.views.sale.views import *
from core.erp.views.position.views import *
from core.erp.views.employer.views import *
from core.erp.views.tests.views import TestView
from core.erp.views.construcction.views import *
from core.erp.views.acquisitionb.views import *
from core.erp.views.acquisitionservices.views import *
from core.erp.views.informsuni.views import *
from core.erp.views.budget.views import *
from core.erp.views.treasury.views import *
from core.erp.views.certification.views import *
from core.erp.views.perfil.views import *
from core.erp.views.perfilprod.views import *
from core.erp.views.productive.views import *
from core.erp.views.publics.views import *

app_name = 'erp'

urlpatterns = [
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # represent
    path('represent/list/', RepresentListView.as_view(), name='represent_list'),
    path('represent/add/', RepresentCreateView.as_view(), name='represent_create'),
    path('represent/update/<int:pk>/', RepresentUpdateView.as_view(), name='represent_update'),
    path('represent/delete/<int:pk>/', RepresentDeleteView.as_view(), name='represent_delete'),
    path('represent/invoice/pdf/<int:pk>/', RepresentInvoicePdfView.as_view(), name='represent_invoice_pdf'),
    # project
    path('project/list/', ProjectListView.as_view(), name='project_list'),
    path('project/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/invoice/pdf/<int:pk>/', ProjectInvoicePdfView.as_view(), name='project_invoice_pdf'),
    path('project/invoicedet/pdf/<int:pk>/', ProjectdetInvoicePdfView.as_view(), name='project_invoicedet_pdf'),
    # project services profesionals
    path('servicesp/list/', ServicesProfListView.as_view(), name='servicesp_list'),
    path('servicesp/add/', ServicesProfCreateView.as_view(), name='servicesp_create'),
    path('servicesp/update/<int:pk>/', ServicesProfUpdateView.as_view(), name='servicesp_update'),
    path('servicesp/delete/<int:pk>/', ServicesProfDeleteView.as_view(), name='servicesp_delete'),
    path('servicesp/invoice/pdf/<int:pk>/', ServicesProfInvoicePdfView.as_view(), name='servicesp_invoice_pdf'),
    # project acquisition belongings
    path('acquisitionb/list/', AcquisitionbListView.as_view(), name='acquisitionb_list'),
    path('acquisitionb/add/', AcquisitionbCreateView.as_view(), name='acquisitionb_create'),
    path('acquisitionb/update/<int:pk>/', AcquisitionbUpdateView.as_view(), name='acquisitionb_update'),
    path('acquisitionb/delete/<int:pk>/', AcquisitionbDeleteView.as_view(), name='acquisitionb_delete'),
    path('acquisitionb/invoice/pdf/<int:pk>/', AcquisitionbInvoicePdfView.as_view(), name='acquisitionb_invoice_pdf'),
    # project acquisition services
    path('acquisitionservices/list/', AcquisitionServicesListView.as_view(), name='acquisitionservices_list'),
    path('acquisitionservices/add/', AcquisitionServicesCreateView.as_view(), name='acquisitionservices_create'),
    path('acquisitionservices/update/<int:pk>/', AcquisitionServicesUpdateView.as_view(), name='acquisitionservices_update'),
    path('acquisitionservices/delete/<int:pk>/', AcquisitionServicesDeleteView.as_view(), name='acquisitionservices_delete'),
    path('acquisitionservices/invoice/pdf/<int:pk>/', AcquisitionServicesInvoicePdfView.as_view(), name='acquisitionservices_invoice_pdf'),
    # project informs
    path('informsuni/list/', InformsuniListView.as_view(), name='informsuni_list'),
    path('informsuni/add/', InformsuniCreateView.as_view(), name='informsuni_create'),
    path('informsuni/update/<int:pk>/', InformsuniUpdateView.as_view(), name='informsuni_update'),
    path('informsuni/delete/<int:pk>/', InformsuniDeleteView.as_view(), name='informsuni_delete'),
    path('informsuni/invoice/pdf/<int:pk>/', InformsuniInvoicePdfView.as_view(), name='informsuni_invoice_pdf'),
    # construcction
    path('construcction/list/', ConstrucctionListView.as_view(), name='construcction_list'),
    path('construcction/add/', ConstrucctionCreateView.as_view(), name='construcction_create'),
    path('construcction/update/<int:pk>/', ConstrucctionUpdateView.as_view(), name='construcction_update'),
    path('construcction/delete/<int:pk>/', ConstrucctionDeleteView.as_view(), name='construcction_delete'),
    path('construcction/invoice/pdf/<int:pk>/', ConstrucctionInvoicePdfView.as_view(), name='construcction_invoice_pdf'),
    path('construcction/invoicedet/pdf/<int:pk>/', ConstrucctiondetInvoicePdfView.as_view(), name='construcction_invoicedet_pdf'),
    # position
    path('position/list/', PositionListView.as_view(), name='position_list'),
    path('position/add/', PositionCreateView.as_view(), name='position_create'),
    path('position/update/<int:pk>/', PositionUpdateView.as_view(), name='position_update'),
    path('position/delete/<int:pk>/', PositionDeleteView.as_view(), name='position_delete'),
    # employer
    path('employer/list/', EmployerListView.as_view(), name='employer_list'),
    path('employer/add/', EmployerCreateView.as_view(), name='employer_create'),
    path('employer/update/<int:pk>/', EmployerUpdateView.as_view(), name='employer_update'),
    path('employer/delete/<int:pk>/', EmployerDeleteView.as_view(), name='employer_delete'),
    path('employer/invoice/pdf/<int:pk>/', EmployerInvoicePdfView.as_view(), name='employer_invoice_pdf'),
    # perfil
    path('perfil/list/', PerfilListView.as_view(), name='perfil_list'),
    path('perfil/add/', PerfilCreateView.as_view(), name='perfil_create'),
    path('perfil/update/<int:pk>/', PerfilUpdateView.as_view(), name='perfil_update'),
    path('perfil/delete/<int:pk>/', PerfilDeleteView.as_view(), name='perfil_delete'),
    path('perfil/invoice/pdf/<int:pk>/', PerfilInvoicePdfView.as_view(), name='perfil_invoice_pdf'),
    # budget
    path('budget/list/', BudgetListView.as_view(), name='budget_list'),
    path('budget/add/', BudgetCreateView.as_view(), name='budget_create'),
    path('budget/update/<int:pk>/', BudgetUpdateView.as_view(), name='budget_update'),
    path('budget/delete/<int:pk>/', BudgetDeleteView.as_view(), name='budget_delete'),
    path('budget/invoice/pdf/<int:pk>/', BudgetInvoicePdfView.as_view(), name='budget_invoice_pdf'),
    # certification
    path('certification/list/', CertificationListView.as_view(), name='certification_list'),
    path('certification/add/', CertificationCreateView.as_view(), name='certification_create'),
    path('certification/update/<int:pk>/', CertificationUpdateView.as_view(), name='certification_update'),
    path('certification/delete/<int:pk>/', CertificationDeleteView.as_view(), name='certification_delete'),
    path('certification/invoice/pdf/<int:pk>/', CertificationInvoicePdfView.as_view(), name='certification_invoice_pdf'),
    # treasury
    path('treasury/list/', TreasuryListView.as_view(), name='treasury_list'),
    path('treasury/add/', TreasuryCreateView.as_view(), name='treasury_create'),
    path('treasury/update/<int:pk>/', TreasuryUpdateView.as_view(), name='treasury_update'),
    path('treasury/delete/<int:pk>/', TreasuryDeleteView.as_view(), name='treasury_delete'),
    path('treasury/invoice/pdf/<int:pk>/', TreasuryInvoicePdfView.as_view(), name='treasury_invoice_pdf'),
    # productive
    path('productive/list/', ProductiveListView.as_view(), name='productive_list'),
    path('productive/add/', ProductiveCreateView.as_view(), name='productive_create'),
    path('productive/update/<int:pk>/', ProductiveUpdateView.as_view(), name='productive_update'),
    path('productive/delete/<int:pk>/', ProductiveDeleteView.as_view(), name='productive_delete'),
    path('productive/invoice/pdf/<int:pk>/', ProductiveInvoicePdfView.as_view(), name='productive_invoice_pdf'),
    path('productive/invoicedet/pdf/<int:pk>/', ProductivedetInvoicePdfView.as_view(), name='productive_invoicedet_pdf'),
	# path('productive/report/', ProductiveReportView.as_view(), name='productive_report'),
    
    # perfilprod
    path('perfilprod/list/', PerfilprodListView.as_view(), name='perfilprod_list'),
    path('perfilprod/add/', PerfilprodCreateView.as_view(), name='perfilprod_create'),
    path('perfilprod/update/<int:pk>/', PerfilprodUpdateView.as_view(), name='perfilprod_update'),
    path('perfilprod/delete/<int:pk>/', PerfilprodDeleteView.as_view(), name='perfilprod_delete'),
    path('perfilprod/invoice/pdf/<int:pk>/', PerfilprodInvoicePdfView.as_view(), name='perfilprod_invoice_pdf'),
    # publics
    path('publics/list/', PublicsListView.as_view(), name='publics_list'),
    path('publics/add/', PublicsCreateView.as_view(), name='publics_create'),
    path('publics/update/<int:pk>/', PublicsUpdateView.as_view(), name='publics_update'),
    path('publics/delete/<int:pk>/', PublicsDeleteView.as_view(), name='publics_delete'),
    path('publics/invoice/pdf/<int:pk>/', PublicsInvoicePdfView.as_view(), name='publics_invoice_pdf'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),

    ]
