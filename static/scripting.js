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

    /**
     * Deletes the bookmark represented by the current model.
     *
     * @param {jQuery.Event} e The jQuery click event. Contains the model in data.
     */
    deleteClick: function(e) {
        bookmarkId = this.model.get('id');
        $.ajax({
            context: this,
            type: 'DELETE',
            url: `/b/${bookmarkId}`,
            error: function(request, status, err) {
                console.error(`error deleting bookmark ${bookmarkId}: ${err}`);
            },
            success: function(data, status, request) {
                this.remove();
            }
        });
    },

    /**
     * Renders the bookmark to the row element it's been assigned.
     *
     * @returns {BookmarkView} The current BookmarkView.
     */
    render: function() {
        let bookmarkId = this.model.get('id');
        let context = {
            id: bookmarkId,
            label: this.model.get('label'),
            text: this.model.get('text'),
            url: this.model.get('url')
        };
        let output = BookmarkTemplate(context);
        this.$el.html(output);
        $(`#delete-${bookmarkId}`).click(this, function (e) { e.data.deleteClick(e); });
        let tagCell = $(`#tags-${bookmarkId}`);
        let tags = this.model.get('tags');
        for (tag of tags) {
            let bookmark_tag_model = new BookmarkTagModel({
                bookmark_id: bookmarkId,
                id: tag.id,
                label: tag.label
            });
            let bookmark_tag_view = new BookmarkTagView({ model: bookmark_tag_model });
            tagCell.append(bookmark_tag_view.$el);
            bookmark_tag_view.render();
        }
        return this;
    }
});

var BookmarkListView = Backbone.View.extend({
    model: BookmarkCollection,

    /**
     * Renders a list of bookmarks to the assigned element.
     *
     * @returns {BookmarkListView} This BookmarkListView.
     */
    render: function() {
        this.$el.html('');
        for (bookmark of this.model) {
            let bookmark_view = new BookmarkView({model: bookmark});
            this.$el.append(bookmark_view.$el);
            bookmark_view.render();
        }
        return this;
    },

    /**
     * Updates the list view by fetching the collection and rendering it.
     */
    update: function() {
        this.model.fetch({
            view: this,

            /**
             */
            success: function(collection, response, options) {
                options.view.render();
            }
        });
    }
});

var BookmarkTagTemplate = Handlebars.compile($('#bookmark-tag-template').html());

var BookmarkTagModel = Backbone.Model.extend({});

var BookmarkTagView = Backbone.View.extend({
    model: BookmarkTagModel,
    tagName: 'span',
    render: function() {
        let context = {
            bookmark_id: this.model.get('bookmark_id'),
            id: this.model.get('id'),
            label: this.model.get('label')
        };
        let output = BookmarkTagTemplate(context);
        this.$el.html(output);
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

    /**
     * Deletes the tag represented by the model.
     *
     * @param {jQuery.Event} e Click event. Contains the model in data.
     */
    clickDelete: function(e) {
        tagId = this.model.get('id');
        $.ajax({
            context: this,
            type: 'DELETE',
            url: `/t/${tagId}`,
            error: function(request, status, err) {
                console.error(`error deleting tag ${tagId}: ${err}`);
            },
            success: function(data, status, request) {
                this.remove();
            }
        });
    },

    /**
     * Renders the tag to the assigned element.
     *
     * @returns {TagView} This TagView.
     */
    render: function() {
        let tagId = this.model.get('id');
        let context = {
            id: tagId,
            label: this.model.get('label'),
        };
        let output = TagTemplate(context);
        this.$el.html(output);
        $(`#delete-${tagId}`).click(this, function (e) { e.data.clickDelete(e); });
        return this;
    }
});

var TagListView = Backbone.View.extend({
    model: TagCollection,

    /**
     * Renders the collection of tags.
     *
     * @returns {TagListView} This TagListView.
     */
    render: function() {
        this.$el.html('');
        for (tag of this.model) {
            let tag_view = new TagView({model: tag});
            this.$el.append(tag_view.$el);
            tag_view.render();
        }
        return this;
    },

    /**
     * Updates the list view by fetching the collection and rendering it.
     */
    update: function() {
        this.model.fetch({
            view: this,

            /**
             */
            success: function(collection, response, options) {
                options.view.render();
            }
        });
    }
});

// perform logic that needs the DOM to have finished loading
$(document).ready(function() {
    var bookmarks = new BookmarkCollection();

    var bookmarks_view = new BookmarkListView({
        el: $('#bookmark-list'),
        model: bookmarks
    });

    bookmarks_view.update();

    var tags = new TagCollection();

    var tags_view = new TagListView({
        el: $('#tag-list'),
        model: tags
    });

    tags_view.update();

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
                bookmarks.add(data, {at: 0});
                bookmarks_view.render();
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
                tags_view.render();
            }
        });
    });
});

})();
