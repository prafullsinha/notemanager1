from .views import HomeView, Signup, SearchView, FilterView, Filter1View, PostView, PersonalView, SortView
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
                  path('edit/<str:title>/', views.EditView, name="edit"),
                  path('', HomeView.as_view(), name='home'),
                  path('detail/<str:title>/', views.DetailView, name="detail"),
                  path('signup/', Signup.as_view(), name="signup"),
                  path('search/', SearchView.as_view(), name="search"),
                  path('filter/', FilterView.as_view(), name="filter"),
                  path('filter1/', Filter1View.as_view(), name="filter1"),
                  path('post/', PostView.as_view(), name="post"),
                  path('personal/', PersonalView.as_view(), name="personal"),
                  path('sort/', SortView.as_view(), name="sort"),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)