import os
from src.functions import generate_playlist
from pyfakefs.fake_filesystem_unittest import TestCase

class TestGeneratePlaylist(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir('/bar')

    def test_generates_playlist(self):
        list_of_songs = [
            ('bob', 'V', '01 - epic song.flac'),
            ('Sega', 'Sonic Songs', '02 - sonic theme song.mp3'),
            ('Larry Luu', 'Great Hits', 'super super!.m4a')
        ]
        name_of_playlist = 'my epic playlist'

        generate_playlist(list_of_songs, name_of_playlist, '/bar')

        assert (name_of_playlist + '.M3U8') in os.listdir('/bar')

        # read the file back and confirm the file has been correctly written
        correct_file_contents = "#EXTM3U\n#EXTINF:,\nbob/V/01 - epic song.flac\n#EXTINF:,\nSega/Sonic Songs/02 - sonic theme song.mp3\n#EXTINF:,\nLarry Luu/Great Hits/super super!.m4a\n"

        with open('/bar/' + name_of_playlist + '.M3U8') as f:
            f_content = f.read()
            assert f_content == correct_file_contents, print(f_content, correct_file_contents)
