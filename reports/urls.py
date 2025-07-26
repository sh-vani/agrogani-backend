# reports/urls.py
from django.urls import path
from .views import (SummaryAPIView,CropWiseReportAPIView,FinancialSummaryView,
                    CropDetailReportAPIView,MonthlyTrendsAPIView,
                    IncomeSourcesAPIView,ExpenseBreakdownAPIView)
        #  ExportReportPDFAPIView

urlpatterns = [
    path('summary/', SummaryAPIView.as_view(), name='report-summary'),
    path('report/crop-wise/', CropWiseReportAPIView.as_view(), name='report-crop-wise'),
    path('report/crop/<int:crop_id>/details/', CropDetailReportAPIView.as_view(), name='report-crop-details'),
    path('report/trends/', MonthlyTrendsAPIView.as_view(), name='report-trends'),
     path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),

    path('report/income/', IncomeSourcesAPIView.as_view(), name='report-income'),
    path('report/expenses/', ExpenseBreakdownAPIView.as_view(), name='report-expenses'),
    #    path('report/export/pdf/', ExportReportPDFAPIView.as_view(), name='report-export-pdf'),
]


# from .views import ShareReportAPIView

# urlpatterns += [
#     path('report/share/', ShareReportAPIView.as_view(), name='report-share'),
# ]
