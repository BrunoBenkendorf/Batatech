from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('aluno/', views.aluno, name='aluno'),
    path('professor/', views.professor, name='professor'),
    path('faleconosco/', views.faleconosco, name='faleconosco'),
    path('termo/', views.termo, name='termo'),
    path('privacidade/', views.privacidade, name='privacidade'),
    path('config/', views.config, name='config'),
    path('perfil/', views.perfil, name='perfil'),
    path('cadcurso', views.cadcurso, name='CadCurso'),
    # path('aluno/curso', views.curso, name='Curso'),  # ❌ comentado corretamente
    path('altera', views.altera, name='Altera'),
    path('seleciona', views.seleciona, name='Seleciona'),
    path('pagamento/', views.pagamento, name='pagamento'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('realizar_cadastro/', views.realizar_cadastro, name='realizar_cadastro'),
    path('verificar-email/', views.verificar_email, name='verificar_email'),
    path('salvarcurso/', views.salvarcurso, name='salvarcurso'),
    path('logout/', views.logout_view, name='logout'),
    path('curso/<int:id>/', views.curso, name='curso'),  # ✅ visualização
    path('curso/<int:curso_id>/detalhado/', views.curso_detalhado, name='curso_detalhado'),  # ✅ extra
    path('contato/', views.contato, name='contato'),
    path('processar_pagamento/', views.processar_pagamento, name='processar_pagamento'),
    path('salvar_material/', views.salvar_material, name='salvar_material'),
]
