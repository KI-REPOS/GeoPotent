from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('analyze/', views.AnalysisInputView.as_view(), name='analyze'),
    path('process/<int:analysis_id>/', views.ProcessAnalysisView.as_view(), name='process_analysis'),
    path('results/<int:analysis_id>/', views.ResultsView.as_view(), name='results'),
    path('report/<int:analysis_id>/', views.ReportView.as_view(), name='report'),
    path('report-download/<int:analysis_id>/', views.ReportDownloadView.as_view(), name='report_download'),
]
