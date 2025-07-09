/** Plotly main configuration **/

const config = {
    responsive: true,
    scrollZoom: true,
    displayLogo: false
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

const hamburger = document.getElementById('hamburger-menu');
const menu = document.getElementById('main-menu');

hamburger.addEventListener('click', function () {
    const expanded = hamburger.getAttribute('aria-expanded') === 'true';
    hamburger.setAttribute('aria-expanded', (!expanded).toString());
    menu.classList.toggle('open');
});

// Close menu when clicking outside
document.addEventListener('click', function (e) {
    if (!hamburger.contains(e.target) && !menu.contains(e.target) && menu.classList.contains('open')) {
        hamburger.setAttribute('aria-expanded', 'false');
        menu.classList.remove('open');
    }
});