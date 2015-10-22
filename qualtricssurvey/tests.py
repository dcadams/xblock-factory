import mock
import unittest

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from xblock.field_data import DictFieldData

from qualtricssurvey import QualtricsSurvey


class QualtricsSurveyXblockTests(unittest.TestCase):

    def make_an_xblock(self, **kw):

        course_id = SlashSeparatedCourseKey('foo', 'bar', 'baz')
        runtime = mock.Mock(course_id=course_id)
        scope_ids = mock.Mock()

        field_data = DictFieldData(kw)
        xblock = QualtricsSurvey(runtime, field_data, scope_ids)
        xblock.xmodule_runtime = runtime
        return xblock

    def test_student_view(self):
        """
        Checks the student view with param_name but without anonymous_user_id.
        """

        xblock = self.make_an_xblock()    
        fragment = xblock.student_view()

        url_frag = 'href="https://stanford.qualtrics.com/SE/?SID=Enter your survey ID here.&amp;a='
        self.assertIn(url_frag, fragment.content)
        url_frag = '>" target="_blank">click here'
        self.assertIn(url_frag, fragment.content)

    def test_student_view_no_param_name(self):
        """
        Checks the student view without param_name; user id part should be missing.
        """

        xblock = self.make_an_xblock(param_name=None)
        fragment = xblock.student_view()

        url = '"https://stanford.qualtrics.com/SE/?SID=Enter your survey ID here." target="_blank">click here'
        self.assertIn(url, fragment.content)

    def test_studio_view(self):
        """
        Checks studio view which should contain the source text with %%USER_ID%%.
        """

        xblock = self.make_an_xblock()
        fragment = xblock.studio_view()

        source_text = 'href="https://stanford.qualtrics.com/SE/?SID=Enter your survey ID here.&amp;amp;a=%%USER_ID%%" target="_blank"&gt;click here'
        self.assertIn(source_text, fragment.content)
