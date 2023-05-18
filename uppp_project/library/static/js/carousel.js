document.addEventListener('DOMContentLoaded', function () {
    const previousButtons = document.querySelectorAll('.carousel-button.previous');
    const nextButtons = document.querySelectorAll('.carousel-button.next');

    previousButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const carousel = button.parentElement.querySelector('.carousel');
            const activeItem = carousel.querySelector('.carousel-item.active');

            if (activeItem.previousElementSibling) {
                activeItem.classList.remove('active');
                activeItem.previousElementSibling.classList.add('active');
            } else {
                const lastItem = carousel.lastElementChild;
                activeItem.classList.remove('active');
                lastItem.classList.add('active');
            }

            carousel.classList.add('slide-right');
            setTimeout(function () {
                carousel.classList.remove('slide-right');
            }, 400);
        });
    });

    nextButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            const carousel = button.parentElement.querySelector('.carousel');
            const activeItem = carousel.querySelector('.carousel-item.active');

            if (activeItem.nextElementSibling) {
                activeItem.classList.remove('active');
                activeItem.nextElementSibling.classList.add('active');
            } else {
                const firstItem = carousel.firstElementChild;
                activeItem.classList.remove('active');
                firstItem.classList.add('active');
            }

            carousel.classList.add('slide-left');
            setTimeout(function () {
                carousel.classList.remove('slide-left');
            }, 400); 
        });
    });
});


