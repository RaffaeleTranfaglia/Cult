$(document).ready(function() 
{
    /*
     displays the modal form when log button is clicked
    $('#log-btn').click(function() {
        $('#logModal').modal('show');
    });

    $('#logForm').on('submit', function(event) {
        
        Stop default behavior of the form (send a request to the server and reload the page) 
        in order to handle it with AJAX instead. Allowing for a smoother user experience without a 
        full page reload.
        
        event.preventDefault();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            #TODO check that the url is the correct one
            url: form.attr('action'),
            data: form.serialize(),
            dataType: 'json',
            success: function(response) {
                if (response.status === "success") 
                {
                    $('#logModal').modal('hide');
                    window.location.href = `${window.location.href}?log=success`;
                }
                else
                {
                    alert('An error occurred.');
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
                    alert('An error occurred.');
                }
            }
        });
    });
    */

    // Display a success message if the URL contains log='success' parameter
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('log') && urlParams.get('log') === 'success') {
        $('.alert-success').show();
    } else {
        $('.alert-success').hide();
    }
});