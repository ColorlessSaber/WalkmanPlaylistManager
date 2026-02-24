from src.functions import extract_songs_from_playlist
from pyfakefs.fake_filesystem_unittest import TestCase

class TestExtractSongsFromPlaylist(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs.create_file('/bar/playlist.M3U8', contents="#EXTM3U\n#EXTINF:,\nbob/V/01 - epic song.flac\n#EXTINF:,\nSega/Sonic Songs/02 - sonic theme song.mp3\n#EXTINF:,\nLarry Luu/Great Hits/super super!.m4a\n")

    def test_extract_songs_from_playlist(self):
        songs_in_playlist = (
            ('bob', 'V', '01 - epic song.flac'),
            ('Sega', 'Sonic Songs', '02 - sonic theme song.mp3'),
            ('Larry Luu', 'Great Hits', 'super super!.m4a')
        )
        playlist_name = 'playlist'

        songs_found = extract_songs_from_playlist(playlist_name, '/bar')

        assert songs_found == songs_in_playlist, print(songs_found, songs_in_playlist)