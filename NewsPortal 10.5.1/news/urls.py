from django.urls import path

from .views import NewsList, NewsDetail, NewsFilterList, NewsCreate, NewsEdit, NewsDelete, \
CategoryListView, subscribe, HomeView

urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('search/', NewsFilterList.as_view(), name='post_search'),
    path('<int:pk>/', NewsDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/create/', NewsCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', NewsEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='articles_delete'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('home/', HomeView.as_view(), name='welcome_email_template')
]

