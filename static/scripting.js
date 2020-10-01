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
    template: "#bookmark-template",
    tagName: 'tr'
});


/**
 *
 */
BeagleWizard.BookmarkTableView = Backbone.Marionette.CompositeView.extend({
    tagName: "table",
    id: "bookmark-table",
    className: 'is-narrow is-striped table',
    template: "#bookmark-table-template",
    itemView: BeagleWizard.BookmarkView,

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
    template: "#tag-template",
    tagName: 'tr'
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
