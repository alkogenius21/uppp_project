document.addEventListener('DOMContentLoaded', function () {
    const images = document.querySelectorAll('.images img');
    let currentIndex = 0;

    function fadeOut(element) {
        if (element) {
            element.style.opacity = '0';
        }
    }

    function fadeIn(element) {
        if (element) {
            element.style.opacity = '1';
        }
    }

    function animateImages() {
        const previousIndex = currentIndex === 0 ? images.length - 1 : currentIndex - 1;

        fadeOut(images[previousIndex]);
        fadeIn(images[currentIndex]);

        currentIndex++;
        if (currentIndex >= images.length) {
            currentIndex = 0;
        }
    }

    let animationInterval = setInterval(animateImages, 3000);

    // Останавливаем анимацию при наведении на изображения
    images.forEach(image => {
        image.addEventListener('mouseover', () => {
            clearInterval(animationInterval);
        });

        image.addEventListener('mouseout', () => {
            animationInterval = setInterval(animateImages, 3000);
        });
    });
});