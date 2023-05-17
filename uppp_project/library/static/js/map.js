ymaps.ready(init);

function init() {

    var companyCoordinates = [64.535434, 40.434839]; // [широта, долгота]


    var map = new ymaps.Map("map", {
        center: companyCoordinates,
        zoom: 18
    });

    var marker = new ymaps.Placemark(companyCoordinates, {
        hintContent: 'Вторая Кегостровская Библиотека',
        balloonContent: 'Ул. Пушкина, Д. Колотушкина'
    });

    map.geoObjects.add(marker);
}
