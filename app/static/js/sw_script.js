document.getElementById('nameForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const department = document.getElementById('department');
    const departmentText = department.options[department.selectedIndex].text;
    const hireDate = document.getElementById('hireDate').value;
    const terminationDate = document.getElementById('terminationDate').value;

    let message = 'Привет, ' + name +
        '\nАдрес: ' + address +
        '\nТелефон: ' + phone +
        '\nДепартамент: ' + departmentText +
        '\nДата принятия: ' + hireDate;

    if (terminationDate) {
        message += '\nДата увольнения: ' + terminationDate;
    }

    alert(message);
});