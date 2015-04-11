/**
 * Created by Westron on 3/17/2015.
 */
/**
 * Created by Westron on 3/9/2015.
 */

var $;
var questionWrapper;
var test_id;
var class_id;
var post_url;
function init() {
    $ = jQuery.noConflict();
}

init();


$(document).ready(function () {

    questionWrapper = $('#questions_wrapper');

    test_id = $('#test_id').text();
    class_id = $('#class_id').text();
    post_url = $('#post_url').text();

    initSubmitButton();


});



function initSubmitButton() {
    $('#submit_test_button').click(function (e) {
        e.preventDefault();

        var questionsArray = [];

        questionWrapper.children().each(function packTest() {
            var questionElement = $(this);

            var choice = questionElement.find('input:checked').val();
            questionsArray.push(choice);
        });

        var testObject = {
            test_id: test_id,
            class_id: class_id,
            questions: questionsArray
        };

        postTest(testObject);

    });
}


function postTest(testObject) {

    //var data = $.toJSON(testObject);
    var data = JSON.stringify(testObject);

    var url = post_url;

    doPost(url, data);
}


function doPost(url, data) {
    $.post(url, data, function (postBack) {
        var dialogger =$("#dialog");

            dialogger.dialog(
            {
                buttons: [{
                    text: "Ok", class: 'dialog_button', click: function () {
                        $(this).dialog("close");
                        window.location.replace("/Examera/default/test_page/" + class_id);
                    }
                },
                {
                    text: "Stay Here", class: 'dialog_button', click: function () {
                        $(this).dialog("close");
                    }
                }]
            }
        );

    }).error(function (xhr, status, error) {
        alert("Failed!\n" + error);
    });

}
