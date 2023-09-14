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

var sqliteSource = GetSetting(SQLiteSourceVariable, SQLiteSourceDefault);

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

app.MapEndpoints(
    BookmarkEndpoints.Mapping,
    TagEndpoints.Mapping);

var url = GetSetting(AppUrlVariable, AppUrlDefault);

app.Run(url);

#endregion

/// <summary>
/// Gets a setting value, or returns a default.
/// </summary>
/// <param name="name">Name of the setting to retrieve.</param>
/// <param name="defaultValue">Default value to return if the setting is not set.</param>
/// <returns>Setting value or the default.</returns>
/// <remarks>
/// This will retrieve the environment value that corresponds to <paramref name="name"/>, or returns
/// <paramref name="defaultValue"/>.
/// </remarks>
static string? GetSetting(string name, string? defaultValue = null)
    => Environment.GetEnvironmentVariable(name) ?? defaultValue;
