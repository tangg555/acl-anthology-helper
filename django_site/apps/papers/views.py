from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.

class LocalPapersView(View):
    """
    show local papers downloaded
    """
    def get(self, request):
        return render(request, 'apps/papers/local-papers.html', {})

