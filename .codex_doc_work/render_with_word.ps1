param(
    [Parameter(Mandatory = $true)][string]$InputDocx,
    [Parameter(Mandatory = $true)][string]$OutputPdf
)

$wordApp = $null
$document = $null
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    $document = $wordApp.Documents.Open($InputDocx, $false, $true)
    foreach ($field in $document.Fields) {
        [void]$field.Update()
    }
    $document.ExportAsFixedFormat($OutputPdf, 17)
}
finally {
    if ($null -ne $document) {
        $document.Close(0)
    }
    if ($null -ne $wordApp) {
        $wordApp.Quit()
    }
    if ($null -ne $document) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($document)
    }
    if ($null -ne $wordApp) {
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
