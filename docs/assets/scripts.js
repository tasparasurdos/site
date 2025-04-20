$(document).ready(function() {
  // Estado dos filtros
  var activeFilters = {
    query: '',
    categoria: null,
    etapa: null,
    custo: null,
    plataforma: null,
    requerInternet: null
  };

  // Aplica filtros na lista de tecnologias
  function filterTecnologias() {
    var anyVisible = false;
    $('.item-tecnologia').each(function() {
      var $item = $(this);
      var text = $item.data('titulo').toLowerCase();
      var apresent = $item.data('apresentacao');
      var categoria = $item.data('categoria');
      var etapa = $item.data('etapas');
      var custo = $item.data('custo');
      var plataforma = $item.data('plataforma');
      var requerInternet = $item.data('requer-internet');

      var visible = true;
      // Filtro texto
      if (activeFilters.query && text.indexOf(activeFilters.query) === -1 && apresent.indexOf(activeFilters.query) === -1) {
        visible = false;
      }
      // Filtro categoria
      if (activeFilters.categoria && categoria !== activeFilters.categoria) {
        visible = false;
      }
      // Filtro etapa
      if (activeFilters.etapa && (!etapa || etapa.indexOf(activeFilters.etapa.toLowerCase()) === -1)) {
        visible = false;
      }
      // Filtro custo
      if (activeFilters.custo && custo !== activeFilters.custo) {
        visible = false;
      }
      // Filtro plataforma
      if (activeFilters.plataforma && plataforma.indexOf(activeFilters.plataforma.toLowerCase()) === -1) {
        visible = false;
      }
      // Filtro requer internet
      if (activeFilters.requerInternet && requerInternet !== activeFilters.requerInternet) {
        visible = false;
      }

      if (visible) {
        $item.show();
        anyVisible = true;
      } else {
        $item.hide();
      }
    });
    // Mensagem sem resultados
    if (!anyVisible) {
      $('#no-results').show();
    } else {
      $('#no-results').hide();
    }
  }

  // Filtro de texto para tecnologias
  $('#filtro-tecnologias').on('input', function() {
    activeFilters.query = $(this).val().toLowerCase();
    $('#clear-filters').show();
    filterTecnologias();
  });

  // Eventos de clique nos dropdowns
  $('.dropdown-item').on('click', function(e) {
    e.preventDefault();
    var value = $(this).data('value');
    var $btn = $(this).closest('.dropdown').find('button');
    var key = $btn.attr('id').replace('-filter', '');
    activeFilters[key] = value;
    $btn.text(value)
        .removeClass('btn-outline-secondary opacity-75')
        .addClass('btn-secondary');
    $('#clear-filters').show();
    filterTecnologias();
  });

  // Botão limpar filtros
  $('#clear-filters').on('click', function() {
    activeFilters = {query: '', categoria: null, etapa: null, custo: null, plataforma: null, requerInternet: null};
    $('#filtro-tecnologias').val('');
    $('button[data-label]').each(function() {
      var $b = $(this);
      $b.text($b.data('label'))
        .removeClass('btn-secondary')
        .addClass('btn-outline-secondary opacity-75');
    });
    $(this).hide();
    filterTecnologias();
  });

  // Filtro de recursos por texto
  $('#filtro-recursos').on('input', function() {
    var q = $(this).val().toLowerCase();
    var anyVisibleR = false;
    $('.item-recurso').each(function() {
      var $it = $(this);
      var titulo = $it.data('titulo').toLowerCase();
      var categoria = $it.data('categoria').toLowerCase();
      var plataforma = $it.data('plataforma').toLowerCase();
      var descricao = $it.find('p').first().text().toLowerCase();
      var vis = !q || titulo.indexOf(q) !== -1 || categoria.indexOf(q) !== -1 || plataforma.indexOf(q) !== -1 || descricao.indexOf(q) !== -1;
      if (vis) {
        $it.show();
        anyVisibleR = true;
      } else {
        $it.hide();
      }
    });
    if (!anyVisibleR) {
      $('#no-results-recursos').show();
    } else {
      $('#no-results-recursos').hide();
    }
  });
});
