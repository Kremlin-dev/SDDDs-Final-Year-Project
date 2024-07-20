document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const notificationSound = document.getElementById('notification-sound');

    socket.on('new_data', (data) => {
        showNotification('New data has been added');
        fetchData();
    });

    function showNotification(message) {
        const notificationContainer = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = 'alert alert-info';
        notification.textContent = message;

        notificationContainer.appendChild(notification);
        notificationSound.play();

        setTimeout(() => {
            notificationContainer.removeChild(notification);
        }, 10000);
    }

    const rowsPerPage = 5;
    let currentPage = 1;
    let userData = [];

    async function fetchData() {
        try {
            const response = await fetch('/api/data');
            userData = await response.json();
            displayTableData();
            paginateTable();
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    function displayTableData() {
        const tableBody = document.getElementById('userTable');
        tableBody.innerHTML = '';

        const startIdx = (currentPage - 1) * rowsPerPage;
        const endIdx = Math.min(startIdx + rowsPerPage, userData.length);

        for (let i = startIdx; i < endIdx; i++) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${userData[i].car_id}</td>
                <td>${userData[i].contact}</td>
                <td>${userData[i].drowsiness_state}</td>
                <td>${userData[i].time_detected}</td>
                <td>${userData[i].drowsiness_duration_minutes}</td>
                <td>${userData[i].uptime_minutes}</td>
                <td><button class="btn btn-primary btn-sm" onclick="viewUserDetails(${i})">View</button></td>
            `;
            tableBody.appendChild(row);
        }
    }

    function paginateTable() {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';

        const totalPages = Math.ceil(userData.length / rowsPerPage);

        for (let i = 1; i <= totalPages; i++) {
            const pageItem = document.createElement('li');
            pageItem.className = 'page-item';
            pageItem.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${i})">${i}</a>`;
            pagination.appendChild(pageItem);
        }
    }

    window.goToPage = (page) => {
        currentPage = page;
        displayTableData();
    };

    window.viewUserDetails = (index) => {
        const user = userData[index];
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <p><strong>Car ID:</strong> ${user.car_id}</p>
            <p><strong>Driver Contact:</strong> ${user.contact}</p>
            <p><strong>Drowsiness State:</strong> ${user.drowsiness_state}</p>
            <p><strong>Time Detected:</strong> ${user.time_detected}</p>
            <p><strong>Duration of Drowsiness (min):</strong> ${user.drowsiness_duration_minutes}</p>
            <p><strong>Device Uptime (min):</strong> ${user.uptime_minutes}</p>
        `;
        $('#userInfoModal').modal('show');
    };

    window.filterTable = () => {
        const filterCardID = document.getElementById('filterCardID').value.toLowerCase();
        const filterDriverContact = document.getElementById('filterDriverContact').value.toLowerCase();

        userData = userData.filter(user => 
            user.car_id.toLowerCase().includes(filterCardID) &&
            user.contact.toLowerCase().includes(filterDriverContact)
        );

        displayTableData();
        paginateTable();
    };

    window.printTable = () => {
        window.print();
    };

    fetchData();
});
