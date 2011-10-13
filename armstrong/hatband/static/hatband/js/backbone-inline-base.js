var Item = Backbone.Model.extend({
    url: "",
    initialize: function() {
        this.bind("change", this.updateForm);
    },
    formElements: function() {
        return django.jQuery('input[type=hidden][id^="id_'+this.attributes.prefix+'"]');
    },
    parse: function(){
        var self = this;
        this.formElements().each(function(idx, el){self.readInput(el);});
    },
    readInput: function(input) {
        var input = django.jQuery(input);
        var value = {}
        value[input.attr('name').substr(this.attributes.prefix.length)] = input.val();
        this.set(value);
    },
    updateForm: function() {
        var self = this;
        this.formElements().each(function(idx, el){self.updateInput(el);});
    },
    updateInput: function(input) {
        var input = django.jQuery(input);
        var name = input.attr('name').substr(this.attributes.prefix.length);
        input.val(this.attributes[name]);
    }
});

var ItemList = Backbone.Collection.extend({
    model: Item
});

var ListItemView = Backbone.View.extend({

});

var ListView = Backbone.View.extend({
    render: function() {
        //_.each(this.list, function(
    }
});
