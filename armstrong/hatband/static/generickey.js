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
            callback(facets.data);
          } else if (!facets.inFlight) {
            facets.inFlight = true;
            $.getJSON(options.facetURL, function(data) {
              facets.raw = data;
              for (key in data) {
                facets.data.push(key);
              }
              callback(facets.data);
              facets.inFlight = false;
            });
          }
        },
        valueMatches : function(facet, searchTerm, callback) {
          var app_label = facets.raw[facet],
              model = facet;
          // TODO: don't pound the server
          $.getJSON("/admin/" + app_label + "/" + model + "/search/", {q: searchTerm}, function(data) {
            callback(data.results);
          });
        }
      }
    });
  });
}
