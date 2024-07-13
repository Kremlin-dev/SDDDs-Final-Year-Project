let currentPage = 1;
const rowsPerPage = 10;
document.addEventListener('DOMContentLoaded', () => {
    fetchData();
    setInterval(fetchData, 10000); 

function fetchData() {
    fetch('/api/data') 
        .then(response => response.json())
        .then(data => {
            updateTable(data);
            setupPagination(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateTable(data) {
    const table = document.getElementById('userTable');
    table.innerHTML = ''; 

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const paginatedData = data.slice(start, end);

    paginatedData.forEach(row => {
        const newRow = table.insertRow();
        newRow.insertCell(0).innerHTML = row.card_id;
        newRow.insertCell(1).innerHTML = row.confidence;
        newRow.insertCell(2).innerHTML = row.location;
        newRow.insertCell(3).innerHTML = row.time_moved;
        newRow.insertCell(4).innerHTML = row.drowsiness_state;
        newRow.insertCell(5).innerHTML = row.contact;
        newRow.insertCell(6).innerHTML = '<button class="btn btn-success" onclick="viewUser(\'' + row.card_id + '\')">View</button> <button class="btn btn-secondary" onclick="printRow(this)">Print</button>';
    });
}

function setupPagination(data) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; 

    const pageCount = Math.ceil(data.length / rowsPerPage);

    for (let i = 1; i <= pageCount; i++) {
        const pageItem = document.createElement('li');
        pageItem.classList.add('page-item');
        if (i === currentPage) {
            pageItem.classList.add('active');
        }

        const pageLink = document.createElement('a');
        pageLink.classList.add('page-link');
        pageLink.href = '#';
        pageLink.innerHTML = i;
        pageLink.addEventListener('click', (e) => {
            e.preventDefault();
            currentPage = i;
            updateTable(data);
            setupPagination(data);
        });

        pageItem.appendChild(pageLink);
        pagination.appendChild(pageItem);
    }
}

function filterTable() {
    const filterCardID = document.getElementById('filterCardID').value.toLowerCase();
    const filterConfidence = document.getElementById('filterConfidence').value.toLowerCase();

    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const filteredData = data.filter(row => {
                const cardIDMatch = row.card_id.toLowerCase().includes(filterCardID);
                const confidenceMatch = row.confidence.toLowerCase().includes(filterConfidence);
                return cardIDMatch && confidenceMatch;
            });
            updateTable(filteredData);
            setupPagination(filteredData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function viewUser(card_id) {
    fetch(`/api/car/${card_id}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const modalBody = document.getElementById('modalBody');
                modalBody.innerHTML = `
                    <p><strong>Type:</strong> ${data.type}</p>
                    <p><strong>Driver:</strong> ${data.driver}</p>
                    <p><strong>Year:</strong> ${data.year}</p>
                `;
                $('#userInfoModal').modal('show');
            }
        })
        .catch(error => console.error('Error fetching car information:', error));
}

function printRow(button) {
    const row = button.parentNode.parentNode;
    const rowData = [];
    for (let i = 0; i < row.cells.length - 1; i++) {
        rowData.push(row.cells[i].innerText);
    }
    const printWindow = window.open('', '', 'height=400,width=600');
    printWindow.document.write('<html><head><title>Print Data</title></head><body><pre>' + rowData.join('\n') + '</pre></body></html>');
    printWindow.document.close();
    printWindow.print();
}
