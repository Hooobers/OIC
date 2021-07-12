from typing import List
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files.storage import FileSystemStorage


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# The upload methods for files on /upload/
def upload(request):
    context = {}
    
    # Checks for a call for POST
    if request.method == 'POST':

        # If the Convert button has been clicked
        if request.method == 'POST' and 'run_script' in request.POST:
            
            # Import function to run
            from blog.merge_and_convert import convert

            # Call function
            convert()

            # Display the csv file

        # If the Upload File button has been clicked.
        else:    
            uploaded_file = request.FILES['document']

            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)

            name = fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
    
    return render(request, 'blog/upload.html', context)



# def upload_csv(request):
#     data = {}
#     if "GET" == request.method:
#         return render(request, "myapp/upload_csv.html", data)
#     # if not GET, then proceed
#     try:
#         csv_file = request.FILES["csv_file"]
#         if not csv_file.name.endswith('.csv'):
#             messages.error(request,'File is not CSV type')
#             return HttpResponseRedirect(reverse("myapp:upload_csv"))
#             #if file is too large, return
#         if csv_file.multiple_chunks():
#             messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
#             return HttpResponseRedirect(reverse("myapp:upload_csv"))
            
#             file_data = csv_file.read().decode("utf-8")		
            
#             lines = file_data.split("\n")
#                 #loop over the lines and save them in db. If error , store as string and then display
#             for line in lines:						
#                 fields = line.split(",")
#                 data_dict = {}
#                 data_dict["name"] = fields[0]
#                 data_dict["start_date_time"] = fields[1]
#                 data_dict["end_date_time"] = fields[2]
#                 data_dict["notes"] = fields[3]
#                 try:
#                     form = EventsForm(data_dict)
#                     if form.is_valid():
#                         form.save()					
#                     else:
#                         logging.getLogger("error_logger").error(form.errors.as_json())												
#                 except Exception as e:
#                     logging.getLogger("error_logger").error(repr(e))					
#                     pass
                    
#     except Exception as e:
#         logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
#         messages.error(request,"Unable to upload file. "+repr(e))

#     return HttpResponseRedirect(reverse("myapp:upload_csv"))