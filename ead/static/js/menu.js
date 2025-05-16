window.addEventListener("scroll", function () {
    let header = document.querySelector('#efeito')
    header.classList.toggle('rolagem', this.window.scrollY > 0)
})