
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoFalse
$presentation = $ppt.Presentations.Open("D:\Download\RR Auction\SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx", [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)

$outDir = "D:\Download\RR Auction\ppt_slides_check"
if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$presentation.Slides.Item(8).Export("$outDir\slide_08.png", "PNG", 1920, 1080)
$presentation.Slides.Item(9).Export("$outDir\slide_09.png", "PNG", 1920, 1080)
$presentation.Slides.Item(10).Export("$outDir\slide_10.png", "PNG", 1920, 1080)
$presentation.Slides.Item(11).Export("$outDir\slide_11.png", "PNG", 1920, 1080)
$presentation.Slides.Item(14).Export("$outDir\slide_14.png", "PNG", 1920, 1080)

$presentation.Close()
$ppt.Quit()
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "Export completed successfully"
