param([Parameter(Mandatory=$true)][string]$InputPath,[Parameter(Mandatory=$true)][string]$PdfPath)
$taskWord=$null
$taskDoc=$null
try {
    $taskWord=New-Object -ComObject Word.Application
    $taskWord.Visible=$false
    $taskWord.DisplayAlerts=0
    $taskWord.AutomationSecurity=3
    $taskDoc=$taskWord.Documents.Open($InputPath,$false,$true,$false)
    $taskDoc.Repaginate()
    $taskDoc.ExportAsFixedFormat($PdfPath,17)
    Write-Output ('Pages: '+$taskDoc.ComputeStatistics(2))
} finally {
    if ($null -ne $taskDoc) {
        $taskDoc.Close(0)
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($taskDoc) | Out-Null
    }
    if ($null -ne $taskWord) {
        $taskWord.Quit()
        [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($taskWord) | Out-Null
    }
}
