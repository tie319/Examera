/**
 * Created by Westron on 3/9/2015.
 */
    
var $;
var questionWrapper;
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
                $(this).closest('.questions_table').remove();
            }
            else{
                $('.flash').html('Test needs at least one question').slideDown().delay(2800).fadeOut();
            }
        });
}

function initAddButton(){
    $('#add_question_button').click(function () {

        var newQuestion = questionWrapper.children().first().clone();

        newQuestion.appendTo(questionWrapper);

        initRemoveButtons();

    });
}

function initSubmitButton(){
    $('#submit_test_button').click(function () {

        var testName = $('#test_name_input').val();

        var testInfo = $('#test_info_input').val();

        var questionsArray = [];

        questionWrapper.children().each(function packTest(){
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
        }

        postTest(testObject);

    });
}


function postTest(testObject) {

 var data = $.toJSON(testObject);
 var url = "{{=URL('default', 'new_test')}}";

 doPost(url, data);
}


function doPost(callback, data) {
 $.post(callback, data, function(data){})
 .done(function() { alert("Done!"); })
 .fail(function() { alert("Failed!");})
}
