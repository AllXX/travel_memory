from django.urls import path,include
from . import views


app_name = 'memory'

urlpatterns = [
    path('',views.home,name='home'),
    path('mymap',views.mymap,name='mymap'),
    path('signup',views.AccountRegistration.as_view(),name='signup'),
    path('login',views.Login,name='login'),
    path('logout',views.Logout,name="logout"),
    path('memory',views.memory,name='memory'),
    path('post_create', views.MemoryCreate.as_view(),name='post_create'),
    path('delete/<int:pk>',views.MemoryDelete.as_view(),name='delete'),
    path('edit/<int:pk>/', views.MemoryEdit.as_view(), name='edit'),
    path('detail/<int:pk>',views.MemoryDetail.as_view(),name='detail'),
    path('profile',views.profile,name='profile'),
    path('howtouse',views.howtouse,name="how-to-use"),
    path('rule',views.rule,name="rule"),
    path('policy',views.policy,name='policy')
]