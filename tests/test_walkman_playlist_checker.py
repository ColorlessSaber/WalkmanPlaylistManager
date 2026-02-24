from src.functions.walkman_playlist_checker import walkman_playlist_checker

class TestWalkmanPlaylistChecker:

    def test_detects_playlist(self):
        file = 'playlist.M3U8'
        assert walkman_playlist_checker(file) == True

    def test_detects_no_playlist(self):
        file = 'playlist.txt'
        assert walkman_playlist_checker(file) == False