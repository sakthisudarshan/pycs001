// OpenTelemetryFixture.cs — OpenTelemetry distributed tracing and metrics fixture for C# .NET 8.0
using System;
using System.Diagnostics;
using System.Diagnostics.Metrics;
using System.Threading.Tasks;

namespace BackendCsServiceA.Quality.OpenTelemetry
{
    public class OpenTelemetryFixture
    {
        // ActivitySource for distributed tracing (OpenTelemetry specification)
        public static readonly ActivitySource ActivitySource = new ActivitySource(
            "BackendCsServiceA.Tracer",
            "1.0.0"
        );

        // Meter for OpenTelemetry metrics instrumentation
        public static readonly Meter Meter = new Meter(
            "BackendCsServiceA.Metrics",
            "1.0.0"
        );

        private static readonly Counter<long> RequestCounter = Meter.CreateCounter<long>(
            "http.server.requests",
            description: "Count of incoming requests processed"
        );

        private static readonly Histogram<double> LatencyHistogram = Meter.CreateHistogram<double>(
            "http.server.duration",
            unit: "ms",
            description: "Request latency in milliseconds"
        );

        public static async Task<string> ExecuteTracedOperationAsync(string operationName, string recordId)
        {
            using Activity? activity = ActivitySource.StartActivity(
                operationName,
                ActivityKind.Server
            );

            activity?.SetTag("record.id", recordId);
            activity?.SetTag("service.name", "backend-cs-service-a");
            activity?.SetTag("telemetry.sdk.language", "dotnet");

            RequestCounter.Add(1, new System.Collections.Generic.KeyValuePair<string, object?>("operation", operationName));

            var sw = Stopwatch.StartNew();
            try
            {
                activity?.AddEvent(new ActivityEvent("operation.started"));
                await Task.Delay(10); // Simulated async work
                activity?.AddEvent(new ActivityEvent("operation.completed"));
                activity?.SetStatus(ActivityStatusCode.Ok);
                return $"Processed record {recordId} under trace {activity?.TraceId}";
            }
            catch (Exception ex)
            {
                activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
                activity?.AddEvent(new ActivityEvent("exception", tags: new ActivityTagsCollection { { "exception.message", ex.Message } }));
                throw;
            }
            finally
            {
                sw.Stop();
                LatencyHistogram.Record(sw.Elapsed.TotalMilliseconds);
            }
        }
    }
}
