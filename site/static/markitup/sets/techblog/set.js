// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
// Custom TechBlog set.
// ----------------------------------------------------------------------------
(function() {

function showMarkItUpHelp() {
	window.location.href = 'http://markitup.jaysalvat.com/';
}

function customPreview(markitup) {
    var editor = $(markitup.textarea);
    var footer = editor.next('.markItUpFooter');
    var preview = footer.next('.article-preview');

    if (!preview[0]) {
        preview = $('<div class="rich-content article-preview" title="dblclick, чтобы спрятать"></div>').insertAfter(footer);
        preview.dblclick(function() {
            $(this).fadeOut(function() {
                $(this).remove();
            });
        });
    }

    $.ajax({
        type: 'POST',
        url: '/api/parse_html/',
        data: {
            data: editor.val()
        },
        success: function(data) {
            preview.html(data);
        }
    });
}

mySettings = {
	onShiftEnter:	{keepDefault:false, replaceWith:'<br />\n'},
	onCtrlEnter:	{keepDefault:false, openWith:'\n<p>', closeWith:'</p>\n'},
	onTab:			{keepDefault:false, openWith:'    '},
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
		{name:'Убрать тэги', className:'clean', replaceWith:function(markitup) { return markitup.selection.replace(/<(.*?)>/g, "") } },
		{name:'Просмотр', className:'preview', replaceWith:customPreview /* why not call:customPreview? Because I can't get the instance from there */ },
		{separator:'---------------' },
		{name:'Что это за редактор?', className:'help', call:showMarkItUpHelp }
	]
}

})();