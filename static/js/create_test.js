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

        initRemoveButtons();

    });

    initRemoveButtons();

});
function initRemoveButtons() {
    var qTable = $('#questions_table_' + qidNumber);
    var thisRemoveButton = qTable.find('.remove_question');
        thisRemoveButton.click(function () {
            var wrapper = $('#questions_wrapper');
            //var me = $(this);
            if (wrapper.children().length > 1) {
                qidNumber--;
                qTable.closest('.questions_table').remove();
            }
            else{
                //flash need one q
            }
        });
}

