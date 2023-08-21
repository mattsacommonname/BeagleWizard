#region usings

using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

#endregion

/// <summary>
/// Bookmark data entity.
/// </summary>
[Table("Bookmarks")]
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
    [Required]
    public DateTime Created { get; set; }

    /// <summary>
    /// Human-readable label.
    /// </summary>
    /// <remarks>
    /// This should be unique.
    /// </remarks>
    [Required]
    [StringLength(512)]
    public string Label { get; set; } = null!;

    /// <summary>
    /// Last modification of this entity.
    /// </summary>
    /// <remarks>
    /// Should not be user editable.
    /// </remarks>
    [Required]
    public DateTime Modified { get; set; }

    // public IEnumerable<string>? Tags { get; set; }

    /// <summary>
    /// User-defined description of the bookmark.
    /// </summary>
    [StringLength(4096)]
    public string? Text { get; set; }

    /// <summary>
    /// URL of the bookmark.
    /// </summary>
    [Required]
    [StringLength(2048)]
    public string Url { get; set; } = null!;

    #endregion
}
