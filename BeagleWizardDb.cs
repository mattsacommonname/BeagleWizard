#region usings

using Microsoft.EntityFrameworkCore;

#endregion

/// <summary>
/// Bookmark database
/// </summary>
public class BeagleWizardDb : DbContext
{
    #region constructors

    /// <summary>
    /// Constructor
    /// </summary>
    /// <param name="options">Database options</param>
    public BeagleWizardDb(DbContextOptions<BeagleWizardDb> options)
    : base(options) { }

    #endregion

    #region public properties

    /// <summary>
    /// Bookmarks.
    /// </summary>
    public DbSet<BookmarkEntity> Bookmarks => this.Set<BookmarkEntity>();

    /// <summary>
    /// Tags.
    /// </summary>
    public DbSet<TagEntity> Tags => this.Set<TagEntity>();

    #endregion
}
