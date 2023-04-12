function showMap() {
	var geocoder = new google.maps.Geocoder();
	var address = document.getElementById('address').value;

	geocoder.geocode({ 'address': address }, function (results, status) {
		if (status == 'OK') {
			var map = new google.maps.Map(document.getElementById('map'), {
				zoom: 15,
				center: results[0].geometry.location
			});

			var marker = new google.maps.Marker({
				map: map,
				position: results[0].geometry.location
			});

		} else {
			alert('Geocode was not successful for the following reason: ' + status);
		}
	});
}
