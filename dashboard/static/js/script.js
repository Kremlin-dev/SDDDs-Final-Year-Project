document.addEventListener('DOMContentLoaded', () => {
    const rowsPerPage = 3;
    let currentPage = 1;
    let userData = [];

    function fetchData() {
        fetch('/api/data')  
            .then(response => response.json())
            .then(data => {
                userData = data;
                displayTableData();
                paginateTable();
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function displayTableData() {
        const tableBody = document.getElementById('userTable');
        tableBody.innerHTML = '';
    
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const paginatedData = userData.slice(start, end);
    
        for (const user of paginatedData) {
            const row = tableBody.insertRow();
            row.insertCell(0).textContent = user.car_id;
            row.insertCell(1).textContent = user.contact; // Update to user.contact
            row.insertCell(2).textContent = user.drowsiness_state;
            row.insertCell(3).textContent = user.time_detected;
            row.insertCell(4).textContent = user.drowsiness_duration_minutes; // Update to user.drowsiness_duration_minutes
            row.insertCell(5).textContent = user.uptime_minutes; // Update to user.uptime_minutes
    
            const actionCell = row.insertCell(6);
            const viewButton = document.createElement('button');
            viewButton.textContent = 'View';
            viewButton.className = 'btn btn-primary';
            viewButton.addEventListener('click', () => showUserInfo(user));
            actionCell.appendChild(viewButton);
        }
    }
    

    function filterTable() {
        const filterCardID = document.getElementById('filterCardID').value.toUpperCase();
        const filterDriverContact = document.getElementById('filterDriverContact').value.toUpperCase();

        userData = userData.filter(user => 
            user.car_id.toUpperCase().includes(filterCardID) &&
            user.driver_contact.toUpperCase().includes(filterDriverContact)
        );

        currentPage = 1;
        displayTableData();
        paginateTable();
    }

    function paginateTable() {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';

        const totalPages = Math.ceil(userData.length / rowsPerPage);

        for (let i = 1; i <= totalPages; i++) {
            let li = document.createElement('li');
            li.classList.add('page-item');
            if (i === currentPage) li.classList.add('active');

            let a = document.createElement('a');
            a.classList.add('page-link');
            a.textContent = i;
            a.setAttribute('href', '#');
            a.addEventListener('click', function (e) {
                e.preventDefault();
                currentPage = i;
                displayTableData();
                paginateTable();
            });

            li.appendChild(a);
            pagination.appendChild(li);
        }
    }

    function showUserInfo(user) {
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <p>Car ID: ${user.car_id}</p>
            <p>Driver Contact: ${user.contact}</p>
            <p>Drowsiness State: ${user.drowsiness_state}</p>
            <p>Time Detected: ${user.time_detected}</p>
            <p>Duration of Drowsiness (min): ${user.drowsiness_duration_minutes}</p>
            <p>Device Uptime (min): ${user.uptime_minutes}</p>
        `;
        $('#userInfoModal').modal('show');
    }

    function printTable() {
        const divToPrint = document.getElementById('userTable');
        const newWin = window.open('');
        newWin.document.write('<html><head><title>Print</title>');
        newWin.document.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">');
        newWin.document.write('</head><body>');
        newWin.document.write('<table class="table table-bordered">');
        newWin.document.write(divToPrint.innerHTML);
        newWin.document.write('</table></body></html>');
        newWin.document.close();
        newWin.print();
    }

    document.getElementById('filterCardID').addEventListener('input', filterTable);
    document.getElementById('filterDriverContact').addEventListener('input', filterTable);
    document.querySelector('.btn.btn-primary').addEventListener('click', printTable);

    fetchData();
});
