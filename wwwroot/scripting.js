/* Copyright 2023 Matthew Bishop
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

import { createApp } from 'http://localhost:8000/vue/3.2.47/vue.esm-browser.prod.js';


function document_loaded() {
    createApp({
        //#region data

        data() {
            return {
                /**
                 * @property {object[]} List of all bookmarks.
                 */
                bookmarks: null,

                /**
                 * @property {boolean} Logged in.
                 */
                loggedIn: true,

                /**
                 * @property {object} New bookmark model.
                 */
                newBookmark: {
                    label: null,
                    text: null,
                    url: null,
                },

                /**
                 * @property {object} New tag model.
                 */
                newTag: {
                    label: null,
                },

                /**
                 * @property {object[]} List of tags.
                 */
                tags: null,
            };
        },

        //#endregion

        //#region methods

        methods: {
            /**
             * Creates a bookmark by posting it to the appropriate REST endpoint.
             */
            async createBookmark() {
                try {
                    await fetch(
                        "/b",
                        {
                            body: JSON.stringify(this.newBookmark),
                            headers: { "Content-Type": "application/json" },
                            method: "POST",
                        },
                    );
                    this.newBookmark.label = null;
                    this.newBookmark.text = null;
                    this.newBookmark.url = null;
                    await this.readAllBookmarks();
                } catch (error) {
                    console.error(error);
                    return;
                }
            },

            /**
             * Creates a tag by posting it to the appropriate REST endpoint.
             */
            async createTag() {
                try {
                    await fetch(
                        "/t",
                        {
                            body: JSON.stringify(this.newTag),
                            headers: { "Content-Type": "application/json" },
                            method: "POST",
                        },
                    );
                    this.newTag.label = null;
                    await this.readAllTags();
                } catch (error) {
                    console.error(error);
                    return;
                }
            },

            /**
             * Reads all bookmarks from the appropriate REST endpoint.
             */
            async readAllBookmarks() {
                let r = await fetch("/b");
                this.bookmarks = await r.json();
            },

            /**
             * Reads all tags from the appropriate REST endpoint.
             */
            async readAllTags() {
                let r = await fetch("/t");
                this.tags = await r.json();
            },
        },

        //#endregion

        //#region mounted event

        /**
         * Vue app mounted logic.
         */
        mounted() {
            this.readAllBookmarks();
            this.readAllTags();
        },

        //#endregion
    }).mount("#app");
}


try {
    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", document_loaded);
    else
        document_loaded();
} catch (error) {
    console.error(error);
}
