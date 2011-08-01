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
    options.query = options.query || '';
    VS.init({
      container  : $("#generic_key_" + id),
      query      : options.query,
      unquotable : [
        'text',
        'account',
        'filter',
        'access'
      ],
      callbacks  : {
        search : function(query) {
          if (query.length <= 0) {
            return;
          }
          var result = query.split(":", 2),
              model = result[0],
              content_type_id = facets.raw[model].id,
              model_id = result[1].slice(2); // ditch the ' "'
          $("#" + id).val(model_id);
          $("#" + id.replace("object_id", "content_type")).val(content_type_id);
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
          var app_label = facets.raw[facet].app_label,
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
