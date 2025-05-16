const userInfo = document.getElementById('alunoinfo');
const dropdownMenu = document.getElementById('dropdownMenu');

userInfo.addEventListener('click', function (event) {
  event.stopPropagation();
  dropdownMenu.classList.toggle('show');
});

// Se clicar fora, fecha o menu
window.addEventListener('click', function (event) {
  if (!event.target.closest('#userDropdown') && dropdownMenu.classList.contains('show')) {
    dropdownMenu.classList.remove('show');
  }
});