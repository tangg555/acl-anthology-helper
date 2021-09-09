from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.http import JsonResponse
from .data_process import load_papers_to_db

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
        query_set = load_papers_to_db(data['conference'], data['year'], data['content'])
        papers = []
        for one in query_set:
            papers.append({
                'conf': one.conf,
                'year': one.year,
                'conf_content': one.conf_content,
                'title': one.title,
                'authors': one.authors
            })

        return JsonResponse(papers, safe=False)
