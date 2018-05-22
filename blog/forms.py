from django import forms
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Worker, Comment, Post
from taggit.managers import TaggableManager

User = get_user_model()

class WorkerCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 	= forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 	= forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    tags		= forms.CharField(label='Tags', help_text='A comma-separated list of tags.')

    class Meta:
        model = User
        fields = ['username',]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(WorkerCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_staff = False
        user.save()

        tags = self.cleaned_data['tags'].replace(' ', '').split(',')
        Worker.objects.create(user=user)
        for i in tags:
        	user.worker.tags.add(i.lower())
        return user



class WorkerForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username 	= forms.CharField(label='Username')
    password1 	= forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 	= forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = ['tags']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # @transaction.atomic
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(WorkerCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_staff = False
        user.save()
        # tags = self.cleaned_data['tags'].strip().split(',')
        # print(tags)
        # worker = Worker.objects.create(user=user)
        # worker.tags.add(i for i in tags)
        # worker.save()
        return user


class EmployerCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email',]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmployerCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_staff = True

        if commit:
        	user.save()
        return user



class CommentCreateForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body',]
		

class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','body',]

    # def save(self, commit=True):
    #     post = super(EmployerCreateForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     user.is_active = True
    #     user.is_staff = True

    #     if commit:
    #     	user.save()
    #     return user
# class WorkerCreateForm(UserCreationForm):

# 	class Meta(UserCreationForm.Meta):
# 		model = User


# 	@transaction.atomic
# 	def save(self):
# 		user = super.save(commit=False)
# 		user.is_staff = False
# 		user.save()
# 		worker = Worker.objects.create(user=user)
# 		return user


# class EmployerCreateForm(UserCreationForm):

# 	class Meta(UserCreationForm.Meta):
# 		model = User


# 	def save(self):
# 		user = super.save(commit=False)
# 		user.is_staff = True
# 		if commit:
# 			user.save()
# 		return user



