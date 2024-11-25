document.addEventListener('DOMContentLoaded', function() {
    const departmentCards = document.querySelectorAll('.department-card');

    departmentCards.forEach(card => {
        card.addEventListener('click', function() {
            const employeeList = this.querySelector('.employee-list');
            employeeList.style.display = employeeList.style.display === 'none' ? 'block' : 'none';
        });
    });
});