from django.shortcuts import render, redirect
from .models import Aluno, Professor,MensagemContato,Curso
from django.http import HttpResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
@csrf_exempt
def index(request):
    cursos = Curso.objects.all()
    return render(request, 'TelaHome.html', {'cursos': cursos})
def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            aluno = Aluno.objects.get(email=email, senha=senha)
            request.session['aluno_id'] = aluno.id_aluno # salva ID na sessão
            return redirect('aluno')
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
        return redirect('login')  # força login se não autenticado

    professor = get_object_or_404(Professor, id_professor=professor_id)
    return render(request, 'TelaProfessor.html', {'professor': professor})
def curso(request):
    return render(request=request, template_name='TelaCurso.html')
def aluno(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login')  # força login se não autenticado

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)
    return render(request, 'TelaAluno.html', {'aluno': aluno})
def altera(request):
    return render(request=request, template_name='TelaAltCurso.html')
def seleciona(request):
    return render(request=request, template_name='TelaSelecionarCurso.html')
def pagamento(request):
    nome_curso = request.GET.get('curso', '')
    valor = request.GET.get('valor', '')
    return render(request, 'TelaPagamento.html', {
        'nome_curso': nome_curso,
        'valor': valor
    })
def nr10(request):
    return render(request=request, template_name='TelaNR_10.html')
def nr12(request):
    return render(request=request, template_name='TelaNR_12.html')
def nr35(request):
    return render(request=request, template_name='TelaNR_35.html')
def informatica(request):
    return render(request=request, template_name='TelaInformaticaBasica.html')
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

        # Verifica se o e-mail já existe em Aluno ou Professor
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
            return HttpResponse("Curso cadastrado com sucesso!")
        except IntegrityError:
            return HttpResponse("Erro: Curso com esse nome já existe.")

def logout_view(request):
    request.session.flush()  # limpa todos os dados da sessão
    return redirect('login')
def processar_pagamento(request):
    if request.method == "POST":
        curso = request.POST.get("curso")
        valor = request.POST.get("valor")
        metodo = request.POST.get("pagamento")
        
        if metodo == "pix":
            chave_pix = request.POST.get("chave_pix")
            return HttpResponse(f"Pagamento via PIX com chave {chave_pix} para o curso {curso} no valor de R$ {valor} recebido.")

        elif metodo == "boleto":
            return HttpResponse(f"Boleto gerado com sucesso para o curso {curso} no valor de R$ {valor}.")

        elif metodo in ["debito", "credito"]:
            numero_cartao = request.POST.get("numero_cartao")
            validade = request.POST.get("validade")
            cvv = request.POST.get("cvv")
            parcelas = request.POST.get("parcelas") if metodo == "credito" else None
            return HttpResponse(f"Pagamento via {metodo.upper()} com cartão final {numero_cartao[-4:]} para o curso {curso} no valor de R$ {valor} recebido.")

        return HttpResponse("Método de pagamento inválido.", status=400)
    return HttpResponse("Método não permitido", status=405)
def curso_detalhado(request, curso_id):
    curso = get_object_or_404(Curso, id_curso=curso_id)
    return render(request, 'TelaCursoDetalhado.html', {'curso': curso})
def contato(request):
    return render(request, 'TelaContato.html')