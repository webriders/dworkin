var Markups = {
    utils: {
        underscore: function(markItUp, char) {
            heading = '';
            n = $.trim(markItUp.selection || markItUp.placeHolder).length;
            for (i = 0; i < n; i++) {
                heading += char;
            }
            return '\n' + heading;
        }
    },

    //======================================
    // HTML Markup
    //======================================
    html: {
        nameSpace: 'htmlMarkup',
        previewParserPath: '/markitup/preview/html/',
        onShiftEnter:    {keepDefault:false, replaceWith:'<br />\n'},
        onCtrlEnter:    {keepDefault:false, openWith:'\n<p>', closeWith:'</p>\n'},
        onTab:            {keepDefault:false, openWith:'    '},
        markupSet: [
            {name:'Заголовок 1', key:'1', openWith:'<h1(!( class="[![Class]!]")!)>', closeWith:'</h1>', placeHolder:'Ваш заголовок...' },
            {name:'Заголовок 2', key:'2', openWith:'<h2(!( class="[![Class]!]")!)>', closeWith:'</h2>', placeHolder:'Ваш заголовок...' },
            {name:'Заголовок 3', key:'3', openWith:'<h3(!( class="[![Class]!]")!)>', closeWith:'</h3>', placeHolder:'Ваш заголовок...' },
            {name:'Заголовок 4', key:'4', openWith:'<h4(!( class="[![Class]!]")!)>', closeWith:'</h4>', placeHolder:'Ваш заголовок...' },
            {name:'Заголовок 5', key:'5', openWith:'<h5(!( class="[![Class]!]")!)>', closeWith:'</h5>', placeHolder:'Ваш заголовок...' },
            {name:'Заголовок 6', key:'6', openWith:'<h6(!( class="[![Class]!]")!)>', closeWith:'</h6>', placeHolder:'Ваш заголовок...' },
            {name:'Абзац', openWith:'<p(!( class="[![Class]!]")!)>', closeWith:'</p>' },
            {separator:'---------------' },
            {name:'Жирный', key:'B', openWith:'(!(<strong>|!|<b>)!)', closeWith:'(!(</strong>|!|</b>)!)' },
            {name:'Наклонённый', key:'I', openWith:'(!(<em>|!|<i>)!)', closeWith:'(!(</em>|!|</i>)!)' },
            {name:'Перечёркнутый', key:'S', openWith:'<del>', closeWith:'</del>' },
            {separator:'---------------' },
            {name:'Ul', openWith:'<ul>\n', closeWith:'</ul>\n' },
            {name:'Ol', openWith:'<ol>\n', closeWith:'</ol>\n' },
            {name:'Li', openWith:'<li>', closeWith:'</li>' },
            {separator:'---------------' },
            {name:'Рисунок', key:'P', replaceWith:'<img src="[![Путь к рисунку:!:http://]!]" alt="[![Alt-текст]!]" />' },
            {name:'Ссылка', key:'L', openWith:'<a href="[![Ссылка:!:http://]!]"(!( title="[![Hint-текст]!]")!)>', closeWith:'</a>', placeHolder:'Текст...' },
            {name:'Код (блок)', className:'code-block', openWith:'<pre><code language="[![Язык программирования:!:]!]">', closeWith:'</code></pre>', placeHolder:'[source code]' },
            {name:'Код (inline)', className:'code-inline', openWith:'<code language="[![Язык программирования:!:]!]">', closeWith:'</code>', placeHolder:'[source code]' },
            {separator:'---------------' },
            {name:'Убрать тэги', className:'clean', replaceWith:function(markitup) {
                return markitup.selection.replace(/<(.*?)>/g, "")
            } },
//            {name:'Просмотр', className:'preview', replaceWith:customPreview /* why not call:customPreview? Because I can't get the instance from there */ },
//            {separator:'---------------' },
//            {name:'Что это за редактор?', className:'help', call:showMarkItUpHelp }
            {separator:'---------------' },
            {name:'Preview', className:'preview', call:'preview'}
        ]
    },

    //======================================
    // Markdown Markup
    //======================================
    markdown: {
        nameSpace: 'markdownMarkup',
        previewParserPath: '/markitup/preview/markdown/',
        onShiftEnter: {keepDefault:false, openWith:'\n\n'},
        markupSet: [
            {name:'First Level Heading', key:'1', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '=')
            } },
            {name:'Second Level Heading', key:'2', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '-')
            } },
            {name:'Heading 3', key:'3', openWith:'### ', placeHolder:'Your title here...' },
            {name:'Heading 4', key:'4', openWith:'#### ', placeHolder:'Your title here...' },
            {name:'Heading 5', key:'5', openWith:'##### ', placeHolder:'Your title here...' },
            {name:'Heading 6', key:'6', openWith:'###### ', placeHolder:'Your title here...' },
            {separator:'---------------' },
            {name:'Bold', key:'B', openWith:'**', closeWith:'**'},
            {name:'Italic', key:'I', openWith:'_', closeWith:'_'},
            {separator:'---------------' },
            {name:'Bulleted List', openWith:'- ' },
            {name:'Numeric List', openWith:function(markItUp) {
                return markItUp.line + '. ';
            }},
            {separator:'---------------' },
            {name:'Picture', key:'P', replaceWith:'![[![Alternative text]!]]([![Url:!:http://]!] "[![Title]!]")'},
            {name:'Link', key:'L', openWith:'[', closeWith:']([![Url:!:http://]!] "[![Title]!]")', placeHolder:'Your text to link here...' },
            {separator:'---------------'},
            {name:'Quotes', openWith:'> '},
            {name:'Code Block / Code', openWith:'(!(\t|!|`)!)', closeWith:'(!(`)!)'},
            {separator:'---------------'},
            {name:'Preview', call:'preview', className:"preview"}
        ]
    },

    //======================================
    // ReST! Markup
    //======================================
    rst : {
        nameSpace: 'ReST',
        previewParserPath: '/markitup/preview/rst/',
        onShiftEnter: {keepDefault:false, openWith:'\n\n'},
        onTab: {keepDefault:false, replaceWith:'    '},
        markupSet: [
            {name:'Level 1 Heading', key:'1', placeHolder:'Your title Here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '#');
            } },
            {name:'Level 2 Heading', key:'2', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '*');
            } },
            {name:'Level 3 Heading', key:'3', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '=');
            } },
            {name:'Level 4 Heading', key:'4', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '-');
            } },
            {name:'Level 5 Heading', key:'5', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '^');
            } },
            {name:'Level 6 Heading', key:'6', placeHolder:'Your title here...', closeWith:function(markItUp) {
                return Markups.utils.underscore(markItUp, '"');
            } },
            {separator:'---------------' },
            {name:'Bold', key:'B', openWith:'**', closeWith:'**', placeHolder:'Input Your Bold Text Here...'},
            {name:'Italic', key:'I', openWith:'`', closeWith:'`', placeHolder:'Input Your Italic Text Here...'},
            {separator:'---------------' },
            {name:'Bulleted List', openWith:'- ' },
            {name:'Numeric List', openWith:function(markItUp) {
                return markItUp.line + '. ';
            } },
            {separator:'---------------' },
            {name:'Picture', key:'P', openWith:'.. image:: ', placeHolder:'Link Your Images Here...'},
            {name:'Link', key:"L", openWith:'`', closeWith:'`_ \n\n.. _`Link Name`: [![Url:!:http://]!]', placeHolder:'Link Name' },
            {name:'Quotes', openWith:'    '},
            {name:'Code', openWith:'\n:: \n\n	 '},
            {separator:'---------------' },
            {name:'Preview', className:'preview', call:'preview'}
        ]
    },

    //======================================
    // Textile Markup
    //======================================
    textile : {
        nameSpace: 'textileMarkup',
        previewParserPath: '/markitup/preview/textile/',
        onShiftEnter:        {keepDefault:false, replaceWith:'\n\n'},
        markupSet: [
            {name:'Heading 1', key:'1', openWith:'h1(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
            {name:'Heading 2', key:'2', openWith:'h2(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
            {name:'Heading 3', key:'3', openWith:'h3(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
            {name:'Heading 4', key:'4', openWith:'h4(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
            {name:'Heading 5', key:'5', openWith:'h5(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
            {name:'Heading 6', key:'6', openWith:'h6(!(([![Class]!]))!). ', placeHolder:'Your title here...' },
            {name:'Paragraph', key:'P', openWith:'p(!(([![Class]!]))!). '},
            {separator:'---------------' },
            {name:'Bold', key:'B', closeWith:'*', openWith:'*'},
            {name:'Italic', key:'I', closeWith:'_', openWith:'_'},
            {name:'Stroke through', key:'S', closeWith:'-', openWith:'-'},
            {separator:'---------------' },
            {name:'Bulleted list', openWith:'(!(* |!|*)!)'},
            {name:'Numeric list', openWith:'(!(# |!|#)!)'},
            {separator:'---------------' },
            {name:'Picture', replaceWith:'![![Source:!:http://]!]([![Alternative text]!])!'},
            {name:'Link', openWith:'"', closeWith:'([![Title]!])":[![Link:!:http://]!]', placeHolder:'Your text to link here...' },
            {separator:'---------------' },
            {name:'Quotes', openWith:'bq(!(([![Class]!])!)). '},
            {name:'Code', openWith:'@', closeWith:'@'},
            {separator:'---------------' },
            {name:'Preview', className:'preview', call:'preview'}
        ]
    },

    init : function() {

        var self = this;

        $('#id_markup').change(function() {

            $("#id_short_raw").markItUpRemove();
            $("#id_description_raw").markItUpRemove();

            if (this.value == 'html') {
                $("#id_short_raw").markItUp(self.html);
                $("#id_description_raw").markItUp(self.html);
            }
            else if (this.value == 'markdown') {
                $("#id_short_raw").markItUp(self.markdown);
                $("#id_description_raw").markItUp(self.markdown);
            }
            else if (this.value == 'rst') {
                $("#id_short_raw").markItUp(self.rst);
                $("#id_description_raw").markItUp(self.rst);
            }
            else if (this.value == 'textile') {
                $("#id_short_raw").markItUp(self.textile);
                $("#id_description_raw").markItUp(self.textile);
            }
        });
    }
};

$(function() {
    Markups.init();
});
