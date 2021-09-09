from django.shortcuts import render, HttpResponse
from django.views.generic.base import View

# Create your views here.

class LocalPapersView(View):
    """
    show local papers downloaded
    """
    def get(self, request):
        return render(request, 'apps/papers/local-papers.html', {})

class DownloadPapersView(View):
    """
    list conferences that can be downloaded
    """
    def get(self, request):
        return render(request, 'apps/papers/download-papers.html', {})

class DownloadAjaxView(View):
    """

    """
    def get(self, request):
        return HttpResponse('ajax get succeed!')

    def post(self, request):
        data = request.POST
        info = data.get('conference-info')
        return HttpResponse(f'ajax post succeed! content: {info}')
