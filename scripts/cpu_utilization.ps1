# Get the CPU utilization percentage using Get-Counter
$cpuUsage = Get-Counter '\Processor(_Total)\% Processor Time'

# Extract the CPU utilization percentage and output only the numeric value
$cpuUsageValue = $cpuUsage.CounterSamples.CookedValue
Write-Host $cpuUsageValue  # Output the numeric value directly