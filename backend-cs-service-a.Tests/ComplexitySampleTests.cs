using BackendCsServiceA.Analysis;
using Xunit;

namespace BackendCsServiceA.Tests;

/// <summary>
/// Tests for <see cref="ComplexitySample.ProcessComplexRules"/>.
/// Covers all 8 branch decision outcomes + loop boundaries.
///
/// Metrics targeted:
///   ✅ Statement Coverage %       — every line executed
///   ✅ Branch Coverage %          — all if/else branches taken
///   ✅ Path Coverage %            — nested condition paths
///   ✅ Mutation Kill Rate %       — specific asserts kill arithmetic mutants
///   ✅ All-Uses Coverage %        — score: defined → used in += → returned
///   ✅ Loop Condition Testing     — quantity 0 / 1 / even / odd
/// </summary>
public class ComplexitySampleTests
{
    // ── Inactive path ─────────────────────────────────────────────────────
    [Fact]
    public void Inactive_Returns_MinusOne()
    {
        // Branch: is_active=false → score = -1
        int result = ComplexitySample.ProcessComplexRules(1, "gold", false, 0);
        Assert.Equal(-1, result);
    }

    [Fact]
    public void Inactive_IgnoresTierAndQuantity()
    {
        int result = ComplexitySample.ProcessComplexRules(2, "silver", false, 10);
        Assert.Equal(-1, result);
    }

    // ── Gold + Category 1 ─────────────────────────────────────────────────
    [Fact]
    public void Gold_Category1_NoQuantity_Returns50()
    {
        int result = ComplexitySample.ProcessComplexRules(1, "gold", true, 0);
        Assert.Equal(50, result);
    }

    [Fact]
    public void Gold_Category1_Quantity1_Returns52()
    {
        // Loop: i=0 (even) → +2 → total 52
        int result = ComplexitySample.ProcessComplexRules(1, "gold", true, 1);
        Assert.Equal(52, result);
    }

    [Fact]
    public void Gold_Category1_Quantity4_Returns56()
    {
        // i=0,2 → +2 each (+4); i=1,3 → +1 each (+2) → 50+6=56
        int result = ComplexitySample.ProcessComplexRules(1, "gold", true, 4);
        Assert.Equal(56, result);
    }

    [Fact]
    public void Gold_Category1_Quantity3_Returns55()
    {
        // i=0→+2, i=1→+1, i=2→+2 → 50+5=55
        int result = ComplexitySample.ProcessComplexRules(1, "gold", true, 3);
        Assert.Equal(55, result);
    }

    // ── Gold + Category 2 ─────────────────────────────────────────────────
    [Fact]
    public void Gold_Category2_NoQuantity_Returns40()
    {
        int result = ComplexitySample.ProcessComplexRules(2, "gold", true, 0);
        Assert.Equal(40, result);
    }

    // ── Gold + Category Other (else branch) ───────────────────────────────
    [Fact]
    public void Gold_CategoryOther_NoQuantity_Returns30()
    {
        int result = ComplexitySample.ProcessComplexRules(3, "gold", true, 0);
        Assert.Equal(30, result);
    }

    // ── Silver + Category 1 ───────────────────────────────────────────────
    [Fact]
    public void Silver_Category1_NoQuantity_Returns25()
    {
        int result = ComplexitySample.ProcessComplexRules(1, "silver", true, 0);
        Assert.Equal(25, result);
    }

    [Fact]
    public void Silver_Category1_Quantity2_Returns28()
    {
        // 25 + (i=0→+2, i=1→+1) = 28
        int result = ComplexitySample.ProcessComplexRules(1, "silver", true, 2);
        Assert.Equal(28, result);
    }

    // ── Silver + Category Other ────────────────────────────────────────────
    [Fact]
    public void Silver_CategoryOther_NoQuantity_Returns15()
    {
        int result = ComplexitySample.ProcessComplexRules(5, "silver", true, 0);
        Assert.Equal(15, result);
    }

    // ── Bronze (else) tier ────────────────────────────────────────────────
    [Fact]
    public void Bronze_NoQuantity_Returns5()
    {
        int result = ComplexitySample.ProcessComplexRules(1, "bronze", true, 0);
        Assert.Equal(5, result);
    }

    [Fact]
    public void Bronze_Quantity2_Returns8()
    {
        // 5 + (i=0→+2, i=1→+1) = 8
        int result = ComplexitySample.ProcessComplexRules(1, "bronze", true, 2);
        Assert.Equal(8, result);
    }

    // ── Large quantity (boundary test) ────────────────────────────────────
    [Fact]
    public void Gold_Category1_Quantity10_Returns65()
    {
        // 5 even × +2 = 10; 5 odd × +1 = 5 → 50+15=65
        int result = ComplexitySample.ProcessComplexRules(1, "gold", true, 10);
        Assert.Equal(65, result);
    }
}
