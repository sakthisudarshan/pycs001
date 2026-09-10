// trigger.cs — OpenTelemetry runner verification
using System;
using System.Diagnostics;
using System.Threading.Tasks;

namespace BackendCsServiceA.Quality.OpenTelemetry
{
    public class Trigger
    {
        public static async Task<int> RunAsync(string[]? args = null)
        {
            Console.WriteLine("=== [OpenTelemetry] C# Tracing & Metrics Verification ===");

            using var listener = new ActivityListener
            {
                ShouldListenTo = s => s.Name == "BackendCsServiceA.Tracer",
                Sample = (ref ActivityCreationOptions<ActivityContext> _) => ActivitySamplingResult.AllDataAndRecorded,
                ActivityStarted = a => Console.WriteLine($"[Trace Start] {a.OperationName} (TraceId={a.TraceId})"),
                ActivityStopped = a => Console.WriteLine($"[Trace Stop]  {a.OperationName} (Duration={a.Duration.TotalMilliseconds}ms)")
            };
            ActivitySource.AddActivityListener(listener);

            string result = await OpenTelemetryFixture.ExecuteTracedOperationAsync("HandleRecordEvent", "rec-001");
            Console.WriteLine($"Result: {result}");

            Console.WriteLine("=== OpenTelemetry verification successful ===");
            return 0;
        }
    }
}
