from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),

    path('people/', views.PersonListView.as_view(), name='people'),
    path('person/<int:pk>/', views.PersonDetailView.as_view(), name='person_detail'),
    path('person/<int:pk>/delete/', views.PersonDeleteView.as_view(), name='person_delete'),
    path('person/<int:pk>/update/', views.PersonUpdateView.as_view(), name='person_update'),
    path('person/filter/', views.PersonFilterView.as_view(), name='person_filter'), 

    path('competitions/', views.CompetitionListView.as_view(), name='competitions'),
    path('competition/<int:pk>/', views.CompetitionDetailView.as_view(), name='competition_detail'),

    path('result/<int:pk>/', views.ResultDetailView.as_view(), name='result_detail'),
    path('result/new/', views.ResultCreateView.as_view(), name='result_new'),
    path('result/<int:pk>/delete/', views.ResultDeleteView.as_view(), name='result_delete'),
    path('result/<int:pk>/update/', views.ResultUpdateView.as_view(), name='result_update'),
    path('result/filter/', views.ResultFilterView.as_view(), name='result_filter')
]
