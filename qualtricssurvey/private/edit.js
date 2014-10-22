function QualtricsSurveyEdit(runtime, element) {
    'use strict';

    var $ = window.$;
    var $element = $(element);
    var buttonSave = $element.find('.save-button');
    var buttonCancel = $element.find('.cancel-button');
    var url = runtime.handlerUrl(element, 'studio_view_save');

    buttonCancel.on('click', function () {
        runtime.notify('cancel', {});
        return false;
    });

    buttonSave.on('click', function () {
        runtime.notify('save', {
            message: 'Saving...',
            state: 'start',
        });
        $.ajax(url, {
            type: 'POST',
            data: JSON.stringify({
                // TODO: Add entries here for each field to be saved
                'display_name': $('#xblock_qualtricssurvey_display_name').val(),
                'survey_id': $('#xblock_qualtricssurvey_survey_id').val(),
                'your_university': $('#xblock_qualtricssurvey_your_university').val(),
                'link_text': $('#xblock_qualtricssurvey_link_text').val(),
                'param_name': $('#xblock_qualtricssurvey_param_name').val(),
            }),
            success: function buttonSaveOnSuccess() {
                runtime.notify('save', {
                    state: 'end',
                });
            },
            error: function buttonSaveOnError() {
                runtime.notify('error', {});
            }
        });
        return false;
    });
    
    $('#display-source').click(function(e) {
    	e.preventDefault();
    	$('#content-source').toggle();
    });
    
}
