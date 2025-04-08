param(
    [switch]$Verbose,  # Flag for verbose mode
    [switch]$Silent,   # Flag for silent mode
    [string]$RelativeIcoPath  # Relative path to the ico directory from the project root
)

# Ensure $RelativeIcoPath has a default value if not provided
if (-not $RelativeIcoPath) {
    $RelativeIcoPath = "media\\media-ico\\"  # Set default value
}

#Write-Host "RelativeIcoPath:" $RelativeIcoPath  # Debugging line


# Determine verbosity
$SilentMode = $Silent
$VerboseMode = $Verbose -and -not $Silent

# Define directories
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)  # Go up an additional level
$ProjectDirName = Split-Path -Leaf $ProjectDir  # Extract project directory name

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

# Function to resolve absolute icon paths
function Resolve-IconPath {
    param (
        [string]$Filename
    )
    # Return the absolute path for IconResource
    return "$ProjectDir\$RelativeIcoPath$Filename"
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
        $AbsoluteIconPath = ""    # Absolute path for IconResource assignment
        $RelativeIconPath = ""    # Relative path for logging
        foreach ($Line in $FileContent) {
            if ($Line -like "IconResource=*") {
                $ExistingFilename = Split-Path -Leaf ($Line -replace "IconResource=", "")
                $CurrentIconFilename = $ExistingFilename  # Store the current icon filename
                $AbsoluteIconPath = Resolve-IconPath -Filename $ExistingFilename  # Absolute path for IconResource
                #Write-Host "AbsoluteIconPath:" $AbsoluteIconPath
                $RelativeIconPath = Convert-ToRelativePath -AbsolutePath $AbsoluteIconPath  # Relative path for logs
                #Write-Host "RelativeIconPath:" $RelativeIconPath
                if ($Line -ne "IconResource=$AbsoluteIconPath") {
                    # Only update if the new path is different
                    $UpdatedLines += "IconResource=$AbsoluteIconPath"
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