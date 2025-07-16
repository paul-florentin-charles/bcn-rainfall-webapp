/** Plotly main configuration **/

const default_plotly_config = {
    displaylogo: false,
    modeBarButtonsToRemove: ['select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d'],
    responsive: true,
    scrollZoom: false,
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

/* Switch between light mode and dark mode */
const themeSwitch = document.getElementById('theme-switch');

function setTheme(light) {
    if (light) {
        document.body.classList.add('light-mode');
    } else {
        document.body.classList.remove('light-mode');
    }
}

// Load theme from localStorage
const storedTheme = localStorage.getItem('theme');
if (storedTheme === 'light') {
    setTheme(true);
} else if (storedTheme === 'dark') {
    setTheme(false);
}

if (themeSwitch) {
    themeSwitch.addEventListener('click', () => {
        const isLight = !document.body.classList.contains('light-mode');
        setTheme(isLight);
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
    });
}