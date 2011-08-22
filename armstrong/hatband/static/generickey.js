var jQuery = jQuery || django.jQuery;
var armstrong = armstrong || {};
armstrong.widgets = armstrong.widgets || {};

armstrong.widgets.generickey = function($, options) {
  var id = options.id,
      object_id_name = options.object_id_name || "object_id",
      content_type_name = options.content_type_name || "content_type",
      object_id_input = $("#" + id),
      pk_input = $("#" + id.replace(object_id_name, "id")),
      content_type_input = $("#" + id.replace(object_id_name, content_type_name)),
      container = $("#generic_key_" + id),
      row = container.parents("tr"),
      params = {
        object_id: row.find("." + object_id_name + ' input[type="hidden"]').val(),
        content_type_id: row.find("." + content_type_name + " input").val()
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
          clearSearch: function(callback) {
            content_type_input.removeAttr("value");
            object_id_input.removeAttr("value");
            row.find('.delete input').attr({"checked": "checked"});
            callback();
          },
          search : function(query) {
            if (query.length <= 0) {
              return;
            }
            var result = query.split(":", 2),
                model = result[0],
                content_type_id = facets.raw[model].id,
                model_id = result[1].slice(2); // ditch the ' "'
            object_id_input.val(model_id);
            content_type_input.val(content_type_id);
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
