from django.urls import path

from .views import (HomePageView, WorkerCreateView, EmployerCreateView,
					 post_detail, PostCreateView, HomePageView,
					 PostListView, ProfileUpdateView, PostEditView
					)

app_name = 'blog'

urlpatterns = [
	path('', HomePageView.as_view(), name='home'),
    path('signup/worker/', WorkerCreateView.as_view(), name='worker_signup'),
	path('signup/employer/', EmployerCreateView.as_view(), name="employer_signup"),
	path('postcreate/', PostCreateView.as_view(), name="post_create"),
	path('postlist/', PostListView.as_view(), name="postlist"),
	path('postlist/tag/<str:tag_slug>/', PostListView.as_view(), name="postlist_tag_slug"),
	path('profile/<str:pk>/', ProfileUpdateView.as_view(), name="profile"),
	path('<str:year>/<str:slug>/edit/', PostEditView.as_view(), name="post_edit"),
	path('<str:year>/<str:slug>/', post_detail, name="post_detail"),
]
