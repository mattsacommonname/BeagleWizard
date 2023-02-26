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

#region build & run web app

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();
app.MapRazorPages();

#region stubbed API enpoints & data

var nextBookmarkId = 0;
var bookmarks = new Dictionary<int, StubBookmark>
{
    {nextBookmarkId, new (nextBookmarkId++, "Vanity", "https://www.mattsacommonname.com", "Look at me!")},
    {nextBookmarkId, new (nextBookmarkId++, "BeagleWizard", "https://github.com/mattsacommonname/BeagleWizard", "So meta")},
    {nextBookmarkId, new (nextBookmarkId++, "scriban", "https://github.com/scriban/scriban", "Not Razor; a potential")},
};

app.MapGet("/b", () => Results.Ok(bookmarks.Values));
app.MapGet("/b/{id}", (int id) => Results.Ok(bookmarks[id]));
app.MapPost("/b", (StubBookmark b) =>
{
    b.Id = nextBookmarkId++;
    bookmarks.Add(b.Id, b);
    Results.Created($"/b/{b.Id}", b);
});
app.MapPut("/b/{id}", (int id, StubBookmark b) =>
{
    bookmarks[id] = b;
    return Results.NoContent();
});
app.MapDelete("/b/{id}", (int id) =>
{
    if (bookmarks.TryGetValue(id, out var b))
        return Results.NotFound();

    bookmarks.Remove(id);
    return Results.Ok(b);
});

var nextTagId = 0;
var tags = new Dictionary<int, StubTag>
{
    {nextTagId, new (nextTagId++, "Code")},
};

app.MapGet("/t", () => Results.Ok(tags.Values));
app.MapGet("/t/{id}", (int id) => Results.Ok(tags[id]));
app.MapPost("/t", (StubTag t) =>
{
    t.Id = nextTagId++;
    tags.Add(t.Id, t);
    Results.Created($"/t/{t.Id}", t);
});
app.MapPut("/t/{id}", (int id, StubTag t) =>
{
    tags[id] = t;
    return Results.NoContent();
});
app.MapDelete("/t/{id}", (int id) =>
{
    if (tags.TryGetValue(id, out var t))
        return Results.NotFound();

    tags.Remove(id);
    return Results.Ok(t);
});

#endregion

app.Run();

#endregion

#region stubbed data definitions

public record StubBookmark(int Id, string Label, string Url, string Text, IEnumerable<string>? Tags = null, DateTime? Created = null, DateTime? Modified = null)
{
    public int Id { get; set; } = Id;
    public DateTime? Created { get; set; } = Created ?? DateTime.UtcNow;
    public DateTime? Modified { get; set; } = Modified ?? DateTime.UtcNow;
}

public record StubTag(int Id, string Label)
{
    public int Id { get; set; } = Id;
}

#endregion
