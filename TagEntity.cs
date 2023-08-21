#region  usings

using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

#endregion

/// <summary>
/// Tag data entity.
/// </summary>
[Table("Tags")]
[Index(nameof(Label), IsUnique = true)]
public class TagEntity
{
    #region public properties

    /// <summary>
    /// Unique identifier.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Associated bookmarks.
    /// </summary>
    [JsonIgnore]
    public ICollection<BookmarkEntity>? Bookmarks { get; set; }

    /// <summary>
    /// Tag's label.
    /// </summary>
    [Required]
    [StringLength(64)]
    public string Label { get; set; } = null!;

    #endregion
}
