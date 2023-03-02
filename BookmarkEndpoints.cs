/// <summary>
/// Bookmark endpoints.
/// </summary>
public static class BookmarkEndpoints
{
    #region shared constants

    /// <summary>
    /// Base name for route naming.
    /// </summary>
    public const string BaseName = "Bookmark";

    /// <summary>
    /// Common root path.
    /// </summary>
    private const string RootPath = "/";

    /// <summary>
    /// Common ID'd path.
    /// </summary>
    private const string IdPath = "/{id}";

    #endregion

    #region create methods

    /// <summary>
    /// Name for Create endpoint.
    /// </summary>
    public const string CreateName = $"{BaseName}.{nameof(Create)}";

    /// <summary>
    /// Relative path for Create endpoint.
    /// </summary>
    public const string CreatePath = RootPath;

    /// <summary>
    /// Endpoint for creating a bookmark.
    /// </summary>
    /// <param name="inputBookmark">The new bookmark data.</param>
    /// <param name="db">The database storing bookmarks.</param>
    /// <param name="linker">The link generator to for determining other endpoint routes.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Create(BookmarkEntity inputBookmark, BeagleWizardDb db, LinkGenerator linker)
    {
        inputBookmark.Created = DateTime.UtcNow;
        inputBookmark.Modified = inputBookmark.Created;
        db.Bookmarks.Add(inputBookmark);
        await db.SaveChangesAsync();

        var uri = linker.GetPathByName(ReadName, new {id = inputBookmark.Id});
        if(uri is null)
            return TypedResults.Problem("Failed to get bookmark read path");

        return TypedResults.Created(uri, inputBookmark);
    }

    #endregion

    #region delete methods

    /// <summary>
    /// Name for delete endpoint.
    /// </summary>
    public const string DeleteName = $"{BaseName}.{nameof(Delete)}";

    /// <summary>
    /// Relative path for delete endpoint.
    /// </summary>
    public const string DeletePath = IdPath;

    /// <summary>
    /// Endpoint for deleting a bookmark.
    /// </summary>
    /// <param name="id">The bookmark to delete's ID.</param>
    /// <param name="db">The database storing bookmarks.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Delete(int id, BeagleWizardDb db)
    {
        var bookmark = await db.Bookmarks.FindAsync(id);
        if (bookmark is null)
            return TypedResults.NotFound();

        db.Bookmarks.Remove(bookmark);
        await db.SaveChangesAsync();

        return TypedResults.Ok(bookmark);
    }

    #endregion

    #region route mapping

    /// <summary>
    /// Maps the bookmark endpoints to routes.
    /// </summary>
    /// <param name="routeBuilder">Route builder to map with.</param>
    public static void Map(IEndpointRouteBuilder routeBuilder)
    {
        routeBuilder.MapDelete(DeletePath, Delete)
            .WithName(DeleteName);
        routeBuilder.MapGet(ReadPath, Read)
            .WithName(ReadName);
        routeBuilder.MapGet(ReadAllPath, ReadAll)
            .WithName(ReadAllName);
        routeBuilder.MapPost(CreatePath, Create)
            .WithName(CreateName);
        routeBuilder.MapPut(UpdatePath, Update)
            .WithName(UpdateName);
    }

    #endregion

    #region read methods

    /// <summary>
    /// Name for individual bookmark Read endpoint.
    /// </summary>
    public const string ReadName = $"{BaseName}.{nameof(Read)}";

    /// <summary>
    /// Relative path for Read endpoint.
    /// </summary>
    public const string ReadPath = IdPath;

    /// <summary>
    /// Endpoint for Reading an individual bookmark.
    /// </summary>
    /// <param name="id">The bookmark to read's ID.</param>
    /// <param name="db">The database storing bookmarks</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Read(int id, BeagleWizardDb db)
        => await db.Bookmarks.FindAsync(id) is BookmarkEntity b ? TypedResults.Ok(b) : TypedResults.NotFound();

    /// <summary>
    /// Name for Read all endpoint.
    /// </summary>
    public const string ReadAllName = $"{BaseName}.{nameof(ReadAll)}";

    /// <summary>
    /// Relative path for Read all endpoint.
    /// </summary>
    public const string ReadAllPath = RootPath;

    /// <summary>
    /// Endpoint for Reading all bookmarks.
    /// </summary>
    /// <param name="db">The database storing bookmarks</param>
    /// <returns>HTTP response.</returns>
    public static IResult ReadAll(BeagleWizardDb db) => TypedResults.Ok(db.Bookmarks);

    #endregion

    #region update methods

    /// <summary>
    /// Name for Update endpoint.
    /// </summary>
    public const string UpdateName = $"{BaseName}.{nameof(Update)}";

    /// <summary>
    /// Relative path for Update endpoint.
    /// </summary>
    public const string UpdatePath = IdPath;

    /// <summary>
    /// Endpoint for updating a bookmark.
    /// </summary>
    /// <param name="id">The bookmark to update's ID.</param>
    /// <param name="inputBookmark">The updated bookmark data.</param>
    /// <param name="db">The database storing bookmarks</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Update(int id, BookmarkEntity inputBookmark, BeagleWizardDb db)
    {
        var bookmark = await db.Bookmarks.FindAsync(id);

        if (bookmark is null)
            return TypedResults.NotFound();

        bookmark.Label = inputBookmark.Label;
        bookmark.Text = inputBookmark.Text;
        bookmark.Url = inputBookmark.Url;

        bookmark.Modified = DateTime.UtcNow;

        await db.SaveChangesAsync();

        return TypedResults.NoContent();
    }

    #endregion
}
