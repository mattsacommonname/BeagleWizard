#region license

/* Copyright 2023 Matthew Bishop
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#endregion

#region usings

using Microsoft.EntityFrameworkCore;

#endregion

#region constants

const string AppUrlDefault = "http://localhost:3000";
const string AppUrlVariable = "URL";

const string CacheControlKey = "Cache-Control";  // TODO: this should probably only be for development
const string CacheControlValue = "no-cache";  // TODO: this should probably only be for development

const string SQLiteSourceDefault = "var/bw.db";
const string SQLiteSourceVariable = "SQLITE_SOURCE";

#endregion

#region build & run web app

var builder = WebApplication.CreateBuilder(args);

builder.Logging
    .ClearProviders()
    .AddConsole();

var sqliteSource = Environment.GetEnvironmentVariable(SQLiteSourceVariable) ?? SQLiteSourceDefault;

builder.Services
    .AddDbContext<BeagleWizardDb>(o => o.UseSqlite($"Data Source={sqliteSource}"))
    .AddDatabaseDeveloperPageExceptionFilter();

var app = builder.Build();

var staticFileOptions = new StaticFileOptions  // TODO: this should probably only be for development
{
    OnPrepareResponse = c => c.Context.Response.Headers.Append(CacheControlKey, CacheControlValue),
};
app.UseDefaultFiles()
    .UseStaticFiles(staticFileOptions);

var bookmarkEndpoints = app.MapGroup(BookmarkEndpoints.Prefix);
BookmarkEndpoints.Map(bookmarkEndpoints);

var tagEndpoints = app.MapGroup(TagEndpoints.Prefix);
TagEndpoints.Map(tagEndpoints);

var url = Environment.GetEnvironmentVariable(AppUrlVariable) ?? AppUrlDefault;

app.Run(url);

#endregion
