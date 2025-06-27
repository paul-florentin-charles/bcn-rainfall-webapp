/** Plotly main configuration **/

const config: Partial<Plotly.Config> = {
    responsive: true,
    scrollZoom: true,
};

/** Document style **/

const style: CSSStyleDeclaration = window.getComputedStyle(document.body)


/** Scroll to top button **/

const scrollToTopBtn = document.getElementById('scrollToTop') as HTMLElement;

const toggleScrollToTopButton = (): void => {
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

const hamburger = document.getElementById('hamburger-menu') as HTMLElement;
const menu = document.getElementById('main-menu') as HTMLElement;

hamburger.addEventListener('click', function () {
    const expanded = hamburger.getAttribute('aria-expanded') === 'true';
    hamburger.setAttribute('aria-expanded', (!expanded).toString());
    menu.classList.toggle('open');
});

// Close menu when clicking outside
document.addEventListener('click', function (e: MouseEvent) {
    const target = e.target as Node;
    if (!hamburger.contains(target) && !menu.contains(target) && menu.classList.contains('open')) {
        hamburger.setAttribute('aria-expanded', 'false');
        menu.classList.remove('open');
    }
});