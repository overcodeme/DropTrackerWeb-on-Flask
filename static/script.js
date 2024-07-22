document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('projectForm');
    form.addEventListener('submit', function(event) {
        let valid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            if (!input.value) {
                input.classList.add('is-invalid');
                valid = false;
            } else {
                input.classList.remove('is-invalid');
            }
        });
        if (!valid) {
            event.preventDefault();
            alert('Пожалуйста, заполните все обязательные поля.');
        }
    });
});