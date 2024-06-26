// 'ready' method ensure that the function runs only after the document is fully loaded and ready.
$(document).ready(function(){
    // Listener on the button with id '#watchlist-btn'
    $('#watchlist-btn').click(function(){
        /*
        Retrieve the movie pk from the button 'movie-pk' attribute. 
        $(this) refers to the button object.
        .data('movie-pk') get the data of 'data-movie-pk' attribute.
        */
        const movieId = $(this).data('movie-pk');
        const csrftoken = csrfToken;

        $.ajax({
            type: 'POST',
            url: `/movie/toggle_watchlist/${movieId}/`,
            headers: {
                'X-CSRFToken': csrftoken  // Set CSRF token in request headers
            },
            data: {},
            success: function(response) {
                if (response.in_watchlist) {
                    $('#watchlist-btn').text('Remove from Watchlist');
                } else {
                    $('#watchlist-btn').text('Add to Watchlist');
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