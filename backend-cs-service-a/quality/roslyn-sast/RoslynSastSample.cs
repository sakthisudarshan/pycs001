// RoslynSastSample.cs — SAST rule violation fixtures for Roslyn / SecurityCodeScan
using System;
using System.Data;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace BackendCsServiceA.Quality.RoslynSast
{
    public class RoslynSastSample
    {
        // SCS0015: Hardcoded secret/password
        private const string AdminPassword = "SuperSecretPassword123!";
        private const string ApiKey = "AKIAIOSFODNN7EXAMPLE";

        // SCS0006: Weak hashing algorithm (MD5 / SHA1)
        public static string ComputeWeakHash(string input)
        {
#pragma warning disable CA5350, CA5351
            using var md5 = MD5.Create();
            byte[] hash = md5.ComputeHash(Encoding.UTF8.GetBytes(input));
            return BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant();
#pragma warning restore CA5350, CA5351
        }

        // SCS0006: Weak hashing with SHA1
        public static string ComputeSha1Hash(string input)
        {
#pragma warning disable CA5350
            using var sha1 = SHA1.Create();
            byte[] hash = sha1.ComputeHash(Encoding.UTF8.GetBytes(input));
            return Convert.ToBase64String(hash);
#pragma warning restore CA5350
        }

        // SCS0002: Potential SQL injection / unvalidated input
        public static string BuildDynamicSqlQuery(string tableName, string userInput)
        {
            // Direct concatenation vulnerability
            return $"SELECT * FROM {tableName} WHERE username = '{userInput}'";
        }

        // SCS0018: Path traversal vulnerability
        public static string ReadUserFile(string basePath, string userFilename)
        {
            string fullPath = Path.Combine(basePath, userFilename);
            if (File.Exists(fullPath))
            {
                return File.ReadAllText(fullPath);
            }
            return string.Empty;
        }

        // SCS0005: Weak random number generator for cryptographic context
        public static int GenerateInsecureToken()
        {
            var rnd = new Random();
            return rnd.Next(100000, 999999);
        }
    }
}
