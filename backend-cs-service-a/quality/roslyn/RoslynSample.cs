// RoslynSample.cs — General Roslyn rule violations fixture
using System;
using System.IO;

namespace BackendCsServiceA.Quality.Roslyn
{
    public class RoslynSample
    {
        // Unused private field (IDE0051 / CA1823)
        private static int _unusedCounter = 42;

        public static string ProcessData(string input)
        {
            if (string.IsNullOrEmpty(input))
            {
                return string.Empty;
            }
            return input.Trim().ToUpperInvariant();
        }
    }
}
