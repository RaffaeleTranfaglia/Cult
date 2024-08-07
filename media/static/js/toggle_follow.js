// 'ready' method ensure that the function runs only after the document is fully loaded and ready.
$(document).ready(function(){
    // Listener on the button with id '#follow-btn'
    $('#follow-btn').click(function(){
        /*
        Retrieve the profile id from the button 'profile-id' attribute. 
        $(this) refers to the button object.
        .data('profile-id') get the data of 'data-profile-id' attribute.
        */
        const profileId = $(this).data('profile-id');
        const csrftoken = csrfToken;

        $.ajax({
            type: 'POST',
            url: `/profile/toggle_follow/${profileId}/`,
            headers: {
                'X-CSRFToken': csrftoken  // Set CSRF token in request headers
            },
            data: {},
            success: function(response) {
                if (response.is_following) {
                    $('#follow-btn').text('Unfollow');
                } else {
                    $('#follow-btn').text('Follow');
                }
            },
            error: function(xhr, status, error) {
                console.log("AJAX error:", xhr, status, error);
                if (xhr.status === 403) {
                    // Parse the redirect URL from the response
                    const redirectUrl = xhr.responseJSON.login_url || '/login/';
                    // Redirect to login page
                    window.location.href = redirectUrl + '?next=' + encodeURIComponent(window.location.pathname);
                } else {
                    alert(xhr['responseJSON']['error']);
                }
            }
        });
    });
});

// Function to get CSRF token from cookie
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