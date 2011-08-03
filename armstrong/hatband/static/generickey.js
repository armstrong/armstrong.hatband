var jQuery = jQuery || django.jQuery;
var armstrong = armstrong || {};
armstrong.widgets = armstrong.widgets || {};

armstrong.widgets.generickey = function($, options) {
  var id = options.id,
      container = $("#generic_key_" + id),
      row = container.parents("tr"),
      params = {
        object_id: row.find('.object_id input[type="hidden"]').val(),
        content_type_id: row.find(".content_type input").val()
      };

  var initVisualSearch  = function() {
    $(document).ready(function() {
      var facets = {
        inFlight: false,
        data: [],
        raw: false,
      };
      options.query = options.query || '';
      VS.init({
        container  : container,
        query      : options.query,
        unquotable : [],
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
  };

  if (params.content_type_id) {
    $.getJSON(options.queryLookupURL, params, function(data) {
      options.query = data.query
      initVisualSearch();
      });
  } else {
    initVisualSearch();
  }
};
