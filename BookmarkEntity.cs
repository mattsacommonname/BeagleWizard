/// <summary>
/// Bookmark data entity.
/// </summary>
public class BookmarkEntity
{
    #region public properties

    /// <summary>
    /// Unique ID of the entity.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Entities creation date.
    /// </summary>
    /// <remarks>
    /// Ideally, this should never change after creation.
    /// </remarks>
    public DateTime Created { get; set; }

    /// <summary>
    /// Human-readable label.
    /// </summary>
    /// <remarks>
    /// This should be unique.
    /// </remarks>
    public string? Label { get; set; }

    /// <summary>
    /// Last modification of this entity.
    /// </summary>
    /// <remarks>
    /// Should not be user editable.
    /// </remarks>
    public DateTime Modified { get; set; }

    // public IEnumerable<string>? Tags { get; set; }

    /// <summary>
    /// User-defined description of the bookmark.
    /// </summary>
    public string? Text { get; set; }

    /// <summary>
    /// URL of the bookmark.
    /// </summary>
    public string? Url { get; set; }

    #endregion

    #region constructors

    /// <summary>
    /// Empty constructor.
    /// </summary>
    public BookmarkEntity() { }

    #endregion
}
