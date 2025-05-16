(function aplicarConfiguracoesGlobais() {
  const configSalva = localStorage.getItem('bataTechConfig');
  if (!configSalva) return;

  const config = JSON.parse(configSalva);

  // Aplica tema escuro
  if (config.temaEscuro) {
    document.body.style.background = 'linear-gradient(#1a1a1a, #333)fixed';
    document.body.style.color = 'white';
  } else {
    document.body.style.background = 'linear-gradient(#fdf5ad, #fab663)fixed';
    document.body.style.color = 'black';
  }

  // Exemplo simples de tradução de título
  const h1 = document.querySelector('h1');
  if (config.idioma === 'en' && h1) {
    h1.textContent = 'BataTECH - Courses';
  } else if (config.idioma === 'es' && h1) {
    h1.textContent = 'BataTECH - Cursos';
  }

  // Você pode expandir isso para menus, botões, etc., com um sistema de tradução real
})();
