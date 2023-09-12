#region usings

using Microsoft.AspNetCore.Routing;
using Mapper = System.Action<Microsoft.AspNetCore.Routing.IEndpointRouteBuilder>;

#endregion

/// <summary>
/// <see cref="IEndpointRouteBuilder"/> extension methods.
/// </summary>
public static class IEndpointRouteBuilderExtensions
{
    #region extension methods

    /// <summary>
    /// Maps Beagle Wizard endpoints.
    /// </summary>
    /// <param name="builder">this</param>
    /// <param name="mappings">The endpoint prefix url and mapping function tuple.</param>
    /// <returns><paramref name="builder">, for the fluency.</returns>
    public static IEndpointRouteBuilder MapEndpoints(
        this IEndpointRouteBuilder builder, params (string prefix, Mapper mapper)[] mappings)
    {
        foreach(var (prefix, mapper) in mappings)
        {
            var group = builder.MapGroup(prefix);
            mapper(group);
        }

        return builder;
    }

    #endregion
}
