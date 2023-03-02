/// <summary>
/// Tag endpoints.
/// </summary>
public static class TagEndpoints
{
    #region shared constants

    /// <summary>
    /// Base name for route naming.
    /// </summary>
    public const string BaseName = "Tag";

    /// <summary>
    /// Common root path.
    /// </summary>
    private const string RootPath = "/";

    /// <summary>
    /// Common ID'd path.
    /// </summary>
    private const string IdPath = "/{id}";

    #endregion

    #region create methods & constants

    /// <summary>
    /// Name for Create endpoint.
    /// </summary>
    public const string CreateName = $"{BaseName}.{nameof(Create)}";

    /// <summary>
    /// Relative path for Create endpoint.
    /// </summary>
    public const string CreatePath = RootPath;

    /// <summary>
    /// Endpoint for creating a tag.
    /// </summary>
    /// <param name="inputBookmark">The new tag data.</param>
    /// <param name="db">The database storing tags.</param>
    /// <param name="linker">The link generator to for determining other endpoint routes.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Create(TagEntity inputTag, BeagleWizardDb db, LinkGenerator linker)
    {
        db.Tags.Add(inputTag);
        await db.SaveChangesAsync();

        var uri = linker.GetPathByName(ReadName, new { id = inputTag.Id });
        if(uri is null)
            return TypedResults.Problem("Failed to get tag read path");

        return TypedResults.Created(uri, inputTag);
    }

    #endregion

    #region delete methods & constants

    /// <summary>
    /// Name for delete endpoint.
    /// </summary>
    public const string DeleteName = $"{BaseName}.{nameof(Delete)}";

    /// <summary>
    /// Relative path for delete endpoint.
    /// </summary>
    public const string DeletePath = IdPath;

    /// <summary>
    /// Endpoint for deleting a tag.
    /// </summary>
    /// <param name="id">The tag to delete's ID.</param>
    /// <param name="db">The database storing tags.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Delete(int id, BeagleWizardDb db)
    {
        var tag = await db.Tags.FindAsync(id);
        if (tag is null)
            return TypedResults.NotFound();

        db.Tags.Remove(tag);
        await db.SaveChangesAsync();

        return TypedResults.Ok(tag);
    }

    #endregion

    #region route mapping

    /// <summary>
    /// Maps the tag endpoints to routes.
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

    #region read methods & constants

    /// <summary>
    /// Name for individual tag Read endpoint.
    /// </summary>
    public const string ReadName = $"{BaseName}.{nameof(Read)}";

    /// <summary>
    /// Relative path for Read endpoint.
    /// </summary>
    public const string ReadPath = IdPath;

    /// <summary>
    /// Endpoint for Reading an individual tag.
    /// </summary>
    /// <param name="id">The tag to read's ID.</param>
    /// <param name="db">The database storing tags.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Read(int id, BeagleWizardDb db)
        => await db.Tags.FindAsync(id) is TagEntity b ? TypedResults.Ok(b) : TypedResults.NotFound();

    /// <summary>
    /// Name for Read all endpoint.
    /// </summary>
    public const string ReadAllName = $"{BaseName}.{nameof(ReadAll)}";

    /// <summary>
    /// Relative path for Read all endpoint.
    /// </summary>
    public const string ReadAllPath = RootPath;

    /// <summary>
    /// Endpoint for Reading all tags.
    /// </summary>
    /// <param name="db">The database storing tags.</param>
    /// <returns>HTTP response.</returns>
    public static IResult ReadAll(BeagleWizardDb db) => TypedResults.Ok(db.Tags);

    #endregion

    #region update methods & constants

    /// <summary>
    /// Name for Update endpoint.
    /// </summary>
    public const string UpdateName = $"{BaseName}.{nameof(Update)}";

    /// <summary>
    /// Relative path for Update endpoint.
    /// </summary>
    public const string UpdatePath = IdPath;

    /// <summary>
    /// Endpoint for updating a tag.
    /// </summary>
    /// <param name="id">The tag to update's ID.</param>
    /// <param name="inputBookmark">The updated tag data.</param>
    /// <param name="db">The database storing tags.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Update(int id, TagEntity inputTag, BeagleWizardDb db)
    {
        var tag = await db.Tags.FindAsync(id);

        if (tag is null)
            return TypedResults.NotFound();

        tag.Label = inputTag.Label;

        await db.SaveChangesAsync();

        return TypedResults.NoContent();
    }

    #endregion
}
