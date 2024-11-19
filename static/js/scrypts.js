document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let confirmAction = confirm("Вы уверены, что хотите создать эту задачу?");
            if (!confirmAction) {
                event.preventDefault();
            }
        });
    });
});

$(document).ready(function() {
    // Анимация при наведении на строки таблицы
    $(".table tbody tr").hover(
        function() {
            $(this).css("background-color", "#ffe0e0");
        },
        function() {
            $(this).css("background-color", "");
        }
    );

    // Подтверждение перед переходом на другие страницы
    $("a.btn-primary").click(function(e) {
        if (!confirm("Вы уверены, что хотите перейти?")) {
            e.preventDefault();
        }
    });

    // Добавление всплывающих подсказок к кнопкам
    $('[data-toggle="tooltip"]').tooltip();
});
