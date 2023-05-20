(function () {
    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
})();

var players = [];
var currentSlide = 0;
var isPlayingVideo = false;

function onYouTubeIframeAPIReady() {
    players[0] = new YT.Player('youtube-player1', {
        height: '400',
        width: '730',
        videoId: 'T4Px70rNaq0',
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        },
        playerVars: {
            autoplay: 0
        }
    });

    players[1] = new YT.Player('youtube-player2', {
        height: '400',
        width: '730',
        videoId: 'B7JJmM7IQH0',
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        },
        playerVars: {
            autoplay: 0
        }
    });

    players[2] = new YT.Player('youtube-player3', {
        height: '400',
        width: '730',
        videoId: '48NmJz8XV44',
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        },
        playerVars: {
            autoplay: 0
        }
    });
}

function onPlayerReady(event) {
    event.target.playVideo();
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.PLAYING) {
        isPlayingVideo = true;
        $('#video-carousel').carousel('pause');
    } else if (event.data === YT.PlayerState.ENDED || event.data === YT.PlayerState.PAUSED || event.data === YT.PlayerState.CUED) {
        isPlayingVideo = false;
        $('#video-carousel').carousel('cycle');
    }
}

$(document).ready(function () {
    $('#video-carousel').on('slide.bs.carousel', function (e) {
        if (isPlayingVideo) {
            players[currentSlide].pauseVideo();
        }
    });

    $('.carousel-control-prev').click(function () {
        if (isPlayingVideo) {
            players[currentSlide].pauseVideo();
        }
    });

    $('.carousel-control-next').click(function () {
        if (isPlayingVideo) {
            players[currentSlide].pauseVideo();
        }
    });
});