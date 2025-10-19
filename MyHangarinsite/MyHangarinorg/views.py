from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from django.http import FileResponse
from django.conf import settings
from .models import Task, SubTask, Note, Category, Priority
from .forms import TaskForm, SubTaskForm, NoteForm, CategoryForm, PriorityForm
from django.db.models import Q
from django.utils import timezone
import os


class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic counts
        context["total_tasks"] = Task.objects.count()
        context["total_subtasks"] = SubTask.objects.count()
        context["total_notes"] = Note.objects.count()
        context["total_categories"] = Category.objects.count()
        context["total_priorities"] = Priority.objects.count()
        
        # Task status counts - using case-insensitive contains for flexibility
        context["completed_tasks"] = Task.objects.filter(status__icontains='complete').count()
        context["in_progress_tasks"] = Task.objects.filter(status__icontains='progress').count()
        context["pending_tasks"] = Task.objects.filter(status__icontains='pending').count()
        
        # Yearly statistics
        today = timezone.now().date()
        context["tasks_created_this_year"] = Task.objects.filter(created_at__year=today.year).count()
        
        return context


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(status__icontains=query) |
                Q(category__name__icontains=query) |
                Q(priority__name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['title', '-title', 'status', '-status', 'category__name', '-category__name', 
                  'priority__name', '-priority__name', 'created_at', '-created_at', 'deadline', '-deadline']
        sort_by = self.request.GET.get("sort_by")
        
        if sort_by in allowed:
            return sort_by
        return 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort_by', 'title')
        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task-list')


class SubTaskList(ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(status__icontains=query) |
                Q(parent_task__title__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['title', '-title', 'status', '-status', 'parent_task__title', '-parent_task__title', 'created_at', '-created_at']
        sort_by = self.request.GET.get("sort_by")
        
        if sort_by in allowed:
            return sort_by
        return 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort_by', 'title')
        return context


class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_confirm_delete.html'
    success_url = reverse_lazy('subtask-list')


class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(task__title__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['content', '-content', 'task__title', '-task__title', 'created_at', '-created_at']
        sort_by = self.request.GET.get("sort_by")
        
        if sort_by in allowed:
            return sort_by
        return 'created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort_by', 'created_at')
        return context


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_confirm_delete.html'
    success_url = reverse_lazy('note-list')


# Category Views
class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['name', '-name', 'created_at', '-created_at']
        sort_by = self.request.GET.get("sort_by")
        
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort_by', 'name')
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# Priority Views
class PriorityList(ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ['name', '-name', 'created_at', '-created_at']
        sort_by = self.request.GET.get("sort_by")
        
        if sort_by in allowed:
            return sort_by
        return 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort_by', 'name')
        return context


class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_confirm_delete.html'
    success_url = reverse_lazy('priority-list')


# ✅ Add this at the very end
class ServiceWorkerView(View):
    """Serve the PWA serviceworker.js file from the static directory"""
    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.STATICFILES_DIRS[0], 'serviceworker.js')
        return FileResponse(open(file_path, 'rb'), content_type='application/javascript')
