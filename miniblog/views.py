import datetime
import functools
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db import reset_queries, connection
from django.db.models import F, Max, Count, Prefetch
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from miniblog.forms import ProfileForm

from miniblog.models import Blog, User, Comment, Profile
from . import serializers as s


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
        query = self.request.GET.get('q')
        object_list = Blog.objects.select_related('author').annotate(last_update=Coalesce(Max('comment__pub_date'), 'pub_date')).\
            order_by(F('last_update').desc(nulls_last=False))
        if query:
            object_list = object_list.filter(name__icontains=query)
        return object_list
        

class BloggerListView(generic.ListView):
    model = User
    # model = Profile
    paginate_by = 10
    template_name = 'miniblog/blogger_list.html'

    def get_queryset(self):
        return User.objects.exclude(blog__isnull=True).annotate(blogs_num=Count('blog')).\
            order_by(F('blogs_num').desc(nulls_last=True), 'username')


class BlogDetailView(generic.DetailView):
    model = Blog


class BloggerDetailView(generic.DetailView):
    model = User
    template_name = 'miniblog/blogger_detail.html'
    

# class NewProfileView(generic.FormView):
#     template_name = "miniblog/profile.html"
#     form_class = ProfileForm

#     def form_valid(self, form):
#         form.save(self.request.user)
#         return super(NewProfileView, self).form_valid(form)

#     def get_success_url(self, *args, **kwargs):
#         return reverse("index")


class EditProfileView(generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "miniblog/profile.html"
     
    def get_object(self, *args, **kwargs):
        # user = get_object_or_404(User, pk=self.kwargs['pk'])
        user = get_object_or_404(User, pk=self.request.user.pk)

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse("edit-user-profile")


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
        # form.instance.pub_date = datetime.datetime.now()
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})


# 1
# class BlogView(APIView):
#     @query_debugger
#     def get(self, request):
#         queryset = Blog.objects.select_related('author').all()
#         # blogs = []
#         #
#         # for blog in queryset:
#         #     blogs.append({'id': blog.id, 'name': blog.name, 'author': blog.author.username})
#         #
#         # return Response(blogs)
#
#         serializer = BlogSerializer(queryset, many=True)
#         return Response({"blogs": serializer.data})
#
#     def post(self, request):
#         blog = request.data.get('blog')
#
#         serializer = BlogSerializer(data=blog, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             blog_saved = serializer.save()
#         return Response({"success": "Blog '{}' created successfully".format(blog_saved.name)})
#
#     def put(self, request, pk):
#         saved_blog = get_object_or_404(Blog.objects.all(), pk=pk)
#         data = request.data.get('blog')
#         serializer = BlogSerializer(instance=saved_blog, data=data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             blog_saved = serializer.save()
#         return Response({
#             "success": "Blog '{}' updated successfully".format(blog_saved.name)
#         })
#
#     def delete(self, request, pk):
#         blog = get_object_or_404(Blog.objects.all(), pk=pk)
#         blog.delete()
#         return Response({
#             "message": "Blog with id `{}` has been deleted.".format(pk)
#         }, status=204)


# 2.1
# class BlogView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Blog.objects.select_related('author').all()
#     serializer_class = BlogSerializer
#
#     @query_debugger
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         author = get_object_or_404(User, id=self.request.data.get('author_id'))
#         return serializer.save(author=author)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# 2.2
# class BlogView(ListCreateAPIView):
#     queryset = Blog.objects.select_related('author').all()
#     serializer_class = BlogSerializer
#
#     def perform_create(self, serializer):
#         author = get_object_or_404(User, id=self.request.data.get('author_id'))
#         return serializer.save(author=author)
#
#
# class SingleBlogView(RetrieveUpdateDestroyAPIView):
#     queryset = Blog.objects.select_related('author').all()
#     serializer_class = BlogSerializer


# 3.1
# class BlogView(viewsets.ViewSet):
#
#     @query_debugger
#     def list(self, request):
#         queryset = Blog.objects.select_related('author').annotate(last_update=Coalesce(Max('comment__pub_date'), 'pub_date')).\
#             order_by(F('last_update').desc(nulls_last=False))
#         serializer = s.BlogSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     @query_debugger
#     def retrieve(self, request, pk=None):
#         queryset = Blog.objects.select_related('author').all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = s.BlogSerializer(user)
#         return Response(serializer.data)


# 3.2
class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = s.BlogSerializer
    queryset = Blog.objects.select_related('author').annotate(last_update=Coalesce(Max('comment__pub_date'), 'pub_date')).\
            order_by(F('last_update').desc(nulls_last=False))
    
    def get_queryset(self):
        object_list = self.queryset
        query = self.request.GET.get('q')
        if query:
            object_list = object_list.filter(name__icontains=query)
        return object_list
            
    def get_serializer_class(self):
        if self.action in ['list']:
            return s.BlogSerializer
        else:
            return s.BlogDetailSerializer

    # default value already set in models
    # def perform_create(self, serializer):
    #     date_list = [self.request.data.get('pub_date'), datetime.datetime.now()]
    #     pub_date = next(date for date in date_list if date)
    #     serializer.save(pub_date=pub_date)


class BloggerViewSet(viewsets.ModelViewSet):
    serializer_class = s.BloggerSerializer
    queryset = User.objects.select_related('profile').exclude(blog__isnull=True).annotate(blogs_num=Count('blog')).\
            order_by(F('blogs_num').desc(nulls_last=True), 'username')

    def get_serializer_class(self):
        if self.action in ['list']:
            return s.BloggerSerializer
        else:
            return s.BloggerDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = s.CommentSerializer
    queryset = Comment.objects.select_related('commented_blog').select_related('author').order_by(F('pub_date').desc(nulls_last=True))

    def get_serializer_class(self):
        if self.action in ['list']:
            return s.CommentSerializer
        else:
            return s.CommentDetailSerializer


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)