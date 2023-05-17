ymaps.ready(init);

function init() {

    var companyCoordinates = [64.535434, 40.434839]; // [������, �������]


    var map = new ymaps.Map("map", {
        center: companyCoordinates,
        zoom: 18
    });

    var marker = new ymaps.Placemark(companyCoordinates, {
        hintContent: '������ ������������� ����������',
        balloonContent: '��. �������, �. �����������'
    });

    map.geoObjects.add(marker);
}
