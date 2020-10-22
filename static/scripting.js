/* Copyright 2020 Matthew Bishop
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


/**
 * BeagleWizard namespace.
 */
var BeagleWizard = {};


(function(){

/**
 * Application
 */
BeagleWizard.App = new Backbone.Marionette.Application();

BeagleWizard.App.addRegions({
    bookmarkRegion: "#bookmark-list",
    tagRegion: "#tag-list"
});

BeagleWizard.App.addInitializer(function(options){
  let bookmarkTable = new BeagleWizard.BookmarkTableView({
    collection: options.bookmarks
  });
  BeagleWizard.App.bookmarkRegion.show(bookmarkTable);

  let tagTable = new BeagleWizard.TagTableView({
    collection: options.tags
  });
  BeagleWizard.App.tagRegion.show(tagTable);
});


/**
 *
 */
BeagleWizard.BookmarkModel = Backbone.Model.extend({});


/**
 *
 */
BeagleWizard.BookmarkCollection = Backbone.Collection.extend({
    model: BeagleWizard.BookmarkModel,
    url: '/b'
});


/**
 *
 */
BeagleWizard.BookmarkView = Backbone.Marionette.ItemView.extend({
    events: {
        'click .cancel-button': 'cancelEdit',
        'click .edit-button': 'editMode',
        'click .save-button': 'saveChanges'
    },
    tagName: 'tr',
    template: '#bookmark-template',
    ui: {
        display_elements: '.display-element',
        edit_elements: '.edit-element',
        edit_label: '.bookmark-edit-label',
        edit_text: '.bookmark-edit-text',
        edit_url: '.bookmark-edit-url'
    },

    cancelEdit: function(e){
        this.ui.edit_label.val(this.model.get('label'));
        this.ui.edit_text.val(this.model.get('text'));
        this.ui.edit_url.val(this.model.get('url'));
        this.ui.display_elements.removeClass('is-hidden');
        this.ui.edit_elements.addClass('is-hidden');
        this.render();
    },

    editMode: function(e){
        this.ui.display_elements.addClass('is-hidden');
        this.ui.edit_elements.removeClass('is-hidden');
    },

    saveChanges: function(e){
        let updates = {
            'label': this.ui.edit_label.val(),
            'text': this.ui.edit_text.val(),
            'url': this.ui.edit_url.val()
        };
        this.model.set(updates);
        this.model.save();
        this.ui.display_elements.removeClass('is-hidden');
        this.ui.edit_elements.addClass('is-hidden');
        this.render();
    }
});


/**
 *
 */
BeagleWizard.BookmarkTableView = Backbone.Marionette.CompositeView.extend({
    id: "bookmark-table",
    className: 'is-narrow is-striped is-fullwidth table',
    itemView: BeagleWizard.BookmarkView,
    tagName: "table",
    template: "#bookmark-table-template",

    initialize: function(){
        this.listenTo(this.collection, "sort", this.renderCollection);
    },

    appendHtml: function(collectionView, itemView){
        collectionView.$('tbody').append(itemView.el);
    }
});


/**
 *
 */
BeagleWizard.TagModel = Backbone.Model.extend({});


/**
 *
 */
BeagleWizard.TagCollection = Backbone.Collection.extend({
    model: BeagleWizard.TagModel,
    url: '/t'
});


/**
 *
 */
BeagleWizard.TagView = Backbone.Marionette.ItemView.extend({
    events: {
        'click .cancel-button': 'cancelEdit',
        'click .edit-button': 'editMode',
        'click .save-button': 'saveChanges'
    },
    tagName: 'tr',
    template: "#tag-template",
    ui: {
        display_elements: '.display-element',
        edit_elements: '.edit-element',
        edit_label: '.tag-edit-label'
    },

    cancelEdit: function(e){
        this.ui.edit_label.val(this.model.get('label'));
        this.ui.display_elements.removeClass('is-hidden');
        this.ui.edit_elements.addClass('is-hidden');
        this.render();
    },

    editMode: function(e){
        this.ui.display_elements.addClass('is-hidden');
        this.ui.edit_elements.removeClass('is-hidden');
    },

    saveChanges: function(e){
        this.model.set('label', this.ui.edit_label.val());
        this.model.save();
        this.ui.display_elements.removeClass('is-hidden');
        this.ui.edit_elements.addClass('is-hidden');
        this.render();
    }
});


/**
 *
 */
BeagleWizard.TagTableView = Backbone.Marionette.CompositeView.extend({
    tagName: "table",
    id: "tag-table",
    className: 'is-narrow is-striped table',
    template: "#tag-table-template",
    itemView: BeagleWizard.TagView,

    initialize: function(){
        this.listenTo(this.collection, "sort", this.renderCollection);
    },

    appendHtml: function(collectionView, itemView){
        collectionView.$('tbody').append(itemView.el);
    }
});


// perform logic that needs the DOM to have finished loading
$(document).ready(function(){
    $('#bookmark-add').click(function(e) {
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                label: $('#bookmark-label').val(),
                text: $('#bookmark-text').val(),
                url: $('#bookmark-url').val()
            }),
            dataType: "json",
            type: 'POST',
            url: '/b',
            error: function(request, status, err) {
                console.error(`error adding bookmark: ${err}`);
            },
            success: function(data, status, request) {
                $('#bookmark-label').val('');
                $('#bookmark-text').val('');
                $('#bookmark-url').val('');
                bookmarks.fetch();
            }
        });
    });
    $('#tag-add').click(function(e) {
        $.ajax({
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                label: $('#tag-label').val()
            }),
            dataType: "json",
            type: 'POST',
            url: '/t',
            error: function(request, status, err) {
                console.error(`error adding tag: ${err}`);
            },
            success: function(data, status, request) {
                $('#tag-label').val('');
                tags.fetch();
            }
        });
    });

    let bookmarks = new BeagleWizard.BookmarkCollection();
    bookmarks.fetch();

    let tags = new BeagleWizard.TagCollection();
    tags.fetch();

    BeagleWizard.App.start({
        bookmarks: bookmarks,
        tags: tags
    });
});

})();
