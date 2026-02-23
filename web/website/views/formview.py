from django.views.generic import TemplateView

class MyTestView(TemplateView):
    template_name = "website/test.html"