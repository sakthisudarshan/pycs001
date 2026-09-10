# OpenTelemetry Quality Fixture — C# (.NET 8.0)

Distributed tracing, metric instrumentation, and span creation verification using .NET 8.0 `System.Diagnostics.ActivitySource` and `System.Diagnostics.Metrics` (OpenTelemetry specification).

## Trigger Details
- **Tool**: `opentelemetry`
- **Language**: `csharp`
- **Version**: `net8.0`
- **Target Files**: `OpenTelemetryFixture.cs`, `trigger.cs`
- **Run Command**: `bash run_opentelemetry.sh`
- **Metrics Covered**:
  - Trace Instrumentation Coverage
  - Span Creation Validation
  - Activity Source Tracking
  - Telemetry Exporter Health
