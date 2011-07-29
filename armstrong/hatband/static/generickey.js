var jQuery = jQuery || django.jQuery;
var armstrong = armstrong || {};
armstrong.widgets = armstrong.widgets || {};

armstrong.widgets.generickey = function($, id, options) {
  $(document).ready(function() {
    var facets = {
      inFlight: false,
      data: [],
      raw: false,
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
          if (facets.data.length > 0) {
            console.log("returning facets");
            console.log(facets.data);
            callback(facets.data);
          } else if (!facets.inFlight) {
            facets.inFlight = true;
            console.log("fetching...");
            $.getJSON(options.facetURL, function(data) {
              console.log("return from server");
              console.log(data);
              facets.raw = data;
              for (key in data) {
                facets.data.push(key);
              }
              callback(facets.data);
              facets.inFlight = false;
            });
          } else {
            console.log("currently in flight and no data");
          }
        },
        valueMatches : function(facet, searchTerm, callback) {
          var app_label = facets.raw[facet],
              model = facet;
          console.log(app_label, model);
          // TODO: don't pound the server
          $.getJSON("/admin/" + app_label + "/" + model + "/search/", {q: searchTerm}, function(data) {
            var result = [], match;
            for (idx in data.names) {
              match = data.names[idx];
              result.push(match.text);
            }
            callback(result);
          });
        }
      }
    });
  });
}
