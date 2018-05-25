from django.urls import path

from .views import (HomePageView, WorkerCreateView, EmployerCreateView,
					 post_detail, PostCreateView, HomePageView,
					 PostListView,
					)

app_name = 'blog'

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
    path('signup/worker/', WorkerCreateView.as_view(), name='worker_signup'),
	path('signup/employer/', EmployerCreateView.as_view(), name="employer_signup"),
	path('postcreate/', PostCreateView.as_view(), name="post_create"),
	path('postlist/', PostListView.as_view(), name="postlist"),
	path('<str:year>/<str:slug>/', post_detail, name="post_detail"),
]
