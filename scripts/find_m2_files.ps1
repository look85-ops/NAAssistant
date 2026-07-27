# Find M2 AOS files
$desktop = 'C:\Users\marcenuk\Desktop'
$items = Get-ChildItem -Path $desktop

foreach ($dir in $items) {
    if ($dir.Attributes -match 'Directory') {
        $name = $dir.Name
        if ($name -match "M2|х�� _��|Rating|AOС|Academ") {
            Write-Host "Directory: $name"
            Write-Host "Path: $($dir.FullName)"
            
            # Get all files recursively
            $allFiles = Get-ChildItem -Path $dir.FullName -Recurse -File
            $xlsFiles = $allFiles | Where-Object { $_.Name.EndsWith('.xlsx') }
            
            foreach ($file in $xlsFiles) {
                Write-Host "  XLSX: $($file.Name)" -ForegroundColor Yellow
                
                # Check if it's the M2 AOS file we're looking for
                if ($file.Name.Contains('AOS') -and $file.Name.Contains('M2') -or 
                    $file.Name.Contains('AOС') -and $file.Name.Contains('M2')) {
                    Write-Host "  <<< TARGET FILE FOUND! $($file.FullName)" -ForegroundColor Green
                }
            }
            Write-Host ""
        }
    }
}
