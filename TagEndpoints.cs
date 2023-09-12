#region usings

using static Microsoft.AspNetCore.Http.TypedResults;

#endregion

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
    /// Endpoint mapping tuple.
    /// </summary>
    public static readonly (string prefix, Action<IEndpointRouteBuilder>) Mapping = (Prefix, Map);

    /// <summary>
    /// Suggested URL path prefix.
    /// </summary>
    public const string Prefix = "/t";

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
            return Problem("Failed to get tag read path");

        return Created(uri, inputTag);
    }

    #endregion

    #region delete methods & constants

    /// <summary>
    /// Name for delete endpoint.
    /// </summary>
    public const string DeleteName = $"{BaseName}.{nameof(Delete)}";

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
            return NotFound();

        db.Tags.Remove(tag);
        await db.SaveChangesAsync();

        return Ok(tag);
    }

    #endregion

    #region route mapping

    /// <summary>
    /// Maps the tag endpoints to routes.
    /// </summary>
    /// <param name="routeBuilder">Route builder to map with.</param>
    public static void Map(IEndpointRouteBuilder routeBuilder)
    {
        routeBuilder.MapDelete(IdPath, Delete)
            .WithName(DeleteName);
        routeBuilder.MapGet(IdPath, Read)
            .WithName(ReadName);
        routeBuilder.MapGet(RootPath, ReadAll)
            .WithName(ReadAllName);
        routeBuilder.MapPost(RootPath, Create)
            .WithName(CreateName);
        routeBuilder.MapPut(IdPath, Update)
            .WithName(UpdateName);
    }

    #endregion

    #region read methods & constants

    /// <summary>
    /// Name for individual tag Read endpoint.
    /// </summary>
    public const string ReadName = $"{BaseName}.{nameof(Read)}";

    /// <summary>
    /// Endpoint for Reading an individual tag.
    /// </summary>
    /// <param name="id">The tag to read's ID.</param>
    /// <param name="db">The database storing tags.</param>
    /// <returns>HTTP response.</returns>
    public static async Task<IResult> Read(int id, BeagleWizardDb db)
        => await db.Tags.FindAsync(id) is TagEntity b ? Ok(b) : NotFound();

    /// <summary>
    /// Name for Read all endpoint.
    /// </summary>
    public const string ReadAllName = $"{BaseName}.{nameof(ReadAll)}";

    /// <summary>
    /// Endpoint for Reading all tags.
    /// </summary>
    /// <param name="db">The database storing tags.</param>
    /// <returns>HTTP response.</returns>
    public static IResult ReadAll(BeagleWizardDb db) => Ok(db.Tags);

    #endregion

    #region update methods & constants

    /// <summary>
    /// Name for Update endpoint.
    /// </summary>
    public const string UpdateName = $"{BaseName}.{nameof(Update)}";

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
            return NotFound();

        tag.Label = inputTag.Label;

        await db.SaveChangesAsync();

        return NoContent();
    }

    #endregion
}
