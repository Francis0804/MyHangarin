from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data you want to pass to the template
        context['welcome_message'] = "Welcome to Hangarin Task Manager"
        return context