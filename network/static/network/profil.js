document.addEventListener("DOMContentLoaded", function() {
    
    // current log in user
    const current_user_id = parseInt(document.querySelector('#container_posts').dataset.person);
    // const current_user_username = document.querySelector('#user_container_posts').dataset.username;
    console.log("log in user is", {current_user_id});

    // whose profil it is
    const user = document.querySelector('.user_profile');
    const user_id = parseInt(user.getAttribute('id'));
    console.log("this profile belogs to user ",{user_id});

    document.getElementById('create_delete_follow').addEventListener('submit', (e) => {
        e.preventDefault();
        const button = document.getElementById('follow_button')
        const status = button.getAttribute('data-status')
        // console.log(status)
        following(user_id, status); 
    });

    edit_profile_window(current_user_id);
});


function following(user_id, status) {
    // console.log("this profile belogs to user ",{user_id});
    // console.log("log in user is", {current_user_id});

    fetch(`/users/${user_id}`, {
        method: 'POST',
        body: JSON.stringify({
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
            // console.log(data);
            const followers_count = document.getElementById('followers')
            const new_followers_count = document.createElement('div')
            new_followers_count.append(data.followers)
            followers_count.replaceChildren(new_followers_count)

            const follow_button_disp = document.getElementById('status_disp')
            const new_follow_button_disp = document.createElement('div')
            new_follow_button_disp.append(data.status.toUpperCase())
            follow_button_disp.replaceChildren(new_follow_button_disp)

            const follow_button= document.getElementById('follow_button')
            follow_button.setAttribute('data-status', data.status);
    }); 
};


function edit_profile_window(current_user_id) {
    const profileModal = document.getElementById('profileModal')
    profileModal.addEventListener('show.bs.modal', () => {

        const update_form = profileModal.querySelector('#edit_post_form')
        update_form.addEventListener('submit', (e) => {
            e.preventDefault();
            const image = document.getElementById('profileModal').querySelector('#image_url').value;
            const bio = document.getElementById('profileModal').querySelector('#bio-text').value;

            edit_profile(current_user_id, image, bio);
        });
    });
};


function edit_profile(current_user_id, image, bio) {

    fetch(`/users/${current_user_id}`, {
        method: 'POST',
        body: JSON.stringify({
            image: image,
            bio: bio
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const image_div = document.getElementById('user_image')
        const new_img = document.createElement('img')

        if (data.image === "") {
            new_img.setAttribute('src', `https://robohash.org/${current_user_id}?200x200`)
        } else {
            new_img.setAttribute('src', data.image) 
        }
        new_img.className = "img-fluid rounded-start rounded-circle"
        image_div.replaceChildren(new_img)
   
        const old_bio = document.getElementById('user_bio');
        const new_bio = document.createElement('p')
        // p.className = ''
        new_bio.append(data.bio);
        old_bio.replaceChildren(new_bio);
    });
};


