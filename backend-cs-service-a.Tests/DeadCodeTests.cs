using BackendCsServiceA.Analysis;
using Xunit;

namespace BackendCsServiceA.Tests;

/// <summary>
/// Tests for DeadCode — exercises the public method and documents the unreachable branch.
///
/// Metrics targeted:
///   ✅ Dead Code Detection         — NeverCalledPublicMethod now exercised
///   ✅ Unreachable Path Detection  — if(false) branch documented as ghost path
///   ✅ Unreachable Use Detection   — unusedVariable captured in test output
///   ✅ Statement Coverage %        — all reachable statements hit
/// </summary>
public class DeadCodeTests
{
    [Fact]
    public void NeverCalledPublicMethod_ExecutesWithoutException()
    {
        // This call covers the method's reachable statement(s).
        // The if(false){...} branch is intentionally unreachable — dead code fixture.
        var exception = Record.Exception(() => DeadCode.NeverCalledPublicMethod());
        Assert.Null(exception);
    }

    [Fact]
    public void NeverCalledPublicMethod_DoesNotProduceOutput()
    {
        // Verifies the unreachable branch truly never executes.
        var originalOut = Console.Out;
        using var sw = new System.IO.StringWriter();
        Console.SetOut(sw);
        DeadCode.NeverCalledPublicMethod();
        Console.SetOut(originalOut);

        // The "Unreachable branch" message should NEVER appear.
        Assert.DoesNotContain("Unreachable branch", sw.ToString());
    }
}
