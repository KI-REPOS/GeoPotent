from django.urls import path
from . import views
from . import views_business

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('analyze/', views.AnalysisInputView.as_view(), name='analyze'),
    path('process/<int:analysis_id>/', views.ProcessAnalysisView.as_view(), name='process_analysis'),
    path('results/<int:analysis_id>/', views.ResultsView.as_view(), name='results'),
    path('report/<int:analysis_id>/', views.ReportView.as_view(), name='report'),
    path('report-download/<int:analysis_id>/', views.ReportDownloadView.as_view(), name='report_download'),
    
    # Business / Marketplace
    path('builders/', views_business.BuilderListView.as_view(), name='builder_list'),
    path('builders/<int:builder_id>/submit/', views_business.SubmitProposalView.as_view(), name='submit_proposal'),
    path('dashboard/', views_business.DashboardView.as_view(), name='dashboard'),
    path('proposals/<int:proposal_id>/', views_business.ProposalDetailView.as_view(), name='proposal_detail'),
]
