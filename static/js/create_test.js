/**
 * Created by Westron on 3/9/2015.
 */

var $;
var questionWrapper;
var url;
function init() {
    $ = jQuery.noConflict();
}

init();


$(document).ready(function () {

    questionWrapper = $('#questions_wrapper');

    initAddButton();

    initSubmitButton();

    initRemoveButtons();

});


function initRemoveButtons() {
    var newQuestion = questionWrapper.children().last();

    newQuestion.find('.remove_question_button').click(function () {
        //var me = $(this);
        if (questionWrapper.children().length > 1) {
            var dialogger =$("#dialog2");
            var $thisButton = $(this);
            dialogger.dialog(
            {
                buttons: [{
                    text: "Yes", class: 'dialog_button', click: function () {
                        $(this).dialog("close");
                        $thisButton.closest('.questions_table').remove();
                    }
                },
                {
                    text: "No", class: 'dialog_button', click: function () {
                        $(this).dialog("close");
                    }
                }]
            }
        );
        }
        else {
            $('.flash').html('Test needs at least one question').slideDown().delay(2800).fadeOut();
        }
    });
}

function initAddButton() {
    $('#add_question_button').click(function () {

        //var newQuestion = questionWrapper.children().first().clone();

        var newQuestion = $("#question_template").children().first().clone();

        newQuestion.appendTo(questionWrapper);

        initRemoveButtons();

    });
}

function initSubmitButton() {
    $('#submit_test_button').click(function (e) {
        e.preventDefault();
        var testName = $('#test_name_input').val();

        var testInfo = $('#test_info_input').val();

        var questionsArray = [];

        questionWrapper.children().each(function packTest() {
            var questionElement = $(this);
            var question = {};
            question.question_text = questionElement.find(".question_text textarea").val();
            question.answer_a = questionElement.find(".answer_a input").val();
            question.answer_b = questionElement.find(".answer_b input").val();
            question.answer_c = questionElement.find(".answer_c input").val();
            question.answer_d = questionElement.find(".answer_d input").val();
            question.correct_answer = questionElement.find(".correct_answer select").val();
            questionsArray.push(question);
        });

        var testObject = {
            test_name: testName,
            test_info: testInfo,
            questions: questionsArray
        };

        postTest(testObject);

    });
}


function postTest(testObject) {

    //var data = $.toJSON(testObject);
    var data = JSON.stringify(testObject);

    var url = "/Examera/default/new_test";

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
                        window.location.replace("/Examera/default/index");
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

    //$.ajax({
    //        url: url,
    //        method: "POST",
    //        data: data,
    //        contentType: "application/json; charset=utf-8",
    //        dataType: "json",
    //        success: function () {
    //            alert("Success!");
    //        },
    //        error: function (xhr, status, error) {
    //            //var err = eval("(" + xhr.responseText + ")");
    //            var d = 4;
    //            alert(error);
    //            alert(d);
    //        }
    //    }
    //)
}
