<script>
    let checkedMessages = 0;
    let totalMessages = 20;
    let remainingMessages = totalMessages;

    function updateInitialStatus() {
        $('#checkedMessagesCount').text(checkedMessages);
    }

    function showLoadingSection() {
        $('#initialStatus').addClass('d-none');
        $('#loadingSection').removeClass('d-none');
    }

    function updateProgressBar() {
        const progressPercentage = Math.min((remainingMessages / totalMessages) * 100, 100);
        $('#progressBar').css('width', progressPercentage + '%').attr('aria-valuenow', progressPercentage).text(`${remainingMessages} из ${totalMessages}`);
    }

    function addMessageRow(message) {
        const row = `<tr>
            <td>${message.id}</td>
            <td>${message.sender}</td>
            <td>${message.subject}</td>
            <td>${message.text.slice(0, 50)}...</td>
            <td>${message.date}</td>
        </tr>`;
        $('#messagesTable').append(row);
    }

    // Получение писем
    function MessageCheck() {
        if (checkedMessages < totalMessages) {
            checkedMessages++;
            updateInitialStatus();

            setTimeout(MessageCheck, 200); // Задержка между проверками
        } else {
            // Переключаемся на загрузку новых писем
            showLoadingSection();
            startLoadingMessages();
        }
    }

    function startLoadingMessages() {
        if (remainingMessages > 0) {
            remainingMessages--;
            updateProgressBar();

            // Имитация добавления нового сообщения
            const message = {
                id: totalMessages - remainingMessages,
                sender: 'example@mail.com',
                subject: 'Тестовое сообщение',
                text: 'Текст этого письма достаточно длинный, но мы выводим только краткий фрагмент.',
                date: new Date().toLocaleString(),
            };
            addMessageRow(message);

            setTimeout(startLoadingMessages, 200); // Задержка между загрузками
        } else {
            // Когда все письма загружены
            $('#progressBar').css('width', '100%').text('Загрузка завершена');
        }
    }

    $(document).ready(function () {
        MessageCheck();  // Начинаем процесс проверки писем
    });
</script>