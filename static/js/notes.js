(function () {
    var list = document.getElementById('notes-list');
    var empty = document.getElementById('notes-empty');
    if (!list) {
        return;
    }

    function showEmptyIfNeeded() {
        if (list.querySelectorAll('.list-group-item').length === 0) {
            list.classList.add('d-none');
            if (empty) {
                empty.classList.remove('d-none');
            }
        }
    }

    list.addEventListener('submit', function (event) {
        var form = event.target.closest('.js-note-delete');
        if (!form) {
            return;
        }
        event.preventDefault();

        if (!window.confirm('Удалить заметку?')) {
            return;
        }

        var button = form.querySelector('button[type="submit"]');
        if (button) {
            button.disabled = true;
        }

        fetch(form.action, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: new FormData(form),
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Request failed');
                }
                return response.json();
            })
            .then(function () {
                var item = document.getElementById('note-' + form.dataset.noteId);
                if (item) {
                    item.remove();
                }
                showEmptyIfNeeded();
            })
            .catch(function () {
                if (button) {
                    button.disabled = false;
                }
                form.submit();
            });
    });
})();
