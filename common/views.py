from django.shortcuts import render


# Create your views here.
def index(request):
    """Returns the landing page to navigate between Patient and Doctor
    Parameters:
        - request
    returns: common/index.html
    """
    return render(request, "common/index.html")