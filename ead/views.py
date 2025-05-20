from django.shortcuts import render, redirect
from .models import Aluno, Professor,MensagemContato,Curso,Matricula
from django.http import HttpResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from datetime import date

@csrf_exempt
def index(request):
    cursos = Curso.objects.all()
    aluno_id = request.session.get('aluno_id')
    return render(request, 'TelaHome.html', {
        'cursos': cursos,
        'aluno_logado': bool(aluno_id)
    })
def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            aluno = Aluno.objects.get(email=email, senha=senha)
            request.session['aluno_id'] = aluno.id_aluno
            return redirect('home')
        except Aluno.DoesNotExist:
            try:
                professor = Professor.objects.get(email=email, senha=senha)
                request.session['professor_id'] = professor.id_professor
                return redirect('professor')
            except Professor.DoesNotExist:
                return render(request, "TelaLogin.html", {
                    "erro": "E-mail ou senha inválidos. Tente novamente."
                })

    return render(request, "TelaLogin.html")
def faleconosco(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        assunto = request.POST.get("assunto")
        mensagem = request.POST.get("mensagem")

        MensagemContato.objects.create(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )
        return HttpResponse("Mensagem enviada com sucesso!")

    return render(request, 'TelaFaleConosco.html')
def termo(request):
    return render(request=request, template_name='TelaTermo.html')

def privacidade(request):
    return render(request=request, template_name='TelaPrivacidade.html')
def config(request):
    return render(request=request, template_name='TelaConfig.html')
def cadastro(request):
    return render(request=request, template_name='TelaCadastro.html')
def cadcurso(request):
    return render(request=request, template_name='TelaCadCurso.html')
def perfil(request):
    return render(request=request, template_name='TelaPerfil.html')
def professor(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login') 

    professor = get_object_or_404(Professor, id_professor=professor_id)
    return render(request, 'TelaProfessor.html', {'professor': professor})
def curso(request):
    return render(request=request, template_name='TelaCurso.html')
def aluno(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login') 

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)

    # Busca cursos matriculados
    matriculas = Matricula.objects.filter(id_aluno=aluno).select_related('id_curso')
    cursos = [m.id_curso for m in matriculas]

    # Checa se houve pagamento
    pagamento_sucesso = request.session.pop('pagamento_sucesso', False)

    return render(request, 'TelaAluno.html', {
        'aluno': aluno,
        'cursos': cursos,
        'pagamento_sucesso': pagamento_sucesso
    })
def altera(request):
    return render(request=request, template_name='TelaAltCurso.html')
def seleciona(request):
    return render(request=request, template_name='TelaSelecionarCurso.html')
def pagamento(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login')

    nome_curso = request.GET.get('curso', '')
    valor = request.GET.get('valor', '')

    return render(request, 'TelaPagamento.html', {
        'nome_curso': nome_curso,
        'valor': valor,
        'aluno_logado': True
    })
def realizar_cadastro(request):
    if request.method == "POST":
        perfil = request.POST.get("perfil")
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        cpf = request.POST.get("cpf")
        senha = request.POST.get("senha")

        nome_completo = f"{nome} {sobrenome}"

        if Aluno.objects.filter(email=email).exists() or Professor.objects.filter(email=email).exists():
            return HttpResponse("E-mail já cadastrado. Utilize outro e-mail.")

        try:
            if perfil == "aluno":
                Aluno.objects.create(
                    nome=nome_completo,
                    email=email,
                    telefone=telefone,
                    cpf=cpf,
                    senha=senha
                )

            elif perfil == "professor":
                formacao = request.POST.get("formacao")
                experiencia = request.POST.get("experiencia")

                Professor.objects.create(
                    nome=nome_completo,
                    email=email,
                    telefone=telefone,
                    cpf=cpf,
                    senha=senha,
                    formacao=formacao,
                    experiencia=experiencia
                )
            return redirect("login")
        except IntegrityError:
            return HttpResponse("Erro: Usuário com o CPF já cadastrado.")

    return HttpResponse("Método não permitido", status=405)
def verificar_email(request):
    email = request.GET.get('email')
    existe = Aluno.objects.filter(email=email).exists() or Professor.objects.filter(email=email).exists()
    return JsonResponse({'exists': existe})
def salvarcurso(request):
    if request.method == "POST":
        titulo = request.POST.get("tituloCurso")
        descricao = request.POST.get("descricaoCurso")
        objetivo = request.POST.get("Objetivo")
        duracao = request.POST.get("duracaoCurso")
        valor = request.POST.get('valorCurso')
        imagem = request.FILES.get("imagemCurso")
    
        try:
            Curso.objects.create(
                nome=titulo,
                descricao=descricao,
                carga_horaria=int(duracao.replace("h", "").strip()),
                objetivo=objetivo,
                valor=valor,
                imagem=imagem
            )
            return redirect("home")
        except IntegrityError:
            return HttpResponse("Erro: Curso com esse nome já existe.")

def logout_view(request):
    request.session.flush()  
    return redirect('login')
def processar_pagamento(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return HttpResponse("Apenas alunos logados podem realizar o pagamento.", status=403)

    if request.method == "POST":
        curso_nome = request.POST.get("curso")
        valor = request.POST.get("valor")
        metodo = request.POST.get("pagamento")

        try:
            curso_obj = Curso.objects.get(nome=curso_nome)
        except Curso.DoesNotExist:
            return HttpResponse("Curso não encontrado.", status=404)

        # Cria matrícula (evita duplicidade)
        Matricula.objects.get_or_create(
            id_aluno_id=aluno_id,
            id_curso=curso_obj,
            defaults={'data_matricula': date.today()}
        )

        # → Redireciona para a página do aluno após o pagamento
        request.session['pagamento_sucesso'] = True
        return redirect('aluno')

    return HttpResponse("Método não permitido", status=405)
def curso_detalhado(request, curso_id):
    curso = get_object_or_404(Curso, id_curso=curso_id)
    aluno_logado = 'aluno_id' in request.session
    return render(request, 'TelaCursoDetalhado.html', {
        'curso': curso,
        'aluno_logado': aluno_logado
    })
def contato(request):
    return render(request, 'TelaContato.html')