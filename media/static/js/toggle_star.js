// 'ready' method ensure that the function runs only after the document is fully loaded and ready.
$(document).ready(function(){
    // Listener on the review list
    $('#review-list').on('click', '#star-img', function(){
        /*
        Retrieve the profile id from the button 'profile-id' attribute. 
        $(this) refers to the image object.
        .data('profile-id') get the data of 'data-profile-id' attribute.
        */
        var $this = $(this);
        const reviewId = $this.data('review-id');
        const star_fill = $this.data('starfill-url');
        const star = $this.data('star-url');
        const csrftoken = csrfToken;

        $.ajax({
            type: 'POST',
            url: `/review/toggle_star/${reviewId}/`,
            headers: {
                'X-CSRFToken': csrftoken  // Set CSRF token in request headers
            },
            data: {},
            success: function(response) {
                if (response.starred) 
                {
                    $this.attr('src', star_fill);
                } 
                else 
                {
                    $this.attr('src', star);
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