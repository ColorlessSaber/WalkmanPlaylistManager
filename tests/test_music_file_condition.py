from src.functions import music_file_condition

class TestMusicFileCondition:

    def test_music_file_mp3_extension(self):
        file = '01 - epic song.mp3'

        assert music_file_condition(file) is True

    def test_music_file_wav_extension(self):
        file = '01 - epic song.wav'

        assert music_file_condition(file) is True

    def test_music_file_m4a_extension(self):
        file = '01 - epic song.m4a'

        assert music_file_condition(file) is True

    def test_music_file_flac_extension(self):
        file = '01 - epic song.flac'

        assert music_file_condition(file) is True