async function fetchData() {
  const termsResponse = await fetch('/terms/');
  const relationshipsResponse = await fetch('/relationships/');

  const terms = await termsResponse.json();
  const relationships = await relationshipsResponse.json();

  return {terms, relationships};
}

function createGraph(data) {
  const modal = document.getElementById('modal');
  const modalTitle = document.getElementById('modal-title');
  const modalContent = document.getElementById('modal-content');
  const closeButton = document.getElementById('close-button');

  closeButton.onclick = function() {
    modal.close();
  };

  const {terms, relationships} = data;

  const elements = [];

  terms.forEach(term => {
    elements.push({
      data: {
        id: `term${term.id}`,
        label: term.name,
        description: term.description,
      },
    });
  });

  relationships.forEach(rel => {
    elements.push({
      data: {
        id: `rel${rel.id}`,
        source: `term${rel.term_1_id}`,
        target: `term${rel.term_2_id}`,
        label: rel.relation_type,
      },
    });
  });

  const cy = cytoscape({
    container: document.getElementById('network'),
    elements: elements,
    style: [
      {
        selector: 'node',
        style: {
          'cursor': 'pointer',
          'label': 'data(label)',
          'text-valign': 'center',
          'text-halign': 'center',
          'background-color': '#607D8B',
          'color': '#fff',
          'font-size': '12px',
          'width': '70px',
          'height': '70px',
          'shape': 'ellipse',
          'overlay-opacity': 0,
        },
      },
      {
        selector: 'edge',
        style: {
          'label': 'data(label)',
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'arrow-scale': 1.5,
          'line-color': '#B0BEC5',
          'target-arrow-color': '#B0BEC5',
          'color': '#37474F',
          'font-size': '10px',
          'text-background-color': '#ECEFF1',
          'text-background-opacity': 1,
          'text-background-shape': 'roundrectangle',
          'text-border-color': '#CFD8DC',
          'text-border-width': 1,
          'text-border-opacity': 1,
          'text-background-padding': 2,
        },
      },
      {
        selector: 'edge:hover',
        style: {
          'line-color': '#546E7A',
          'target-arrow-color': '#546E7A',
        },
      },
    ],
    layout: {
      name: 'grid',
      rows: 3,
      cols: 4,
      padding: 10,
      fit: true,
    },
    userZoomingEnabled: true,
    userPanningEnabled: true,
  });

  cy.on('tap', 'node', function(evt) {
    const node = evt.target;
    modalTitle.textContent = node.data('label');
    modalContent.textContent = node.data('description');
    modal.showModal();
  });

  cy.fit();

  const debounce = (callback, interval = 0) => {
    let prevTimeoutId;

    return (...args) => {
      prevTimeoutId = setTimeout(() => {
        callback(args);
      }, interval);
    }
  }

  window.addEventListener('resize', debounce(cy.fit.bind(cy), 100));
}

fetchData().then(createGraph);