$(document).ready(function() {
    
    num = $('#stages_nav').attr('num');
	width = $('#stages_nav').width();
    $('.stage').css('width', 1/num * width - num*2 - 2 + 'px')    
    $('.tablink', this).bind('click', function(){
    
        currtab = $(this);
        $('.tablink').removeClass('on');
        currtab.addClass('on');
        $('.tab').hide();
        $('#' + currtab.attr('id') + 'box').show();
    
    });
    
    
});