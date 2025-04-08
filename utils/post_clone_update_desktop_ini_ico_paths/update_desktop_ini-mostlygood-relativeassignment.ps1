param(
    [switch]$Verbose,  # Flag for verbose mode
    [switch]$Silent    # Flag for silent mode
)

# Determine verbosity
$SilentMode = $Silent
$VerboseMode = $Verbose -and -not $Silent

# Define directories
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
#$ProjectDir = Split-Path -Parent $ScriptDir
$ProjectDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)  # Go up an additional level
$ProjectDirName = Split-Path -Leaf $ProjectDir  # Extract project directory name
Write-Host "ProjectDirName:" $ProjectDirName
# Function to convert absolute paths to project-relative paths including root directory
function Convert-ToRelativePath {
    param (
        [string]$AbsolutePath
    )
    if ($AbsolutePath -like "$ProjectDir*") {
        $RelativePath = $AbsolutePath.Substring($ProjectDir.Length).TrimStart('\')
        return ".\$ProjectDirName\$RelativePath"
    } else {
        return $AbsolutePath
    }
}

# Function to resolve icon paths
function Resolve-IconPath {
    param (
        [string]$Filename
    )
    return ".\$ProjectDirName\media\media-ico\$Filename"
}

# Find all desktop.ini files
$DesktopIniFiles = Get-ChildItem $ProjectDir -Recurse -Filter "desktop.ini" -Force

if ($DesktopIniFiles.Count -eq 0) {
    if ($VerboseMode) { Write-Host "No desktop.ini files found." }
    Exit 0
}

foreach ($File in $DesktopIniFiles) {
    $DesktopIniPath = $File.FullName
    $RelativeDesktopIniPath = Convert-ToRelativePath -AbsolutePath $DesktopIniPath

    try {
        # Read content
        $FileContent = Get-Content $DesktopIniPath

        # Update paths
        $UpdatedLines = @()
        $Changed = $false
        $CurrentIconFilename = ""  # Variable to store the current icon filename
        $RelativeIconPath = ""    # Variable for relative icon path
        foreach ($Line in $FileContent) {
            if ($Line -like "IconResource=*") {
                $ExistingFilename = Split-Path -Leaf ($Line -replace "IconResource=", "")
                $CurrentIconFilename = $ExistingFilename  # Store the current icon filename
                $NewRelativePath = Resolve-IconPath -Filename $ExistingFilename
                $RelativeIconPath = Convert-ToRelativePath -AbsolutePath $NewRelativePath

                if ($Line -ne "IconResource=$NewRelativePath") {
                    # Only update if the new path is different
                    $UpdatedLines += "IconResource=$NewRelativePath"
                    $Changed = $true
                } else {
                    $UpdatedLines += $Line
                }
            } else {
                $UpdatedLines += $Line
            }
        }

        # Write changes if any
        if ($Changed) {
            Set-Content $DesktopIniPath -Value $UpdatedLines -Force
            if ($VerboseMode) {
                Write-Host "$RelativeDesktopIniPath -> $RelativeIconPath"
            }
        } else {
            if ($VerboseMode) {
                Write-Host "$RelativeDesktopIniPath ~ $RelativeIconPath"
            }
        }
    } catch {
        if ($VerboseMode) {
            Write-Error "Failed: $RelativeDesktopIniPath, Error: $($_.Exception.Message)"
        }
    }
}