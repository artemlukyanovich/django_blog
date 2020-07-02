# from django.contrib.auth.models import User
import datetime
import functools
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import reset_queries, connection
from django.db.models import F, Max, Count
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from rest_framework.response import Response
from rest_framework.views import APIView

from miniblog.models import Blog, User, Comment


# class CustomPermissionRequiredMixin(PermissionRequiredMixin):
#     def handle_no_permission(self):
#         if self.raise_exception:
#             raise PermissionDenied(self.get_permission_denied_message())
#         return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.5f}s")
        return result

    return inner_func


def index(request):
    return render(request, 'index.html', )


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.annotate(last_update=Coalesce(Max('comment__pub_date'), 'pub_date')).\
            order_by(F('last_update').desc(nulls_last=False))


class BloggerListView(generic.ListView):
    model = User
    paginate_by = 10
    template_name = 'miniblog/blogger_list.html'

    @query_debugger
    def get_queryset(self):
        return User.objects.exclude(blog__isnull=True).annotate(blogs_num=Count('blog')).\
            order_by(F('blogs_num').desc(nulls_last=True), 'username')


class BlogDetailView(generic.DetailView):
    model = Blog


class BloggerDetailView(generic.DetailView):
    model = User
    template_name = 'miniblog/blogger_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BloggerDetailView, self).get_context_data(**kwargs)
        context['blogger'] = context['user']
        context['user'] = self.request.user
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['description']

    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.commented_blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        form.instance.pub_date = datetime.datetime.now()
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})


class BlogView(APIView):
    @query_debugger
    def get(self, request):
        queryset = Blog.objects.select_related('author').all()
        blogs = []

        for blog in queryset:
            blogs.append({'id': blog.id, 'name': blog.name, 'author': blog.author.username})

        return Response(blogs)

