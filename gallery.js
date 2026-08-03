document.querySelectorAll('[data-flashcard-gallery]').forEach((gallery) => {
    const cards = Array.from(gallery.querySelectorAll('figure'));
    const previousButton = gallery.querySelector('[data-gallery-previous]');
    const nextButton = gallery.querySelector('[data-gallery-next]');
    const status = gallery.querySelector('[data-gallery-status]');
    let currentIndex = 0;
    let touchStartX = 0;

    const showCard = (index) => {
        currentIndex = (index + cards.length) % cards.length;
        cards.forEach((card, cardIndex) => {
            const isActive = cardIndex === currentIndex;
            card.classList.toggle('is-active', isActive);
            card.setAttribute('aria-hidden', String(!isActive));
        });
        status.textContent = `${currentIndex + 1} of ${cards.length}`;
    };

    previousButton.addEventListener('click', () => showCard(currentIndex - 1));
    nextButton.addEventListener('click', () => showCard(currentIndex + 1));

    gallery.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowLeft') showCard(currentIndex - 1);
        if (event.key === 'ArrowRight') showCard(currentIndex + 1);
    });

    gallery.addEventListener('touchstart', (event) => {
        touchStartX = event.changedTouches[0].clientX;
    }, { passive: true });

    gallery.addEventListener('touchend', (event) => {
        const distance = event.changedTouches[0].clientX - touchStartX;
        if (Math.abs(distance) < 45) return;
        showCard(currentIndex + (distance < 0 ? 1 : -1));
    }, { passive: true });

    gallery.tabIndex = 0;
    showCard(0);
});
