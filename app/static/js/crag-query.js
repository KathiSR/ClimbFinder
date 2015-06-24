var substringMatcher = function(strs) {
return function findMatches(q, cb) {
var matches, substrRegex;
 
// an array that will be populated with substring matches
matches = [];
 
// regex used to determine if a string contains the substring `q`
substrRegex = new RegExp(q, 'i');
 
// iterate through the pool of strings and for any string that
// contains the substring `q`, add it to the `matches` array
$.each(strs, function(i, str) {
if (substrRegex.test(str)) {
// the typeahead jQuery plugin expects suggestions to a
// JavaScript object, refer to typeahead docs for more info
matches.push({ value: str });
}
});
 
cb(matches);
};
};
 
 
items = [];
$.getJSON( "static/crags.json", function( data ) {
$.each( data, function( key, val ) {
    items.push(  val  );
});
// This displays the items as a list
// $( "<ul/>", {
//     "class": "my-new-list",
//     html: items.join( ", " )
//     }).appendTo( "body" );
});



$('#crag-query .typeahead').typeahead({
hint: true,
highlight: true,
minLength: 2
},
{
name: 'items',
displayKey: 'value',
source: substringMatcher(items)
});
