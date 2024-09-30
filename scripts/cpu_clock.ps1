$MaxClockSpeed = (Get-CimInstance CIM_Processor).MaxClockSpeed
$ProcessorPerformance = (Get-Counter -Counter "\Processor Information(_Total)\% Processor Performance").CounterSamples.CookedValue
$CurrentClockSpeed = $MaxClockSpeed*($ProcessorPerformance/100)

Write-Host "Current Processor Speed: " -ForegroundColor Yellow -NoNewLine
Write-Host $CurrentClockSpeed