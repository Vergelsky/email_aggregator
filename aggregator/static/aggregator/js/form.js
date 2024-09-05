$(document).ready(function() {
    $('#accountForm').on('submit', function (event) {
        event.preventDefault();

        const username = $('#username').val();
        const provider = $('#provider').val();
        const password = $('#password').val();

        $.ajax({
            url: '/accounts/',
            method: 'POST',
            data: { username: username, provider: provider, password: password },
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                $('#accountFormContent').hide();
                $('#successMessage').removeClass('hidden');
            },
            error: function (error) {
                alert('Ошибка загрузки данных')
            }
        });
    });

    $('#addAnother').on('click', function () {
        $('#successMessage').addClass('hidden');
        $('#accountFormContent').show();
        $('#username').val('');
        $('#password').val('');
    });

    $('#goToMessages').on('click', function () {
        window.location.href = '/';
    });
});