var Item = Backbone.Model.extend({
    url: "",
    initialize: function() {
        this.readForm();
        this.bind("change", this.updateForm);
    },
    formElements: function() {
        return $('input[type=hidden][id^="id_'+this.attributes.prefix+'"]');
    },
    readForm: function(){
        var self = this;
        this.formElements().each(function(idx, el){self.readInput(el);});
    },
    readInput: function(input) {
        input = $(input);
        var value = {}
        value[input.attr('name').substr(this.attributes.prefix.length)] = input.val();
        this.set(value, {silent: true});
    },
    updateForm: function() {
        var self = this;
        this.formElements().each(function(idx, el){self.updateInput(el);});
    },
    updateInput: function(input) {
        input = $(input);
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
