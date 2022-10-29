document.addEventListener("DOMContentLoaded", function() {
  
    const current_user_id = parseInt(document.getElementById('container_posts').dataset.person);
    document.getElementById('following_nav').addEventListener('click', () => load_all_posts_following(current_user_id, 1));

    const forms = document.querySelectorAll('.form_add_like')
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
                e.preventDefault();  
                // console.log('hi');
                const post_id = parseInt(form.getAttribute("id"));
                // console.log(post_id);
                edi(current_user_id, post_id);
            })   
    });

    comments();
});
    
    
function edi(current_user_id, post_id) {
    // console.log(post_id)
    fetch(`/posts/${post_id}/`, {
        method: 'POST',
        body: JSON.stringify({
            add_like: current_user_id
        })
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data)
        const count = document.getElementById(`count${post_id}`)
        
        const new_value = document.createElement('div')
        new_value.append(data.all_likes)
        count.replaceChildren(new_value)
        // console.log(count)
    })
};

function comments() {

    const all_comments_name = document.querySelectorAll('.comments_name');
    all_comments_name.forEach(comment_name => {
        comment_name.addEventListener('click', (event) => {
            event.preventDefault();
            post_id = parseInt(comment_name.getAttribute('data-post_id'));
            const comments_all = document.getElementById(`comments_section${post_id}`);
            const status = comments_all.style.display

            if (status === "none" || !status) {
                comments_all.style.display = "block";
            }
            else {
                comments_all.style.display = "none";
            }
        
            const form_comment = document.getElementById(`new_comment${post_id}`);
            
            form_comment.addEventListener('submit', event => {
                event.preventDefault();
                const comment_body_textarea = document.getElementById(`new_comment_text${post_id}`).value;
                // console.log(comment_body_textarea);
                add_comment(post_id, comment_body_textarea);
            });
        });
    });
};


function add_comment(post_id, comment_body) {
    // console.log(post_id);
    // console.log(comment_body);
    fetch(`/comments/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            comment_body: comment_body
        })
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data)
        const new_card = document.createElement('div');
        new_card.className = 'card comment_card shadow comments';

        const new_header = document.createElement('div');
        new_header.className = 'card-header';

        const new_name = document.createElement('div');

        const name_link = document.createElement('a');
        name_link.setAttribute('href', `/users/${data.comment.sender}/profil`)
        name_link.append(data.comment.sender_name)
        new_name.append(name_link);

        const new_time = document.createElement('div');
        const small_new_time = document.createElement('small');
        small_new_time.append(data.comment.timestamp);
        new_time.append(small_new_time);


        new_header.append(new_name);
        new_header.append(new_time);

        const new_card_body = document.createElement('div');
        new_card_body.className = "card-body";

        const new_body = document.createElement('div');
        new_body.append(data.comment.body_text);
        new_card_body.append(new_body);

        const br = document.createElement('br');

        new_card.append(new_header);
        new_card.append(new_card_body);
        
        const all_comments = document.getElementById(`comments_all${data.comment.post_id}`)
        all_comments.prepend(br);
        all_comments.prepend(new_card);

        document.getElementById(`new_comment_text${data.comment.post_id}`).value = "";
    });
};
