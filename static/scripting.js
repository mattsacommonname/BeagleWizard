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

(function(){

var BookmarkTemplate = Handlebars.compile($('#bookmark-template').html());

var BookmarkModel = Backbone.Model.extend({urlRoot: '/b'});

var BookmarkCollection = Backbone.Collection.extend({
    model: BookmarkModel,
    url: '/b'
});

var BookmarkView = Backbone.View.extend({
    model: BookmarkModel,
    tagName: 'tr',
    render: function() {
        let context = {
            id: this.model.get('id'),
            label: this.model.get('label'),
            text: this.model.get('text'),
            url: this.model.get('url')
        };
        let output = BookmarkTemplate(context);
        this.$el.html(output);
        return this;
    }
});

var BookmarkListView = Backbone.View.extend({
    model: BookmarkCollection,
    render: function() {
        for (bookmark of this.model) {
            let bookmark_view = new BookmarkView({model: bookmark});
            this.$el.append(bookmark_view.$el);
            bookmark_view.render();
        }
        return this;
    }
});

var TagTemplate = Handlebars.compile($('#tag-template').html());

var TagModel = Backbone.Model.extend({urlRoot: '/t'});

var TagCollection = Backbone.Collection.extend({
    model: TagModel,
    url: '/t'
});

var TagView = Backbone.View.extend({
    model: TagModel,
    tagName: 'tr',
    render: function() {
        let context = {
            id: this.model.get('id'),
            label: this.model.get('label'),
        };
        let output = TagTemplate(context);
        this.$el.html(output);
        return this;
    }
});

var TagListView = Backbone.View.extend({
    model: TagCollection,
    render: function() {
        for (tag of this.model) {
            let tag_view = new TagView({model: tag});
            this.$el.append(tag_view.$el);
            tag_view.render();
        }
        return this;
    }
});

// perform logic that needs the DOM to have finished loading
$(document).ready(function(){
    var bookmarks = new BookmarkCollection();

    var bookmarks_view = new BookmarkListView({
        el: $('#bookmark-list'),
        model: bookmarks
    });

    bookmarks.fetch({
        success: function(collection, response, options) {
            bookmarks_view.render();
        }
    });

    var tags = new TagCollection();

    var tags_view = new TagListView({
        el: $('#tag-list'),
        model: tags
    });

    tags.fetch({
        success: function(collection, response, options) {
            tags_view.render();
        }
    });
});

})();
