from django.shortcuts import render, redirect, get_object_or_404
from .models import Aluno, Professor, MensagemContato, Curso, Matricula, Arquivo, Modulo, Aula,Avaliacao,Questao, QuestaoHasAvaliacao,RespostaAluno,Forum, Postagem,ProgressoArquivo, Administrador
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from datetime import date
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http import FileResponse, Http404
import os


def index(request):
    cursos = Curso.objects.all()
    aluno_id = request.session.get('aluno_id')
    professor_id = request.session.get('professor_id')

    return render(request, 'TelaHome.html', {
        'cursos': cursos,
        'aluno_logado': bool(aluno_id),
        'professor_logado': bool(professor_id)
    })

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        # Lógica para Aluno
        try:
            aluno = Aluno.objects.get(email=email, senha=senha)
            if not aluno.is_active: # Adicionado: Verifica se o aluno está ativo
                return render(request, "TelaLogin.html", {
                    "erro": "Sua conta de aluno está inativa. Entre em contato com o suporte."
                })
            request.session['aluno_id'] = aluno.id_aluno
            return redirect('home')
        except Aluno.DoesNotExist:
            pass

        # Lógica para Professor
        try:
            professor = Professor.objects.get(email=email, senha=senha)
            if not professor.is_active: # Adicionado: Verifica se o professor está ativo
                return render(request, "TelaLogin.html", {
                    "erro": "Sua conta de professor está inativa. Entre em contato com o suporte."
                })
            request.session['professor_id'] = professor.id_professor
            return redirect('home')
        except Professor.DoesNotExist:
            pass
        
        # Lógica para Administrador (se ele usar esta mesma tela de login)
        try:
            administrador = Administrador.objects.get(email=email, senha=senha)
            # Para o admin, você pode decidir se ele também pode ser inativado ou se essa verificação é apenas para usuários normais
            # Se sim, adicione: if not administrador.is_active: ...
            request.session['admin_id'] = administrador.id_administrador
            return redirect('admin_dashboard') # Redireciona para o painel de admin
        except Administrador.DoesNotExist:
            pass

        # Se nenhuma das tentativas de login foi bem-sucedida
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

    arquivos_atividade = arquivos.filter(tipo="atividade")
    arquivos_biblioteca = arquivos.filter(tipo__in=["pdf", "video"])

    aluno_id = request.session.get('aluno_id')
    aluno = None
    progresso = 0
    visualizados_ids = []
    provas_concluidas = 0
    total_arquivos = arquivos.count()
    total_provas = avaliacoes.count()

    avaliacoes_status = []

    if aluno_id:
        aluno = get_object_or_404(Aluno, id_aluno=aluno_id)

        visualizados_ids = list(ProgressoArquivo.objects.filter(
            aluno=aluno,
            arquivo__in=arquivos,
            visualizado=True
        ).values_list('arquivo_id', flat=True))

        visualizados = len(visualizados_ids)

        provas_respondidas_ids = list(RespostaAluno.objects.filter(
            aluno=aluno,
            avaliacao__in=avaliacoes
        ).values_list('avaliacao_id', flat=True).distinct())

        provas_concluidas = len(provas_respondidas_ids)

        for avaliacao in avaliacoes:
            avaliacoes_status.append({
                'avaliacao': avaliacao,
                'respondida': avaliacao.id_avaliacao in provas_respondidas_ids
            })

        total_itens = total_arquivos + total_provas
        concluidos = visualizados + provas_concluidas
        progresso = round((concluidos / total_itens) * 100, 2) if total_itens else 0

    return render(request, 'TelaCurso.html', {
        'curso': curso_obj,
        'arquivos_atividade': arquivos_atividade,
        'arquivos_biblioteca': arquivos_biblioteca,
        'avaliacoes_status': avaliacoes_status,
        'aluno': aluno,
        'progresso': progresso,
        'total_arquivos': total_arquivos,
        'total_provas': total_provas,
        'visualizados_ids': visualizados_ids,
        'provas_concluidas': provas_concluidas,
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
        foto_perfil = request.FILES.get("foto_perfil")
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
                    senha=senha,
                    foto_perfil=foto_perfil
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
                    experiencia=experiencia,
                    foto_perfil=foto_perfil
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
            url_arquivo=arquivo,  # Salva o arquivo corretamente
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
def criar_forum(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login')

    cursos = Curso.objects.all()

    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')

        curso = get_object_or_404(Curso, id_curso=curso_id)

        Forum.objects.create(
            curso=curso,
            titulo=titulo,
            descricao=descricao
        )
        return redirect('professor')

    return render(request, 'TelaCriarForum.html', {'cursos': cursos})
def listar_foruns(request, curso_id):
    curso = get_object_or_404(Curso, id_curso=curso_id)
    foruns = Forum.objects.filter(curso=curso)

    return render(request, 'TelaForuns.html', {
        'curso': curso,
        'foruns': foruns
    })


def visualizar_forum(request, forum_id):
    forum = get_object_or_404(Forum, id_forum=forum_id)
    postagens = Postagem.objects.filter(forum=forum).order_by('data_postagem')

    if request.method == 'POST':
        conteudo = request.POST.get('conteudo')

        if 'aluno_id' in request.session:
            aluno = get_object_or_404(Aluno, id_aluno=request.session['aluno_id'])
            Postagem.objects.create(forum=forum, autor_aluno=aluno, conteudo=conteudo)
        elif 'professor_id' in request.session:
            professor = get_object_or_404(Professor, id_professor=request.session['professor_id'])
            Postagem.objects.create(forum=forum, autor_professor=professor, conteudo=conteudo)

        return redirect('visualizar_forum', forum_id=forum.id_forum)

    return render(request, 'TelaForumDetalhe.html', {
        'forum': forum,
        'postagens': postagens
    })
def seleciona_forum(request):
    professor_id = request.session.get('professor_id')
    if not professor_id:
        return redirect('login')

    cursos = Curso.objects.all()  # Ou filtrar por cursos do professor, se desejar

    return render(request, 'TelaSelecionarForum.html', {'cursos': cursos})
def perfil(request):
    aluno_id = request.session.get('aluno_id')
    professor_id = request.session.get('professor_id')

    usuario = None
    perfil_tipo = None

    if aluno_id:
        usuario = get_object_or_404(Aluno, id_aluno=aluno_id)
        perfil_tipo = 'aluno'
    elif professor_id:
        usuario = get_object_or_404(Professor, id_professor=professor_id)
        perfil_tipo = 'professor'
    else:
        return redirect('login')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')
        foto_perfil = request.FILES.get('foto_perfil')

        if nome and sobrenome:
            usuario.nome = f"{nome} {sobrenome}"
        if email:
            usuario.email = email
        if telefone:
            usuario.telefone = telefone
        if senha:
            usuario.senha = senha
        if foto_perfil:
            usuario.foto_perfil = foto_perfil

        if perfil_tipo == 'professor':
            formacao = request.POST.get('formacao')
            experiencia = request.POST.get('experiencia')
            if formacao:
                usuario.formacao = formacao
            if experiencia:
                usuario.experiencia = experiencia

        usuario.save()
        return redirect('home')

    nome_partes = usuario.nome.split(' ', 1)
    nome = nome_partes[0]
    sobrenome = nome_partes[1] if len(nome_partes) > 1 else ''

    context = {
        'usuario': usuario,
        'perfil_tipo': perfil_tipo,
        'nome': nome,
        'sobrenome': sobrenome,
    }
    return render(request, 'TelaPerfil.html', context)
def buscar_cursos(request):
    termo = request.GET.get('q', '')
    cursos = Curso.objects.filter(
        Q(nome__icontains=termo) | Q(descricao__icontains=termo)
    )

    aluno_id = request.session.get('aluno_id')
    professor_id = request.session.get('professor_id')

    return render(request, 'TelaResultadosBusca.html', {
        'cursos': cursos,
        'termo': termo,
        'aluno_logado': bool(aluno_id),
        'professor_logado': bool(professor_id)
    })

def altera(request):
    curso_id = request.GET.get('id')
    if not curso_id:
        return HttpResponse("ID do curso não fornecido.", status=400)

    curso = get_object_or_404(Curso, id_curso=curso_id)
    arquivos = Arquivo.objects.filter(aula_id_aula__modulo_id_modulo__curso_id_curso=curso)
    provas = Avaliacao.objects.filter(modulo_id_modulo__curso_id_curso=curso)
    foruns = Forum.objects.filter(curso=curso)

    return render(request, 'TelaAltCurso.html', {
        'curso': curso,
        'arquivos': arquivos,
        'provas': provas,
        'foruns': foruns,
    })
def deletar_arquivo(request, arquivo_id):
    curso_id = request.GET.get('curso_id')
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)
    arquivo.delete()
    return redirect(f'{reverse("Altera")}?id={curso_id}')

def editar_arquivo(request, arquivo_id):
    curso_id = request.GET.get('curso_id')
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)

    if request.method == 'POST':
        arquivo.tipo = request.POST.get('tipo')
        arquivo.descricao = request.POST.get('descricao')
        novo_arquivo = request.FILES.get('arquivo')
        if novo_arquivo:
            arquivo.url_arquivo = novo_arquivo
        arquivo.save()
        return redirect(f'{reverse("Altera")}?id={curso_id}')

    return render(request, 'TelaEditarArquivo.html', {
        'arquivo': arquivo,
        'curso_id': curso_id
    })
def deletar_prova(request, avaliacao_id):
    curso_id = request.GET.get('curso_id')
    avaliacao = get_object_or_404(Avaliacao, id_avaliacao=avaliacao_id)

    # Deletar as relações de QuestaoHasAvaliacao que referenciam essa avaliação
    QuestaoHasAvaliacao.objects.filter(avaliacao_id_avaliacao=avaliacao).delete()

    # Agora pode deletar a avaliação
    avaliacao.delete()

    return redirect(f'{reverse("Altera")}?id={curso_id}')
def deletar_forum(request, forum_id):
    curso_id = request.GET.get('curso_id')
    forum = get_object_or_404(Forum, id_forum=forum_id)
    forum.delete()
    return redirect(f'{reverse("Altera")}?id={curso_id}')
def registrar_visualizacao(request, arquivo_id):
    if request.method == 'POST':
        aluno_id = request.session.get('aluno_id')
        if not aluno_id:
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)

        aluno = get_object_or_404(Aluno, id_aluno=aluno_id)
        arquivo = get_object_or_404(Arquivo, id=arquivo_id)

        progresso, _ = ProgressoArquivo.objects.get_or_create(aluno=aluno, arquivo=arquivo)
        progresso.visualizado = True
        progresso.save()

        curso = arquivo.aula_id_aula.modulo_id_modulo.curso_id_curso
        progresso_percentual = calcular_progresso_arquivos(aluno, curso)

        return JsonResponse({
            'status': 'ok',
            'progresso': progresso_percentual
        })

    return JsonResponse({'error': 'Método não permitido'}, status=405)
def calcular_progresso_arquivos(aluno, curso):
    total_arquivos = Arquivo.objects.filter(
        aula_id_aula__modulo_id_modulo__curso_id_curso=curso
    ).count()

    if total_arquivos == 0:
        return 0

    visualizados = ProgressoArquivo.objects.filter(
        aluno=aluno,
        arquivo__aula_id_aula__modulo_id_modulo__curso_id_curso=curso,
        visualizado=True
    ).count()

    progresso = (visualizados / total_arquivos) * 100
    return round(progresso, 2)
def baixar_arquivo(request, arquivo_id):
    aluno_id = request.session.get('aluno_id')
    if not aluno_id:
        return redirect('login')

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)
    arquivo = get_object_or_404(Arquivo, id=arquivo_id)

    if not arquivo.url_arquivo:
        raise Http404("Arquivo não encontrado.")

    # Marca como visualizado
    progresso, _ = ProgressoArquivo.objects.get_or_create(aluno=aluno, arquivo=arquivo)
    progresso.visualizado = True
    progresso.save()

    caminho = arquivo.url_arquivo.path
    if os.path.exists(caminho):
        return FileResponse(open(caminho, 'rb'), as_attachment=True, filename=os.path.basename(caminho))
    else:
        raise Http404("Arquivo não encontrado no servidor.")

def admin_dashboard(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    admin = get_object_or_404(Administrador, id_administrador=admin_id)

    # Fetch data for admin dashboard
    total_cursos = Curso.objects.count()
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    recent_messages = MensagemContato.objects.order_by('-data_envio')[:5]

    context = {
        'admin': admin,
        'total_cursos': total_cursos,
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'recent_messages': recent_messages,
    }
    return render(request, 'TelaAdmin.html', context)

def gerenciar_cursos(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')
    cursos = Curso.objects.all().order_by('nome')
    return render(request, 'TelaGerenciarCursos.html', {'cursos': cursos})

def editar_curso(request, curso_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    curso = get_object_or_404(Curso, id_curso=curso_id)

    if request.method == 'POST':
        curso.nome = request.POST.get("nome")
        curso.descricao = request.POST.get("descricao")
        curso.objetivo = request.POST.get("objetivo")
        curso.carga_horaria = int(request.POST.get("carga_horaria").replace("h", "").strip())
        curso.valor = request.POST.get("valor")
        if request.FILES.get("imagem"):
            curso.imagem = request.FILES.get("imagem")
        curso.save()
        messages.success(request, "Curso atualizado com sucesso!")
        return redirect('gerenciar_cursos')
    return render(request, 'TelaEditarCurso.html', {'curso': curso})

def deletar_curso(request, curso_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    curso = get_object_or_404(Curso, id_curso=curso_id)
    curso.delete()
    messages.success(request, "Curso deletado com sucesso!")
    return redirect('gerenciar_cursos')

# Certifique-se de que sua função gerenciar_usuarios passa os dados corretos:
def gerenciar_usuarios(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login') # Redireciona se não for admin

    alunos = Aluno.objects.all().order_by('nome')
    professores = Professor.objects.all().order_by('nome')

    context = {
        'alunos': alunos,
        'professores': professores,
        # 'perfil_gerenciado': 'aluno' ou 'professor' ou 'administrador' (se você usar isso)
    }
    return render(request, 'TelaGerenciarUsuarios.html', context)

def editar_aluno(request, aluno_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)

    if request.method == 'POST':
        aluno.nome = request.POST.get("nome")
        aluno.email = request.POST.get("email")
        aluno.telefone = request.POST.get("telefone")
        aluno.cpf = request.POST.get("cpf")
        if request.POST.get("senha"):
            aluno.senha = request.POST.get("senha")
        if request.FILES.get("foto_perfil"):
            aluno.foto_perfil = request.FILES.get("foto_perfil")
        aluno.save()
        messages.success(request, "Aluno atualizado com sucesso!")
        return redirect('gerenciar_usuarios')
    return render(request, 'TelaEditarAluno.html', {'usuario': aluno, 'perfil_tipo': 'aluno'})

def deletar_aluno(request, aluno_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)
    aluno.delete()
    messages.success(request, "Aluno deletado com sucesso!")
    return redirect('gerenciar_usuarios')

def editar_professor(request, professor_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    professor = get_object_or_404(Professor, id_professor=professor_id)

    if request.method == 'POST':
        professor.nome = request.POST.get("nome")
        professor.email = request.POST.get("email")
        professor.telefone = request.POST.get("telefone")
        professor.cpf = request.POST.get("cpf")
        if request.POST.get("senha"):
            professor.senha = request.POST.get("senha")
        professor.formacao = request.POST.get("formacao")
        professor.experiencia = request.POST.get("experiencia")
        if request.FILES.get("foto_perfil"):
            professor.foto_perfil = request.FILES.get("foto_perfil")
        professor.save()
        messages.success(request, "Professor atualizado com sucesso!")
        return redirect('gerenciar_usuarios')
    return render(request, 'TelaEditarProfessor.html', {'usuario': professor, 'perfil_tipo': 'professor'})

def deletar_professor(request, professor_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')

    professor = get_object_or_404(Professor, id_professor=professor_id)
    professor.delete()
    messages.success(request, "Professor deletado com sucesso!")
    return redirect('gerenciar_usuarios')

def listar_mensagens_contato(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return redirect('login')
    mensagens = MensagemContato.objects.all().order_by('-data_envio')
    return render(request, 'TelaListarMensagensContato.html', {'mensagens': mensagens})
def inativar_aluno(request, aluno_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Acesso negado. Apenas administradores podem inativar alunos.")
        return redirect('login') # Ou para uma página de erro/dashboard

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)
    aluno.is_active = False
    aluno.save()
    messages.success(request, f"Aluno(a) {aluno.nome} inativado(a) com sucesso!")
    return redirect('gerenciar_usuarios') # Redireciona de volta para a tela de gerenciamento

def ativar_aluno(request, aluno_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Acesso negado. Apenas administradores podem ativar alunos.")
        return redirect('login') # Ou para uma página de erro/dashboard

    aluno = get_object_or_404(Aluno, id_aluno=aluno_id)
    aluno.is_active = True
    aluno.save()
    messages.success(request, f"Aluno(a) {aluno.nome} ativado(a) com sucesso!")
    return redirect('gerenciar_usuarios') # Redireciona de volta para a tela de gerenciamento

def inativar_professor(request, professor_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Acesso negado. Apenas administradores podem inativar professores.")
        return redirect('login') # Ou para uma página de erro/dashboard

    professor = get_object_or_404(Professor, id_professor=professor_id)
    professor.is_active = False
    professor.save()
    messages.success(request, f"Professor(a) {professor.nome} inativado(a) com sucesso!")
    return redirect('gerenciar_usuarios') # Redireciona de volta para a tela de gerenciamento

def ativar_professor(request, professor_id):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Acesso negado. Apenas administradores podem ativar professores.")
        return redirect('login') # Ou para uma página de erro/dashboard

    professor = get_object_or_404(Professor, id_professor=professor_id)
    professor.is_active = True
    professor.save()
    messages.success(request, f"Professor(a) {professor.nome} ativado(a) com sucesso!")
    return redirect('gerenciar_usuarios') # Redireciona de volta para a tela de gerenciamento

