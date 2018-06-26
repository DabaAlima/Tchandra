odoo.define('web_tree_dynamic_colored_field', function(require)
{
    'use strict';
    var ListView = require('web.ListView'),
        pyeval = require('web.pyeval'),
        py = window.py,
        data_manager = require('web.data_manager'),
        core = require('web.core'),
        data = require('web.data'),
        session = require('web.session');

    var QWeb = core.qweb;

    var pair_colors = function(pair_color){
        if (pair_color !== ""){
            var pair_list = pair_color.split(':'),
                color = pair_list[0],
                expression = pair_list[1];
            return [color, py.parse(py.tokenize(expression)), expression];
        }
    };

    var get_eval_context = function(record){
        return _.extend(
            {},
            record.attributes,
            pyeval.context()
        );
    };

    var colorize_helper = function(obj, record, column, field_attribute, css_attribute){
        var result = '';
        if (column[field_attribute]){
            var colors = _(column[field_attribute].split(';'))
            .chain()
            .map(pair_colors)
            .value()
            .filter(function CheckUndefined(value, index, ar) {
                return value !== undefined;
            });
            var ctx = get_eval_context(record);
            for(var i=0, len=colors.length; i<len; ++i) {
                var pair = colors[i],
                    color = pair[0],
                    expression = pair[1];
                if (py.evaluate(expression, ctx).toJSON()) {
                    result = css_attribute + ': ' + color + ';';
                }
            }
        }
        return result;
    };

    var colorize = function(record, column){
        var res = '';
        res += colorize_helper(this, record, column, 'bg_color', 'background-color');
        res += colorize_helper(this, record, column, 'fg_color', 'color');
        return res;
    };

    ListView.List.include({
        init: function(group, opts){
            this._super(group, opts);
            this.columns.fct_colorize = colorize;
        },

    });

    var row_decoration = [
        'decoration-bf',
        'decoration-it',
        'decoration-danger',
        'decoration-info',
        'decoration-muted',
        'decoration-primary',
        'decoration-success',
        'decoration-warning',
        //Extend Background color put here
        'background-orange',
        'background-blue',
        'background-red',
        'background-yellow',
        'background-black',
        'background-green'
    ];
    var decoration_inherit = '';

    ListView.include({

        willStart: function() {
            var self = this;
            // Retrieve the decoration defined on the model's list view
            this.decoration_inherit = _.pick(this.fields_view.arch.attrs, function(value, key) {
                return row_decoration.indexOf(key) >= 0;
            });
            this.decoration_inherit = _.mapObject(this.decoration_inherit, function(value) {
                return py.parse(py.tokenize(value));
            });

            var fields_def = data_manager.load_fields(this.dataset).then(function(fields_get) {
                self.fields_get = fields_get;
            });
            return $.when(this._super(), fields_def);
        },  

        compute_decoration_classnames: function (record) {
            var classnames= '';
            var context = get_eval_context(record);

            _.each(this.decoration_inherit, function(expr, decoration_inherit) {
                if (py.PY_isTrue(py.evaluate(expr, context))) {
                    classnames += ' ' + decoration_inherit.replace('decoration', 'text');
                }
            });
            return classnames;
        },

    });
});
