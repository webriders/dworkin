WR.util.namespace('WR.Dworkin');

WR.Dworkin.comments = {


    init: function() {
        this.initComments();
    },

    initComments: function() {

        $('div.replyLink a').click(function(e) {
            var clickEvent = e;
            e.preventDefault();
            
            var commentId = $(this).attr('href');
            $(commentId).toggle()
        });

        $("form.comment-form").submit(function(e) {
            if( $.trim( this.elements["comment"].value ) == '' )
                return false;
        });
    }

};

$(function() {
    WR.Dworkin.comments.init();
});
