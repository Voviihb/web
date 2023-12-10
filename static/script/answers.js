function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const answer_items = document.getElementsByClassName('like-section-answers')

for (let item of answer_items) {
    const [counter, button] = item.children;
    const btn = button.children[0].children[0];
    const cnt = counter.children[0];
    btn.addEventListener('click', () => {
        const formData = new FormData();
        formData.append('answer_id', btn.dataset.id);
        const request = new Request('/like_answer', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                cnt.innerHTML = data.count;
            })

    })
}



const checkbox_items = document.getElementsByClassName('form-check-input');

for (let checkbox of checkbox_items) {
    checkbox.addEventListener('change', () => {
        const formData = new FormData();
        formData.append('answer_id', checkbox.dataset.ansid);
        formData.append('question_id', checkbox.dataset.queid);

        const request = new Request('/correct_answer', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                checkbox.checked = data.correct;
            });
    });
}