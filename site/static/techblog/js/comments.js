WR.util.namespace('WR.Dworkin');

WR.Dworkin.feedback = {


    init: function() {
        this.initComments();
    },

    initComments: function() {

        $('a.showCommentLink').click(function(e) {
            var clickEvent = e;
            e.preventDefault();
            
            var commentId = $(this).attr('href');
            $(commentId).toggle()
        });
    }

};

$(function() {
    WR.Dworkin.feedback.init();
});
