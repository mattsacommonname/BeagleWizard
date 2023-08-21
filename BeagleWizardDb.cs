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

    #region DbContext overrides

    /// <summary>
    /// Configuration of entity models for a <see cref="BeagleWizardDb" /> <see cref="DbContext" />.
    /// </summary>
    /// <param name="modelBuilder"></param>
    /// <remarks>
    /// Defines the <see cref="BookmarkEntity" />-to-<see cref="TagEntity" /> many-to-many relationship.
    /// </remarks>
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<BookmarkEntity>()
            .HasMany(bookmark => bookmark.Tags)
            .WithMany(tag => tag.Bookmarks)
            .UsingEntity(builder => builder.ToTable("BookmarkTags"));
    }

    #endregion
}
