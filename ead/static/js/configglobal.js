(function aplicarConfiguracoesGlobais() {
  const configSalva = localStorage.getItem('bataTechConfig');
  if (!configSalva) return;

  const config = JSON.parse(configSalva);

  // Aplica tema escuro com imagem
  if (config.temaEscuro) {
    document.body.style.backgroundImage = "url('/static/imagens/fundo.svg')";
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundRepeat = 'no-repeat';
    document.body.style.backgroundAttachment = 'fixed'; // para efeito fixo
    document.body.style.color = 'white';
  } else {
    // Tema claro com outra imagem
    document.body.style.backgroundImage = "url('/static/imagens/test.svg')";
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundRepeat = 'no-repeat';
    document.body.style.backgroundAttachment = 'fixed';
    document.body.style.color = 'black';
  }

  // Tradução do título
  const h1 = document.querySelector('h1');
  if (config.idioma === 'en' && h1) {
    h1.textContent = 'BataTECH - Courses';
  } else if (config.idioma === 'es' && h1) {
    h1.textContent = 'BataTECH - Cursos';
  }
})();
