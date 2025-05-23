from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Professor, MensagemContato, Curso, Matricula, Arquivo, Modulo, Aula,Avaliacao, Questao, QuestaoHasAvaliacao,RespostaAluno
from .models import Aluno, Professor, MensagemContato, Curso, Matricula, Arquivo, Modulo, Aula
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.contrib import messages


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
        return redirect('home')
        return HttpResponse("Mensagem enviada com sucesso!")

    return render(request, 'TelaFaleConosco.html')

def termo(request):
    return render(request, 'TelaTermo.html')

def privacidade(request):
    return render(request, 'TelaPrivacidade.html')

def config(request):
    return render(request, 'TelaConfig.html')

def cadastro(request):
    return render(request, 'TelaCadastro.html')

def cadcurso(request):
    return render(request, 'TelaCadCurso.html')

def perfil(request):
    return render(request, 'TelaPerfil.html')

def professor(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login') 

    professor = get_object_or_404(Professor, id_professor=professor_id)
    return render(request, 'TelaProfessor.html', {'professor': professor})

def curso(request, id):
    curso_obj = get_object_or_404(Curso, id_curso=id)
    arquivos = Arquivo.objects.filter(aula_id_aula__modulo_id_modulo__curso_id_curso=curso_obj)


    avaliacoes = Avaliacao.objects.filter(modulo_id_modulo__curso_id_curso=curso_obj)

    return render(request, 'TelaCurso.html', {
        'curso': curso_obj,
        'arquivos': arquivos,
        'avaliacoes': avaliacoes
    })

    return render(request, 'TelaCurso.html', {
        'curso': curso_obj,
        'arquivos': arquivos
    })


def aluno(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login') 

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)

    matriculas = Matricula.objects.filter(id_aluno=aluno).select_related('id_curso')
    cursos = [m.id_curso for m in matriculas]

    pagamento_sucesso = request.session.pop('pagamento_sucesso', False)

    return render(request, 'TelaAluno.html', {
        'aluno': aluno,
        'cursos': cursos,
        'pagamento_sucesso': pagamento_sucesso
    })

def altera(request):
    curso_id = request.GET.get('id')
    if not curso_id:
        return HttpResponse("ID do curso não fornecido.", status=400)

    curso = get_object_or_404(Curso, id_curso=curso_id)
    return render(request, 'TelaAltCurso.html', {'curso': curso})

def seleciona(request):
    cursos = Curso.objects.all()
    return render(request, 'TelaSelecionarCurso.html', {
        'cursos': cursos
    })

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

def salvar_material(request):
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descricao = request.POST.get("descricao")
        curso_id = request.POST.get("curso_id")
        arquivo = request.FILES.get("arquivo")
        professor_id = request.session.get("professor_id")

        if not all([tipo, descricao, curso_id, arquivo, professor_id]):
            return HttpResponse("Dados incompletos", status=400)

        curso = get_object_or_404(Curso, id_curso=curso_id)
        professor = get_object_or_404(Professor, id_professor=professor_id)

        modulo, _ = Modulo.objects.get_or_create(nome="Geral", curso_id_curso=curso)

        aula = Aula.objects.create(
            titulo=f"{tipo.capitalize()} - {descricao}",
            modulo_id_modulo=modulo,
            professor_id_professor=professor
        )

        Arquivo.objects.create(
            tipo=tipo,
            descricao=descricao,
            url_arquivo=arquivo,  # ✅ Salva o arquivo corretamente
            aula_id_aula=aula
        )

        return redirect('professor')

    return HttpResponse("Método não permitido", status=405)

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

        Matricula.objects.get_or_create(
            id_aluno_id=aluno_id,
            id_curso=curso_obj,
            defaults={'data_matricula': date.today()}
        )

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
        
        
def criar_avaliacao(request):
    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        titulo = request.POST.get('titulo')
        quantidade_questoes = request.POST.get('quantidade_questoes')

        curso = get_object_or_404(Curso, id_curso=curso_id)
        modulo, _ = Modulo.objects.get_or_create(nome='Provas', curso_id_curso=curso)

        avaliacao = Avaliacao.objects.create(
            titulo=titulo,
            modulo_id_modulo=modulo
        )

        # Aqui você pode usar a quantidade de questões para lógica futura
        if quantidade_questoes:
            request.session['quantidade_questoes'] = quantidade_questoes

        return redirect('adicionar_questoes', avaliacao.id_avaliacao)

    elif request.method == 'GET':
        curso_id = request.GET.get('curso_id')
        curso = get_object_or_404(Curso, id_curso=curso_id)

        return render(request, 'TelaCriarAvaliacao.html', {'curso_id': curso_id, 'curso': curso})

    return HttpResponse("Método não permitido", status=405)
def adicionar_questoes(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id_avaliacao=avaliacao_id)

    # Recupera a quantidade desejada da sessão
    quantidade_questoes = int(request.session.get('quantidade_questoes', 0))

    # Conta quantas questões já estão cadastradas para essa avaliação
    total_questoes = QuestaoHasAvaliacao.objects.filter(avaliacao_id_avaliacao=avaliacao).count()

    if request.method == 'POST':
        enunciado = request.POST.get('enunciado')
        alternativa_a = request.POST.get('alternativa_a')
        alternativa_b = request.POST.get('alternativa_b')
        alternativa_c = request.POST.get('alternativa_c')
        alternativa_d = request.POST.get('alternativa_d')
        resposta_correta = request.POST.get('resposta_correta')

        questao = Questao.objects.create(
            enunciado=enunciado,
            tipo='prova',
            alternativa_a=alternativa_a,
            alternativa_b=alternativa_b,
            alternativa_c=alternativa_c,
            alternativa_d=alternativa_d,
            resposta_correta=resposta_correta
        )

        QuestaoHasAvaliacao.objects.create(
            questao_id_questao=questao,
            avaliacao_id_avaliacao=avaliacao
        )

        total_questoes += 1

        # Verifica se já atingiu a quantidade desejada
        if total_questoes >= quantidade_questoes:
            # Limpa a sessão para não afetar outras provas futuras
            request.session.pop('quantidade_questoes', None)
            return redirect('professor')  # Redireciona para a tela do professor ou outra página

        return redirect('adicionar_questoes', avaliacao_id=avaliacao.id_avaliacao)

    return render(request, 'TelaAddQuestao.html', {'avaliacao': avaliacao, 'total_questoes': total_questoes, 'quantidade_questoes': quantidade_questoes})

def responder_prova(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id_avaliacao=avaliacao_id)
    questoes = Questao.objects.filter(questaohasavaliacao__avaliacao_id_avaliacao=avaliacao)
    aluno_id = request.session.get('aluno_id')
    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)

    if request.method == 'POST':
        for questao in questoes:
            resposta = request.POST.get(f'questao_{questao.id_questao}')
            if resposta:
                RespostaAluno.objects.create(
                    aluno=aluno,
                    avaliacao=avaliacao,
                    questao=questao,
                    resposta_escolhida=resposta
                )
        messages.success(request, "Prova enviada com sucesso!")
        return redirect('curso', id=avaliacao.modulo_id_modulo.curso_id_curso.id_curso)

    return render(request, 'TelaResponderProva.html', {
        'avaliacao': avaliacao,
        'questoes': questoes
    })
def visualizar_resultados(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id_avaliacao=avaliacao_id)
    aluno_id = request.GET.get('aluno') or request.session.get('aluno_id')
    professor_id = request.session.get('professor_id')

    if not aluno_id and not professor_id:
        return redirect('login')

    respostas = RespostaAluno.objects.filter(avaliacao=avaliacao, aluno_id=aluno_id)

    resultados = []
    for resposta in respostas:
        correto = resposta.resposta_escolhida == resposta.questao.resposta_correta
        resultados.append({
            'questao': resposta.questao,
            'resposta': resposta.resposta_escolhida,
            'correta': resposta.questao.resposta_correta,
            'acertou': correto,
            'aluno': resposta.aluno
        })

    total_questoes = respostas.count()
    acertos = sum(1 for r in resultados if r['acertou'])

    return render(request, 'TelaResultadoProva.html', {
        'avaliacao': avaliacao,
        'resultados': resultados,
        'total_questoes': total_questoes,
        'acertos': acertos,
        'aluno': respostas[0].aluno if respostas else None
    })
def resultados_aluno(request):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login')

    avaliacoes = Avaliacao.objects.filter(respostaaluno__aluno_id=aluno_id).distinct()
    return render(request, 'TelaResultadoProvasAluno.html', {'avaliacoes': avaliacoes})

def resultados_professor(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login')

    # Obter avaliações ligadas ao professor (mesmo filtro do seu código)
    avaliacoes = Avaliacao.objects.filter(
        modulo_id_modulo__curso_id_curso__modulo__aula__professor_id_professor=professor_id
    ).distinct()

    avaliacoes_com_alunos = []
    for avaliacao in avaliacoes:
        # Pega alunos que responderam essa avaliação
        alunos_ids = RespostaAluno.objects.filter(avaliacao=avaliacao).values_list('aluno', flat=True).distinct()
        alunos = Aluno.objects.filter(id_aluno__in=alunos_ids)
        if alunos.exists():
            avaliacoes_com_alunos.append({
                'avaliacao': avaliacao,
                'alunos': alunos,
            })

    context = {
        'avaliacoes_com_alunos': avaliacoes_com_alunos,
    }
    return render(request, 'TelaResultadoProvasProfessor.html', context)


def detalhes_respostas(request, avaliacao_id, aluno_id):
    avaliacao = get_object_or_404(Avaliacao, pk=avaliacao_id)
    aluno = get_object_or_404(Aluno, pk=aluno_id)

    respostas = RespostaAluno.objects.filter(avaliacao=avaliacao, aluno=aluno).select_related('questao')

    context = {
        'avaliacao': avaliacao,
        'aluno': aluno,
        'respostas': respostas,
    }
    return render(request, 'DetalhesRespostasAluno.html', context)

