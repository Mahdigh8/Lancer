from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth import login, get_user_model
from .utils import unique_slug_generator
from django.contrib.auth.decorators import login_required
from .decorators import worker_required, employer_required
from django.views.generic import DetailView, CreateView, ListView, UpdateView, TemplateView
from .forms import WorkerCreateForm, EmployerCreateForm, CommentCreateForm, PostCreateForm
from .models import Worker, Post, Comment
# Create your views here.

User = get_user_model()


class HomePageView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
        	context['is_staff'] = True
        else:
        	context['is_staff'] = False
        return context


class WorkerCreateView(CreateView):
	model = User
	template_name = 'blog/signup.html' 
	form_class = WorkerCreateForm
	success_url = '/blog/worker/postlist'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'Worker'
		kwargs['user_staff'] = False
		return super().get_context_data(**kwargs)

	# def form_valid(self, form):
	# 	user = form.save(commit=False)

	# 	worker = Worker.objects.create(user=user)
	# 	# worker.tags.add('')
	# 	return user

class EmployerCreateView(CreateView):
	model = User 
	template_name = 'blog/signup.html'
	form_class = EmployerCreateForm
	success_url = '/blog/employer/postlist'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'Employer'
		kwargs['user_staff'] = True
		return super().get_context_data(**kwargs)


@method_decorator([login_required, worker_required], name='dispatch')
class WorkerPostView(ListView):
	# queryset = Post.published.filter(tags__name__in=["delicious"])
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/worker_posts.html'

	def get_queryset(self):
		worker = Worker.objects.filter(user=self.request.user).first()
		tags_obj = worker.tags.all()
		tags = []
		for i in tags_obj:
			tags.append(i)
		return Post.published.filter(tags__name__in=tags).distinct()


@method_decorator([login_required, employer_required], name='dispatch')
class EmployerPostView(ListView):
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/employer_posts.html'

	def get_queryset(self):
		user_ = self.request.user
		return Post.published.filter(user=user_)

@method_decorator([login_required, employer_required], name='dispatch')
class PostCreateView(CreateView):
	model = Post
	fields = ['title', 'body', 'tags']
	# fields = '__all__'
	template_name = 'blog/post_create.html'
	success_url = '/blog/employer/postlist/'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.slug = unique_slug_generator(instance)
		instance.save()
		form.save_m2m()
		return HttpResponseRedirect(self.success_url)	


# class PostUpdateView(LoginRequiredMixin, UpdateView):

# 	context_object_name = 'post'
# 	template_name = 'blog/post_detail.html'

# 	form_class = CommentCreateForm
	
# 	def get_object(self, *args, **kwargs):
# 		slug = self.kwargs.get('slug')
# 		year = self.kwargs.get('year')
# 		return get_object_or_404(Post.published.all(), slug=slug, publish__year=year)


@login_required
def post_detail(request, year, slug):
	post = get_object_or_404(Post, slug=slug, status='published', publish__year=year)
	if request.user.is_staff:
		is_staff = True
	else:
		is_staff = False

	if request.user==post.user or not is_staff:
		is_allowed = True
	else:
		is_allowed = False

	if is_allowed:

		# List of active comments for this post
		comments = post.comments.filter(active=True)
		if request.method == 'POST':
			# A comment was posted
			comment_form = CommentCreateForm(data=request.POST)
			if comment_form.is_valid():
				# Create Comment object but don't save to database yet
				new_comment = comment_form.save(commit=False)
				# Assign the current post to the comment
				new_comment.post = post
				# Assign the username to the comment
				new_comment.name = request.user.username
				# Save the comment to the database
				new_comment.save()
		else:
			comment_form = CommentCreateForm()
		return render(
				request,
				'blog/post_detail.html',
				{'post': post,'comments': comments,
				'comment_form': comment_form,'is_staff':is_staff,
				'is_allowed':is_allowed}
				)
	else:
		return render(request, 'blog/user_not_allowed.html', {})
		# path = request.build_absolute_uri()
		# resolved_login_url = resolve_url(settings.LOGIN_URL)
		# redirect_field_name = REDIRECT_FIELD_NAME
		# return redirect_to_login(path, resolved_login_url, redirect_field_name)