const cursos = [
  { id: 1, titulo: "Curso de JavaScript", descricao: "Aprenda JS do zero.", categoria: "Programação", objetivo: "Criar apps", duracao: "20h", turma: "Turma A" },
  { id: 2, titulo: "Curso de HTML e CSS", descricao: "Crie sites bonitos", categoria: "Design", objetivo: "Construir layouts", duracao: "15h", turma: "Turma B" },
  { id: 3, titulo: "Curso de Python", descricao: "Lógica e automações", categoria: "Programação", objetivo: "Automatizar tarefas", duracao: "25h", turma: "Turma C" }
];

function getCursoById(id) {
  return cursos.find(curso => curso.id === Number(id));
}

function carregarCurso() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  const curso = getCursoById(id);
  if (!curso) {
    alert("Curso não encontrado.");
    return;
  }

  document.getElementById('cursoId').value = curso.id;
  document.getElementById('tituloCurso').value = curso.titulo;
  document.getElementById('descricaoCurso').value = curso.descricao;
  document.getElementById('Categoria').value = curso.categoria;
  document.getElementById('Objetivo').value = curso.objetivo;
  document.getElementById('duracaoCurso').value = curso.duracao;
  document.getElementById('turma').value = curso.turma;
}

window.onload = carregarCurso;