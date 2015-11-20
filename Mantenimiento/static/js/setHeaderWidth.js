var $table = $('table.tablesorter'),		
    $bodyCells = $table.find('tbody tr:first').children(),		
    colWidth;		
		
$(window).resize(function() {		
    colWidth = $bodyCells.map(function() {		
        return $(this).width();		
    }).get();		
    		
    $table.find('thead tr').children().each(function(i, v) {		
        $(v).width(colWidth[i]+10);		
    });    		
}).resize(); // Trigger resize handler