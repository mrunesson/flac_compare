import unittest
import sys
import os

class test_compare(unittest.TestCase):

    def setUp(self):
        self.a=flac_compare.DummyFlac(filename="a")
        self.b=flac_compare.DummyFlac(filename="b")
        self.comp=flac_compare.FlacCompare(self.a,self.b)
        pass

    def testEmptyEqual(self):
        # Two equal created flacs should be equal.
        self.assertTrue(self.comp.equals())

    def testMd5Equal(self):
        self.a.info.md5_signature=237904044194413157454606874029895991563
        self.b.info.md5_signature=237904044194413157454606874029895991561
        self.assertFalse(self.comp.equals())
        self.b.info.md5_signature=237904044194413157454606874029895991563
        self.assertTrue(self.comp.equals())

    def testTotalSamplesEqual(self):
        self.a.info.total_samples=2379040
        self.b.info.total_samples=2379041
        self.assertFalse(self.comp.equals())
        self.b.info.total_samples=2379040
        self.assertTrue(self.comp.equals())

    def testLengthEqual(self):
        self.a.info.length=128.3066
        self.b.info.length=129.3066
        self.assertFalse(self.comp.equals())
        self.b.info.length=128.3066
        self.assertTrue(self.comp.equals())

    def testTagsEqual(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag2']=[2]
        self.b['tag3']=[u'val3', u'val4']
        self.assertTrue(self.comp.equals())
        self.b['tag2']=[3]
        self.assertFalse(self.comp.equals())

    def testNotSameTagsEqual(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.assertFalse(self.comp.equals())
        self.b['tag4']=[2]
        self.assertFalse(self.comp.equals())
        self.a['tag4']=[2]
        self.b['tag2']=[2]
        self.assertTrue(self.comp.equals())
        self.b['tag5']=[2]
        self.assertFalse(self.comp.equals())

    def testCommonTags(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.b['tag4']=[2]
        self.assertEquals(self.comp.common_tags(),['tag1','tag3'])


    def testNewTags(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.b['tag4']=[2]
        self.assertEquals(self.comp.new_tags(),['tag4',])

    def testRemovedTags(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.b['tag4']=[2]
        self.assertEquals(self.comp.removed_tags(),['tag2',])

    def testChangedTags(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.b['tag4']=[2]
        self.assertEquals(self.comp.changed_tags(),[])
        self.a['tag3']=[u'val3', u'val4', u'val5']
        self.assertEquals(self.comp.changed_tags(),['tag3'])

    def testMerge(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.b['tag4']=[2]
        self.comp.merge()
        self.assertEquals(self.comp.new_tags(),['tag4',])
        self.assertEquals(self.comp.removed_tags(),[])

    def testReverseMerge(self):
        self.a['tag1']=[u'value1']
        self.a['tag2']=[2]
        self.a['tag3']=[u'val3', u'val4']
        self.b['tag1']=[u'value1']
        self.b['tag3']=[u'val3', u'val4']
        self.b['tag4']=[2]
        self.comp.merge_reverse()
        self.assertEquals(self.comp.new_tags(),[])
        self.assertEquals(self.comp.removed_tags(),['tag2'])

    def testMergeFauilIfNotAudioEqual(self):
        self.a.info.md5_signature=237904044194413157454606874029895991563
        self.b.info.md5_signature=237904044194413157454606874029895991561
        self.failUnlessRaises(Exception, self.comp.merge)
        self.failUnlessRaises(Exception, self.comp.merge_reverse)

        
if __name__ == '__main__':
    try: import flac_compare
    except ImportError:
        sys.path.append(os.path.abspath("../src"))
        import flac_compare

    unittest.main()
