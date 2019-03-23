from django.urls import path,re_path
from . import views


urlpatterns = [
    path('', views.clist, name='clist'),
    path('next', views.createstrategy, name='createstrategy'),
    path('submit', views.updatestrategy, name='updatestrategy'),
    path('dashboard', views.display_dashboard, name='dashboard'),
    path('manage', views.manage, name='manage'),
    path('stratgroup', views.stratgroup, name='stratgroup'),
    path('stratgroup/submit', views.stratgroupsubmit, name='stratgroupsubmit'),
    path('manage/<int:pk>/', views.strat_detail, name='strat_detail'),
    path('manage/<int:pk>/', views.strat_group_detail, name='strat_group_detail'),
    path('delete_all', views.delete_all, name='delete_all'),
    re_path(r'(?P<task_id>[\w-]*)/revoke', views.revoke, name='revoke'),    
    re_path(r'(?P<task_id>[\w-]*)/', views.get_progress, name='get_progress'),
]