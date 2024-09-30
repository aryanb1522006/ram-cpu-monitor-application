
$cpuInfo = Get-CimInstance -ClassName Win32_Processor


$cpuInfo | ForEach-Object {
    Write-Host "Name: $($_.Name)"
    Write-Host "Manufacturer: $($_.Manufacturer)"
    Write-Host "Processor ID: $($_.ProcessorId)"
    Write-Host "Number of Cores: $($_.NumberOfCores)"
    Write-Host "Number of Logical Processors: $($_.NumberOfLogicalProcessors)"
    Write-Host "Max Clock Speed (MHz): $($_.MaxClockSpeed)"
    Write-Host "L2 Cache Size: $($_.L2CacheSize) KB"
    Write-Host "L3 Cache Size: $($_.L3CacheSize) KB"
    Write-Host "Socket Designation: $($_.SocketDesignation)"
    Write-Host "`n"  # Add a blank line between multiple CPUs if present
}
