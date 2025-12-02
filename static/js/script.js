// Custom JavaScript can go here
document.addEventListener('DOMContentLoaded', function () {
    // Example: Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
