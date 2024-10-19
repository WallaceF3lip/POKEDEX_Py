document.getElementById('searchInput').addEventListener('input', function() {
  const termo = this.value.trim();
  if (termo !== '') {
    fetch(`/search_like?termo=${encodeURIComponent(termo)}`)
      .then(response => response.json())
      .then(data => {
        const listaResultados = document.getElementById('list-results');
        listaResultados.className = 'form-select';
        listaResultados.setAttribute = 'size', '2';
        listaResultados.innerHTML = '';
        data.sort().forEach(resultado => {
          const itemLista = document.createElement('option');
          itemLista.textContent = resultado;
          listaResultados.appendChild(itemLista);
        });
      })
      .catch(error => {
        console.error('Erro ao buscar resultados:', error);
      });
  } else {
    document.getElementById('list-results').innerHTML = '';
  }
});

function selecionarOpcao() {
  const select = document.getElementById('list-results');
  const input = document.getElementById('searchInput');
  
  select.addEventListener('change', function() {
    const opcaoSelecionada = select.options[select.selectedIndex].value;
    input.value = opcaoSelecionada;
  });
}

window.onload = function() {
  selecionarOpcao();
};