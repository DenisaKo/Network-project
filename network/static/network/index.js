document.addEventListener("DOMContentLoaded", function() {

    const exampleModal = document.getElementById('exampleModal')
    exampleModal.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        
        // Extract info from data-bs-* attributes
        const post_id = parseInt(button.getAttribute('data-bs-whatever'))
        // console.log(post_id);
        document.querySelector('#edit').addEventListener('submit', (e) => {
            e.preventDefault();
            const text_area = document.getElementById('exampleModal').querySelector('#message-text').value;
            // console.log(text_area);
            edit_post(post_id, text_area)
        });
    });
});


function edit_post(post_id, body_text) {

    fetch(`/posts/${post_id}/`, {
        method: 'POST',
        body: JSON.stringify({
            body_text: body_text
        })
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data)
        const body = document.getElementById(`body${post_id}`)
        // console.log(body);
        const new_body_text = document.createElement('div')
        new_body_text.append(data.edited_post_body)
        body.replaceChildren(new_body_text)
        // console.log(body)
    })
};








