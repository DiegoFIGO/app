from django.urls import path

from core.reports.views import ReportSaleView, ProductiveReportView

urlpatterns = [
	# reports
	path('sale/', ReportSaleView.as_view(), name='sale_report'),
 	path('productive', ProductiveReportView.as_view(), name='productive_report'),

]