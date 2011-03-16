from mutagen.flac import FLAC

class FlacCompare:
    """Can compare and merge two flac files. Is instantied with one old and
    one new flac object representing different flac files. The flac object
    should be mutagen FLAC instances or similar.
    """

    def __init__(self, oldflac, newflac):
        self.oldflac=oldflac
        self.newflac=newflac

    def common_tags(self):
        """Return the common tags for the flac files."""
        return filter(lambda x: x in self.oldflac, self.newflac)

    def new_tags(self):
        """Return tags exist in newflac but not oldflac."""
        return filter(lambda x: x not in self.oldflac, self.newflac)

    def removed_tags(self):
        """Return tags exist in oldflac but not newflac."""
        return filter(lambda x: x not in self.newflac, self.oldflac)

    def changed_tags(self):
        """Return tags changed between the two flacs."""
        result=[]
        for x in self.common_tags():
            if self.newflac[x]!=self.oldflac[x]:
                result.append(x)
        return result
                

    def audio_equal(self):
        """Compare if the audio part of the two flacs are equal. This is
        done comparing MD5 signature, total samples and length.
        Returns true if one of the flacs does not have a info block with
        the stream info."""
        if self.oldflac.info is None or self.newflac.info is None:
            # If either of the datasets not has an info-block
            # then assume that they are equal.
            return True
        if self.oldflac.info.md5_signature!=self.newflac.info.md5_signature:
            return False
        if self.oldflac.info.total_samples!=self.newflac.info.total_samples:
            return False
        if self.oldflac.info.length!=self.newflac.info.length:
            return False
        return True
    

    def merge(self):
        """Merge missing tags in oldflac into newflac."""
        if not self.audio_equal():
            raise Exception
        for k in self.oldflac.keys():
            if k not in self.newflac:
                self.newflac[k]=self.oldflac[k]

    def merge_reverse(self):
        """Merge missing tags in newflac into oldflac."""
        if not self.audio_equal():
            raise Exception
        for k in self.newflac.keys():
            if k not in self.oldflac:
                self.oldflac[k]=self.newflac[k]


    def equals(self):
        """Compare the two flacs."""
        if not self.audio_equal():
            return False
        if self.new_tags() != []:
            return False
        if self.removed_tags() != []:
            return False
        if self.changed_tags() != []:
            return False
        return True



class metadata_flac_stream_info:
    bits_per_sample=None
    channels=None
    code=None
    length=None
    max_blocksize=None
    max_framesize=None
    md5_signature=None
    min_blocksize=None
    min_framesize=None
    sample_rate=None
    total_samples=None

class DummyFlac(FLAC):

    def load(self, filename):
        """Load file information from a filename."""

        self.metadata_blocks = [metadata_flac_stream_info()]
        self.tags = None
        self.cuesheet = None
        self.seektable = None
        self.filename = filename
