(function () {
    var tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
})();

var players = [];

function onYouTubeIframeAPIReady() {
    players[0] = new YT.Player('youtube-player1', {
        height: '400',
        width: '730',
        videoId: 'T4Px70rNaq0',
        
        playerVars: {
            autoplay: 0,
            mute: 1
        }
    });

    players[1] = new YT.Player('youtube-player2', {
        height: '400',
        width: '730',
        videoId: 'B7JJmM7IQH0',
        
        playerVars: {
            autoplay: 0,
            mute: 1
        }
    });

    players[2] = new YT.Player('youtube-player3', {
        height: '400',
        width: '730',
        videoId: '48NmJz8XV44',
        
        playerVars: {
            autoplay: 0,
            mute: 1
        }
    });
}