/** Plotly main configuration **/

const config = {
    responsive: true,
    scrollZoom: true,
};

/** Document style **/

const style = window.getComputedStyle(document.body)


/** Scroll to top button **/

const scrollToTopBtn = document.getElementById('scrollToTop');

const toggleScrollToTopButton = () => {
    if (window.scrollY > 250) {
        scrollToTopBtn.classList.add('visible');
    } else {
        scrollToTopBtn.classList.remove('visible');
    }
};

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

window.addEventListener('scroll', toggleScrollToTopButton);

/** Toggle hamburger menu for tablets & phones **/