odoo.define('web_dynamic_sepator_float', function (require) {
"use strict";

var core = require('web.core');
var form_widgets = require('web.form_widgets'); 

var _t = core._t;
var QWeb = core.qweb;
var FieldFloat = form_widgets.FieldFloat;

var list_widget_registry = core.list_widget_registry;

var ColumnValidation = list_widget_registry.get('field.boolean').extend({
    /**
     * Return a potentially icon
     *
     * @private
     */
    _format: function (row_data, options) {
        return _.str.sprintf('<img src="js_utility/static/src/img/%s" %s/><span/></div>',
                 row_data[this.id].value ? 'valide.png' : 'non-valide.png', 
                 row_data[this.id].value ? 'title="Etat validé"' : 'title="En attente de validation"' 
                );
    }

});


var HorizontalSeparator = FieldFloat.extend({
    events: {
        'keyup': function (e) {
            if(this.$input.val() && e.keyCode != 16 && e.keyCode != 188 && e.keyCode != 37){
                this.number = this.$input.val();
                this.numberRemoveSpace();
                this.virguleToPoint();
                var value = parseFloat(this.number);
                this.numberFormater = (value).toLocaleString('fr-FR');
                this.$input.val(this.numberFormater);
            }

        },
        'change': 'store_dom_value',
    },
    parse_value: function(val, def) {
        self = this;
        self.res = val;
        
        this.numberRemoveSpace();
        this.virguleToPoint();
        self.res = this.number;
        return this._super(self.res, def);
    },
    format_value: function(val, def) {
        self = this;
        self.res = val;

        self.res = parseFloat(self.res);
        self.res = (self.res).toLocaleString('fr-FR');
        return this._super(self.res, def);
    },
    virguleToPoint: function(){
        self = this;

        this.number = this.number
                          .split(',')
                          .join('.');

    },
    numberRemoveSpace: function(){
        self = this;

        self.rm = this.number.split(String.fromCharCode(160));
        this.number =  self.rm.join('');
    },
    numberReplaceKnownCaracter: function(){
        self = this;

        self.knownCaracter = String.fromCharCode(160); 
        this.numberFormater = this.numberFormater
                                  .split(self.knownCaracter)
                                  .join(' ');

    },



    
});



/**
 * Registry of form fields, called by :js:`instance.web.FormView`.
 *
 * All referenced classes must implement FieldInterface. Those represent the classes whose instances
 * will substitute to the <field> tags as defined in OpenERP's views.
 */
core.form_widget_registry.add('horizontalseparator', HorizontalSeparator);
list_widget_registry.add('field.validation', ColumnValidation);



return {
    
    HorizontalSeparator: HorizontalSeparator,
    ColumnValidation: ColumnValidation,

};

});
