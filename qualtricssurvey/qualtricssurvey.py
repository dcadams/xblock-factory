"""
This is the core logic for the Qualtrics Survey
"""
import os

import pkg_resources, cgi

from xblock.core import XBlock
from xblock.fields import Scope
from xblock.fields import String
from xblock.fragment import Fragment


class QualtricsSurvey(XBlock):
    """
    Xblock for creating a Qualtrics survey.
    """
    display_name = String(
        default='Qualtrics Survey',
        scope=Scope.settings,
    )
    survey_id = String(
        # Default provided by placeholder in edit.html
        default='',
        scope=Scope.settings,
    )
    your_university = String(
        default='stanford',
        scope=Scope.settings,
    )                       
    link_text = String(
        default='click here',
        scope=Scope.settings,
    )
    param_name = String(
        default='a',
        scope=Scope.settings,
    )

    def student_view(self, context=None):
        """
        Build the fragment for the default student view
        """

        display_name = self.display_name
        survey_id = self.survey_id
        your_university = self.your_university
        link_text = self.link_text
        param_name = self.param_name

        anon_user_id = self.xmodule_runtime.anonymous_student_id

        # %%PARAM%% substitution only works in HTML components
        # so it has to be done here for ANON_USER_ID
        user_id_string = ""
        if param_name:
            user_id_string = ('&amp;{param_name}={anon_user_id}').format(
                param_name=param_name,
                anon_user_id=anon_user_id,
            )

        html_source = self.get_resource_string('view.html')
        html_source = html_source.format(
            self=self,
            display_name=display_name,
            survey_id=survey_id,
            your_university=your_university,
            link_text=link_text,
            user_id_string=user_id_string,
        )

        fragment = self.build_fragment(
            html_source=html_source,
        )

        return fragment

    def studio_view(self, context=None):
        """
        Build the fragment for the edit/studio view
        """

        display_name = self.display_name
        survey_id = self.survey_id
        your_university = self.your_university
        link_text = self.link_text
        param_name = self.param_name

        # Show the %%USER_ID%% string in the source view
        user_id_string = ""
        if param_name:
            user_id_string = ('&amp;{param_name}={anon_user_id}').format(
                param_name=param_name,
                anon_user_id='%%USER_ID%%',
            )

        source_text = """
        <p>The survey will open in a new browser tab or window.</p>
        <p><a href="https://""" + your_university + """.qualtrics.com/SE/?SID=""" + survey_id + user_id_string + """" target="_blank">""" + link_text + """</a></p>
        """
 
        source_content = cgi.escape(source_text)

        html_source = self.get_resource_string('edit.html')
        html_source = html_source.format(
            self=self,
            display_name=display_name,
            survey_id=survey_id,
            your_university=your_university,
            link_text=link_text,
            source_content=source_content,
        )

        fragment = self.build_fragment(
            html_source=html_source,
            path_css='edit.less.min.css',
            path_js='edit.js.min.js',
            fragment_js='QualtricsSurveyEdit',
        )
        return fragment

    @XBlock.json_handler
    def studio_view_save(self, data, suffix=''):
        """
        Save XBlock fields

        Returns: the new field values
        """

        self.display_name = data['display_name']
        self.survey_id = data['survey_id']
        self.your_university = data['your_university']
        self.link_text = data['link_text']
        self.param_name = data['param_name']
        return {
            'display_name': self.display_name,
            'survey_id': self.survey_id,
            'your_university': self.your_university,
            'link_text': self.link_text,
            'param_name': self.param_name,
        }

    def get_resource_string(self, path):
        """
        Retrieve string contents for the file path
        """
        path = os.path.join('public', path)
        resource_string = pkg_resources.resource_string(__name__, path)
        return resource_string.decode('utf8')

    def get_resource_url(self, path):
        """
        Retrieve a public URL for the file path
        """
        path = os.path.join('public', path)
        resource_url = self.runtime.local_resource_url(self, path)
        return resource_url

    def build_fragment(self,
        html_source=None,
        path_css=None,
        path_js=None,
        fragment_js=None,
    ):
        """
        Assemble the HTML, JS, and CSS for an XBlock fragment
        """

        fragment = Fragment(html_source)
        if path_css:
            css_url = self.get_resource_url(path_css)
            fragment.add_css_url(css_url)
        if path_js:
            js_url = self.get_resource_url(path_js)
            fragment.add_javascript_url(js_url)
        if fragment_js:
            fragment.initialize_js(fragment_js)

        return fragment
