//possible future image upload JS here - trying to make the site as independent on JS as we can...
var $node = "";
var varCount = 1;
//add a new node
var prependE = 0;

$('#addVar').on('click', function(){
    varCount++;
    if(prependE==0) {
        prependE = this;
    }
    $node = '<p><label for="image'+varCount+'">Image '+varCount+': </label><input type="file" name="image'+varCount+'" id="image'+varCount+'"></p>';
    $(prependE).parent().parent().append($node);
    prependE = '#image'+(varCount);
});