Item = Backbone.Model.extend({
    url: "",
    initialize: function() {
        this.readForm();
        this.bind("change", this.updateForm);
    },
    formElements: function() {
        return $('input[id^="id_'+this.attributes.prefix+'"]');
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

ItemList = Backbone.Collection.extend({
    url: "",
    model: Item,
    parseForm: function(namespace) {
        var forms = $('#' + namespace + '-forms');
        forms.children().each(_.bind(function(idx, el){
            var obj = new this.model({prefix: el.id+"-"});
            this.add(obj);
        }, this));
    },
});

ManagementForm = Backbone.View.extend({
    initialize: function() {
        this.options.collection.bind("reset", this.update, this);
        this.options.collection.bind("add", this.update, this);
        this.options.collection.bind("remove", this.update, this);
    },
    update: function() {
        $("#id_"+this.options.namespace+"-TOTAL_FORMS").val(this.options.collection.length);
    }
})

EmptyForm = Backbone.View.extend({
    elements: function() {
        return this.$('input[id*="__prefix__"]')
    },
    cloneForm: function(formId) {
        return this.elements().map(function(idx, el) {
            el = $(el);
            var newEl = el.clone();
            newEl.attr('id', el.attr('id').replace('__prefix__', formId));
            newEl.attr('name', el.attr('name').replace('__prefix__', formId));
            return newEl.get();
        });
    }
})

ListItemView = Backbone.View.extend({
    tagName: "div",
    events: {
        "click .delete_button": "deletePushed"
    },
    initialize: function() {
        this.model.bind('change', this.render, this);
    },
    render: function() {
        var html = this.options.template(this.model.toJSON());
        $(this.el).html(html);
        if (this.model.get("hatband_display") === undefined) {
            $.get(this.options.preview_url,
                  this.model.attributes,
                  _.bind(function(data, status, jqXHR) {
                      this.model.set({hatband_display: data});
                  }, this),
                  'html');
        }
        return this;
    },
    deletePushed: function(evt) {
        if (evt.detail < 1) {
          // workaround for a visualsearch bug, pressing enter when there's
          // invalid text in there causes it to "click" on the first button
          // If we don't do this we'll submit the whole form
          evt.preventDefault();
          return;
        }
        this.model.set({DELETE: 1});
        $(this.el).hide('drop');
    }
});

ListView = Backbone.View.extend({
    tagName: "div",
    model_class: Item,
    list_item_view_class: ListItemView,
    collection_class: ItemList,
    initialize: function() {
        if (!this.collection) {
            this.collection = new this.collection_class;
            this.collection.parseForm(this.options.namespace);
        }
        this.options.managementForm = new ManagementForm({
            namespace: this.options.namespace,
            collection: this.collection
        });

        this.collection.each(_.bind(this.displayObject, this));

        this.options.emptyForm.bind('createObject', this.addObjectFromForm, this);
        this.collection.bind('add', this.displayObject, this);
    },
    displayObject: function(obj) {
        var view = new this.list_item_view_class({
                model: obj,
                id: obj.cid,
                namespace: this.options.namespace,
                template: _.template($('#'+this.options.namespace+'-list-item-template').html()),
                preview_url: this.options.preview_url
            });
        $(this.el).append(view.render().el);
    },
    addObjectFromForm: function() {
        var formId = this.collection.length;

        // add a new empty form div to our backend
        var formDiv = $('<div id="' + this.options.namespace + '-' + formId + '" class="' + this.options.namespace + '-object"></div>');
        $("#" + this.options.namespace + "-forms").append(formDiv);

        // clone the empty form, change all its values to hidden and append them
        var els = this.options.emptyForm.cloneForm(formId);
        _.map(els, _.bind(this.setupInput, this, formDiv));

        var obj = new this.model_class({prefix: this.options.namespace+"-"+formId+"-"});
        this.collection.add(obj);
    },
    setupInput: function(formDiv, el) {
            $(el).attr("type", "hidden");
            formDiv.append(el);
    }
});

SortableListView = ListView.extend({
    model_order_attribute: 'order',
    initialize: function() {
        ListView.prototype.initialize.call(this);
        $(this.el).sortable();
        var this_sorted = _.bind(function(){this.sorted();}, this);
        // note jQuery bind, not backbone
        $(this.el).bind('sortupdate', this_sorted);
        this.collection.bind("add", this_sorted, this);
    },
    sorted: function() {
        var models = _.map($(this.el).children(), _.bind(function(item){
            return this.collection.getByCid($(item).attr('id'));
        }, this));
        _.each(models, _.bind(function(model, idx, list) {
            args = {}
            args[this.model_order_attribute] = idx;
            model.set(args);
        }, this));
    }
});
