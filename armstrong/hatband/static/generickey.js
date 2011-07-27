var jQuery = jQuery || django.jQuery;
var armstrong = armstrong || {};
armstrong.widgets = armstrong.widgets || {};

armstrong.widgets.generickey = function($, id, options) {
  $(document).ready(function() {
    console.log("wiring up armstrong.widgets.generickey");
    var facets = {
      inFlight: false,
      data: false
    };
    VS.init({
      container  : $(id),
      query      : '',
      unquotable : [
        'text',
        'account',
        'filter',
        'access'
      ],
      callbacks  : {
        search : function(query) {
          console.log(query);
        },
        facetMatches : function(callback) {
          if (facets.data) {
            console.log("returning facets");
            console.log(facets.data);
            callback(facets.data);
          } else if (!facets.inFlight) {
            facets.inFlight = true;
            console.log("fetching...");
            $.getJSON(options.facetURL, function(data) {
              console.log("return from server");
              console.log(data);
              facets.data = data;
              callback(facets.data);
              facets.inFlight = false;
            });
          } else {
            console.log("currently in flight and no data");
          }
        },
        valueMatches : function(facet, searchTerm, callback) {
          callback(["An article", "Some random data", "Awesomeness!"]);
        }
      }
    });
  });
}
