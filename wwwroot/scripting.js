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
        data() {
            this.nextBookmarkId = 0;
            this.nextTagId = 0;
            return {
                bookmarks: [
                    { id: this.nextBookmarkId++, label: "Vanity", text: "https://www.mattsacommonname.com", url: "Look at me!" },
                    { id: this.nextBookmarkId++, label: "BeagleWizard", text: "https://github.com/mattsacommonname/BeagleWizard", url: "So meta" },
                    { id: this.nextBookmarkId++, label: "Vue", text: "https://vuejs.org", url: "framework" },
                ],
                loggedIn: true,
                tags: [{ id: this.nextTagId++, label: "dev" }],
            }
        }
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
