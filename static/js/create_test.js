/**
 * Created by Westron on 3/9/2015.
 */

var qidNumber;
var $;
function init() {
    qidNumber = 0;
    $ = jQuery.noConflict();


}

init();


$(document).ready(function () {

    $('#add_question').click(function () {

        qidNumber++;

        var wrapper = $('#questions_wrapper');

        var newQuestion = wrapper.children().first().clone();


        newQuestion.attr("id", "questions_table_" + qidNumber);


        newQuestion.appendTo(wrapper);

        initRemoveButtons(newQuestion);

    });

    initRemoveButtons($('#questions_table_0'));

});
function initRemoveButtons(newQuestion) {


        newQuestion.find('.remove_question').click(function () {
            var wrapper = $('#questions_wrapper');
            //var me = $(this);
            if (wrapper.children().length > 1) {
                qidNumber--;
                $(this).closest('.questions_table').remove();
            }
            else{
                //flash need one q
            }
        });
}

