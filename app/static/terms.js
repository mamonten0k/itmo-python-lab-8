async function fetchTerms() {
  const response = await fetch('/api/terms/');
  const terms = await response.json();

  const tableBody = document.querySelector('#terms-table tbody');

  terms.forEach(term => {
    const row = document.createElement('tr');
    const nameCell = document.createElement('td');
    const descriptionCell = document.createElement('td');

    nameCell.textContent = term.name;
    descriptionCell.textContent = term.description;

    row.appendChild(nameCell);
    row.appendChild(descriptionCell);

    tableBody.appendChild(row);
  });
}

fetchTerms();