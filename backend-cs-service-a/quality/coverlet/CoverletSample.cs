namespace BackendCsServiceA.Quality.Coverlet
{
    public class CoverletSample
    {
        public int CalculateTotal(int baseVal, int multiplier)
        {
            if (multiplier <= 0) return baseVal;
            return baseVal * multiplier;
        }
    }
}
