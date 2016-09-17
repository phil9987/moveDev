from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'index.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            pass
        return self.render_to_response({})
