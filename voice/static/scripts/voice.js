function setEqualHeight(columns) {
     var max_height = 0;

     columns.each( function() {
         curr_height = $(this).height();
         if (curr_height > max_height)
         {
             max_height = curr_height;
         }
     });

     columns.each( function() {
         $(this).height(max_height);
     })
 }

$(document).ready(function() {
    setEqualHeight($(".span4 > .feature"));
});
