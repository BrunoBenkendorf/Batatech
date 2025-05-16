function trocarAba(id) {
  const abas = document.querySelectorAll('.conteudo-aba');
  const botoes = document.querySelectorAll('.aba');

  abas.forEach((aba) => aba.classList.remove('ativo'));
  botoes.forEach((btn) => btn.classList.remove('ativo'));

  document.getElementById(id).classList.add('ativo');
  event.target.classList.add('ativo');
}