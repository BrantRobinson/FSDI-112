from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView): # class-based view
    template_name = "pages/home.html"

class AboutPageView(TemplateView): # class-based view
    template_name = "pages/about.html"

