// Run whenever the user scroll the page
window.onscroll = function() {
    var backToTopButton = document.getElementById("back-to-top");

    /*
    If the document's body (or root element) has been scrolled more than 20 pixels,
    the button is displayed.
    */
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) 
    {
        backToTopButton.style.display = "block";
    } 
    else 
    {
        // if there are within 20 pixels from the top, the button is hidden again
        backToTopButton.style.display = "none";
    }
};

// Smoothly scroll the page to the top
function scrollToTop() 
{
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
