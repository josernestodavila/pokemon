from django.http import HttpResponse


def healthcheck(request):
    return HttpResponse("Healthy: OK", content_type="text/plain")
