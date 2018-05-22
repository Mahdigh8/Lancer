from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import WorkerCreateView, EmployerCreateView, WorkerPostView, EmployerPostView, post_detail, PostCreateView, HomePageView


app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
	path('signup/worker/', WorkerCreateView.as_view(), name='worker_signup'),
	path('signup/employer/', EmployerCreateView.as_view(), name="employer_signup"),
	path('worker/postlist/', WorkerPostView.as_view(), name="worker_postlist"),
	path('employer/postlist/', EmployerPostView.as_view(), name="employer_postlist"),
	path('<str:year>/<str:slug>/', post_detail, name="post_detail"),
	path('employer/post/create/', PostCreateView.as_view(), name="post_create"),
]
