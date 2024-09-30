# Get total physical memory (RAM) in MB
$totalMemory = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory / 1MB

# Get available physical memory (RAM) in MB
$availableMemory = (Get-CimInstance -ClassName Win32_OperatingSystem).FreePhysicalMemory / 1KB

# Calculate used memory
$usedMemory = $totalMemory - $availableMemory

# Calculate memory usage percentage
$memoryUsagePercentage = ($usedMemory / $totalMemory) * 100

# Display memory details

Write-Host "$([math]::round($memoryUsagePercentage, 2))"
