from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views import View
from .forms import CriarContaForm, FormHomePage
from django.contrib import messages
# Create your views here.


class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomePage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse("filme:login")
        else:
            return reverse("filme:criarconta")
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("filme:homefilmes")
        else:
            return super().get(request, *args, **kwargs)


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    
    # Contabilizar visualizações e adicionar a lista de filmes_vistos a partir do acesso
    def get(self, request, *args, **kwargs):
        # Descobrir qual filme está sendo acessado
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs) 


    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        # filtrar tabela de filmes pegando os filmes cuja categoria é igual a categoria do filme da página (object)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context["filmes_relacionados"] = filmes_relacionados
        return context



class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name='editarperfil.html'
    model = Usuario
    fields = ["first_name", "last_name", "email"]

    def get_success_url(self):
        return reverse('filme:homefilmes')

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            'Conta criada com sucesso! Faça login.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        email = self.request.POST.get('email', '').strip()

        if email and Usuario.objects.filter(
            email__iexact=email
        ).exists():
            messages.error(
                self.request,
                'Este e-mail já está cadastrado. '
                'Faça login com sua conta.'
            )
            return redirect('filme:login')

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('filme:login')

    

class LogoutViewCustom(View):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        return redirect('filme:logout')