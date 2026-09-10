# Roslyn SAST Quality Fixture

Static Application Security Testing (SAST) analyzer fixture for C# (.NET 8.0) using Roslyn Analyzers and SecurityCodeScan.VS2019.

## Trigger Details
- **Tool**: `roslyn-sast` / `SecurityCodeScan`
- **Target Files**: `RoslynSastSample.cs`
- **Rules Detected**: SCS0002 (SQL Injection), SCS0006 (Weak Hashing), SCS0015 (Hardcoded Password), SCS0018 (Path Traversal)
- **Run Command**: `bash run_roslyn.sh`
