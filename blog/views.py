from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.utils import timezone
from taggit.models import Tag
from .utils import unique_slug_generator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .decorators import worker_required, employer_required
from django.views.generic import DetailView, CreateView, ListView, UpdateView, TemplateView
from .forms import WorkerCreateForm, EmployerCreateForm, CommentCreateForm
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
	success_url = '/login'

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
	success_url = '/login'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'Employer'
		kwargs['user_staff'] = True
		return super().get_context_data(**kwargs)



@method_decorator([login_required], name='dispatch')
class PostListView(ListView):
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/postlist.html'

	def get_queryset(self):
		tag_slug = None
		if 'tag_slug' in self.kwargs:
			tag_slug = self.kwargs['tag_slug']
		user_ = self.request.user
		if user_.is_staff:
			posts = Post.published.filter(user=user_)
		else:
			worker = Worker.objects.filter(user=user_).first()
			tags_obj = worker.tags.all()
			tags = []
			for i in tags_obj:
				tags.append(i)
			posts = Post.published.filter(tags__name__in=tags).distinct()
		if tag_slug:
			tag = get_object_or_404(Tag, slug=tag_slug)
			posts = posts.filter(tags__in=[tag])

		return posts


	def get_context_data(self, **kwargs):
		tag = None
		if 'tag_slug' in self.kwargs:
			tag = self.kwargs['tag_slug']
		kwargs['tag'] = tag
		kwargs['is_staff'] = self.request.user.is_staff
		return super().get_context_data(**kwargs)


@method_decorator([login_required, employer_required], name='dispatch')
class PostCreateView(CreateView):
	model = Post
	fields = ['title', 'body', 'tags']
	template_name = 'blog/post_create.html'
	success_url = '/'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.slug = unique_slug_generator(instance)
		instance.save()
		form.save_m2m()
		return HttpResponseRedirect(self.success_url)	


@login_required
def post_detail(request, year, slug):
	post = get_object_or_404(Post, slug=slug, status='published', publish__year=year)
	if request.user.is_staff:
		is_staff = True 
		# post_tags_ids = request.user.post.tags.values_list('id', flat=True)
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

		# List of similar posts
		post_tags_ids = post.tags.values_list('id', flat=True)
		similar_posts = Post.published.filter(tags__in=post_tags_ids)\
		.exclude(id=post.id)
		if request.user.is_staff:
			similar_posts = similar_posts.filter(user=request.user)
		else:
			similar_posts = similar_posts.filter(tags__in=request.user.worker.tags.all())
		similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
		.order_by('-same_tags','-publish')[:4]
		
		return render(
				request,
				'blog/post_detail.html',
				{'post': post,'comments': comments,
				'comment_form': comment_form,'is_staff':is_staff,
				'is_allowed':is_allowed,
				'similar_posts': similar_posts}
				)
	else:
		return render(request, 'blog/user_not_allowed.html', {})


@method_decorator([login_required, worker_required], name='dispatch')
class ProfileUpdateView(UpdateView):
	model = Worker
	fields = ['tags',]
	template_name = 'blog/profile_view.html'

    
@method_decorator([login_required, employer_required], name='dispatch')
class PostEditView(UpdateView):
	model = Post
	fields = ['title','body','tags',]
	template_name = 'blog/post_edit.html'
