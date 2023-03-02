/// <summary>
/// Tag data entity.
/// </summary>
public class TagEntity
{
    #region public properties

    /// <summary>
    /// Unique identifier.
    /// </summary>
    public int Id { get; set; }

    /// <summary>
    /// Tag's label.
    /// </summary>
    /// <remarks>
    /// Should be unique.
    /// </remarks>
    public string? Label { get; set; }

    #endregion

    #region constructors

    /// <summary>
    /// Empty constructor.
    /// </summary>
    public TagEntity() { }

    #endregion
}
