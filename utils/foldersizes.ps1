$folderPath = "C:\Users\user\Documents\dev\dissertation25\"
Get-ChildItem -Directory -Path $folderPath | ForEach-Object {
    $folder = $_
    $size = (Get-ChildItem -Recurse -Path $folder.FullName | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{
        FolderName = $folder.Name
        SizeInBytes = $size
        SizeInMB = "{0:N2}" -f ($size / 1MB)
    }
} | Format-Table -AutoSize