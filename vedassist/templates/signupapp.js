const togglePassword = document.querySelectorAll('#togglePassword');
const password = document.querySelectorAll('#password');

function togglePasswordVisibility() {
    for (let pass of password) {
        // toggle the type attribute
        const type = pass.getAttribute('type') === 'password' ? 'text' : 'password';
        pass.setAttribute('type', type);
        // toggle the eye slash icon
        this.classList.toggle('fa-eye-slash');
    }
}
for (let toggle of togglePassword) {
    toggle.addEventListener('click', togglePasswordVisibility)
}


