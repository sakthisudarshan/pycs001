namespace BackendCsServiceA.Quality.Semgrep
{
    public class SemgrepSample
    {
        public string SanitizeInput(string rawInput)
        {
            if (string.IsNullOrEmpty(rawInput)) return string.Empty;
            return rawInput.Trim().Replace("'", "");
        }
    }
}
