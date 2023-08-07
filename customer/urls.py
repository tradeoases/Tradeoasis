from django.urls import path
from . import views

app_name = 'customer' 

urlpatterns = [
    path('key-metric-summary/', views.key_metric_summary, name='key_metric_summary'),
    path('rating-records/<int:agent_id>/', views.rating_records, name='rating_records'),
    path('line-or-area-charts/', views.line_or_area_charts, name='line_or_area_charts'),
    path('gauges-or-kpi-cards/', views.gauges_or_kpi_cards, name='gauges_or_kpi_cards'),
    path('performance-comparison/', views.performance_comparison, name='performance_comparison'),
    path('response-time-analytics/', views.response_time_analytics, name='response_time_analytics'),
    path('resolution-time-analytics/', views.resolution_time_analytics, name='resolution_time_analytics'),
    path('customer-satisfaction-ratings/', views.customer_satisfaction_ratings, name='customer_satisfaction_ratings'),
    path('agent-performance-reports/', views.agent_performance_reports, name='agent_performance_reports'),
    path('create-article/', views.create_article, name='create_article'),
    path('edit-article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('article-detail/<int:article_id>/', views.article_detail, name='article_detail'),
    path('search-articles/', views.search_articles, name='search_articles'),
    path('update-ticket-status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
    path('assign-ticket/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),
    path('transfer-ticket/<int:ticket_id>/', views.transfer_ticket, name='transfer_ticket'),
]
