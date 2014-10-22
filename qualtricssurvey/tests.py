import unittest
import mock

from xblock.field_data import DictFieldData
from opaque_keys.edx.locations import SlashSeparatedCourseKey


class QualtricsSurveyXblockTests(unittest.TestCase):

    def setUp(self):
        self.course_id = SlashSeparatedCourseKey.from_deprecated_string('foo/bar/baz')
        self.runtime = mock.Mock(course_id=self.course_id)
        self.scope_ids = mock.Mock()

    def make_one(self, **kw):

        from qualtricssurvey import QualtricsSurvey as cls
        field_data = DictFieldData(kw)
        block = cls(self.runtime, field_data, self.scope_ids)
        block.xmodule_runtime = self.runtime
        return block

    def test_student_view(self):

        block = self.make_one()    
        fragment = block.student_view()

        # Leaving out the anonymous_user_id part for now as it is going to change
        url_frag = 'href="https://stanford.qualtrics.com/SE/?SID=1234&amp;a='
        self.assertIn(url_frag, fragment.content)
        url_frag = '>" target="_blank">click here'
        self.assertIn(url_frag, fragment.content)

    def test_student_view_no_paramname(self):

        block = self.make_one(paramName='')
        fragment = block.student_view()

        # user id part should be missing
        url = '"https://stanford.qualtrics.com/SE/?SID=1234" target="_blank">click here'
        self.assertIn(url, fragment.content)

    def test_studio_view(self):

        block = self.make_one()
        fragment = block.studio_view()

        # Should contain the source text with %%USER_ID%%
        source_text = 'href="https://stanford.qualtrics.com/SE/?SID=1234&amp;amp;a=%%USER_ID%%" target="_blank"&gt;click here'
        self.assertIn(source_text, fragment.content)
