$msg = "Launching IDLE"
try{
	$idle = "poetry run python -m idlelib.idle"
} catch {
	$idle = "python -m idlelib.idle"
} finally{
	Write-Host $idle
	Write-Host $msg
	Invoke-Expression $idle
}