from src.functions import scan_for_playlists, walkman_playlist_checker
from pyfakefs.fake_filesystem_unittest import TestCase

class TestScanForPlaylists(TestCase):

    def setUp(self):
        self.setUpPyfakefs()

        # fake directory for testing successful playlist finding
        self.fs.create_file('/foo/playlist1.M3U8')
        self.fs.create_file('/foo/playlist2.txt')
        self.fs.create_file('/foo/playlist3.M3U8')
        self.fs.create_file('/foo/playlist4.txt')
        self.fs.create_file('/foo/playlist5.M3U8')
        self.fs.create_file('/foo/playlist6.txt')

        # fake directory for testing successful non-playlist finding
        self.fs.create_file('/bar/playlist1.txt')
        self.fs.create_file('/bar/playlist2.txt')
        self.fs.create_file('/bar/playlist3.txt')
        self.fs.create_file('/bar/playlist4.txt')
        self.fs.create_file('/bar/playlist5.txt')
        self.fs.create_file('/bar/playlist6.txt')

    def test_finds_playlists(self):

        playlists_to_find = ['playlist1', 'playlist3', 'playlist5']

        playlists_found = scan_for_playlists('/foo', walkman_playlist_checker)

        assert playlists_to_find == playlists_found, print(playlists_to_find, playlists_found)

    def test_finds_no_playlists(self):
        playlists_to_find = []

        playlists_found = scan_for_playlists('/bar', walkman_playlist_checker)

        assert playlists_to_find == playlists_found, print(playlists_to_find, playlists_found)