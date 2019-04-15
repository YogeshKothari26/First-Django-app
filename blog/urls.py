from django.urls import path,re_path
from . import views


urlpatterns = [
    path('', views.clist, name='clist'),
    path('login', views.login, name='login'),
    path('login_submit', views.login_submit, name='login_submit'),
    path('create_indicator', views.create_indicator, name='create_indicator'),
    path('dashboard', views.display_dashboard, name='dashboard'),    
    path('manage/<int:pk>/delete_strat_group', views.delete_strat_group, name='delete_strat_group'),
    path('manage/<int:pk>/delete_watchlist', views.delete_watchlist, name='delete_watchlist'),
    path('manage', views.manage, name='manage'),
    path('manage/delete_all', views.delete_all, name='delete_all'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('submit_watchlist', views.submit_watchlist, name='submit_watchlist'),
    path('form_sub', views.form_sub, name='form_sub'),
    path('error', views.error, name='error'),

    re_path(r'(?P<task_id>[\w-]*)/revoke', views.revoke, name='revoke'),    
    re_path(r'(?P<selected_indicator>[\w|-|_]+)/indicator_popup', views.indicator_popup, name='indicator_popup'),
    re_path(r'(?P<task_id>[\w-]*)/get_progress', views.get_progress, name='get_progress'),    
]
