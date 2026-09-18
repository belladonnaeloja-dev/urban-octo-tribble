<#
.SYNOPSIS
    POST a local file to a Shopify staged-upload target (from stagedUploadsCreate).

.DESCRIPTION
    Step 2 of the template push in ../SKILL.md, Phase 6:
      1. stagedUploadsCreate (resource FILE, mimeType text/plain) -> url + parameters + resourceUrl
      2. THIS SCRIPT posts the file to that url as multipart/form-data, sending every
         signed parameter first and the file part LAST (Google Cloud Storage rejects the
         upload if the file part precedes the signed fields).
      3. themeFilesUpsert with body { type: URL, value: <resourceUrl> }

    The parameters are passed as a JSON file so nothing has to be hand-escaped. Save the
    stagedTargets[0] object from the mutation response verbatim, e.g.:

      {
        "url": "https://shopify-staged-uploads.storage.googleapis.com/",
        "resourceUrl": "https://shopify-staged-uploads.storage.googleapis.com/tmp/...",
        "parameters": [ { "name": "key", "value": "tmp/..." }, ... ]
      }

.PARAMETER FilePath
    The local template JSON (UTF-8, no BOM).

.PARAMETER TargetJson
    Path to the saved stagedTargets[0] JSON.

.EXAMPLE
    pwsh ./upload-staged.ps1 -FilePath .\product.pagepilot-XXXX.json -TargetJson .\staged-target.json

    Prints the resourceUrl on success; pass it to themeFilesUpsert.

.NOTES
    Requires PowerShell 7+ (Invoke-RestMethod -Form). Windows PowerShell 5.1 has no -Form,
    so it falls back to a manual multipart body via HttpClient.
    A non-Windows fallback with the same contract lives next to this file: upload-staged.py.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string] $FilePath,
    [Parameter(Mandatory = $true)] [string] $TargetJson
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $FilePath))   { throw "File not found: $FilePath" }
if (-not (Test-Path -LiteralPath $TargetJson)) { throw "Target JSON not found: $TargetJson" }

$target = Get-Content -LiteralPath $TargetJson -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $target.url -or -not $target.parameters) {
    throw "TargetJson must contain 'url' and 'parameters' (save stagedTargets[0] verbatim)."
}

$fileInfo = Get-Item -LiteralPath $FilePath
$fileName = ($target.parameters | Where-Object { $_.name -eq 'key' } | Select-Object -First 1).value
if ($fileName) { $fileName = Split-Path -Leaf $fileName } else { $fileName = $fileInfo.Name }

Write-Host "Uploading $($fileInfo.Name) ($($fileInfo.Length) bytes) to $($target.url)"

if ($PSVersionTable.PSVersion.Major -ge 7) {
    # Ordered dictionary: signed fields first, file last.
    $form = [ordered]@{}
    foreach ($p in $target.parameters) { $form[$p.name] = [string]$p.value }
    $form['file'] = $fileInfo
    $null = Invoke-RestMethod -Uri $target.url -Method Post -Form $form
} else {
    Add-Type -AssemblyName System.Net.Http
    $client  = New-Object System.Net.Http.HttpClient
    $content = New-Object System.Net.Http.MultipartFormDataContent
    foreach ($p in $target.parameters) {
        $content.Add((New-Object System.Net.Http.StringContent([string]$p.value)), $p.name)
    }
    $bytes = [System.IO.File]::ReadAllBytes($fileInfo.FullName)
    $fileContent = New-Object System.Net.Http.ByteArrayContent(, $bytes)
    $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('text/plain')
    $content.Add($fileContent, 'file', $fileName)
    $resp = $client.PostAsync($target.url, $content).Result
    if (-not $resp.IsSuccessStatusCode) {
        $body = $resp.Content.ReadAsStringAsync().Result
        throw "Upload failed: $([int]$resp.StatusCode) $($resp.ReasonPhrase)`n$body"
    }
}

# Local MD5 so it can be compared with checksumMd5 from the theme file read-back.
$md5 = (Get-FileHash -LiteralPath $FilePath -Algorithm MD5).Hash.ToLower()
Write-Host "Upload OK. local size=$($fileInfo.Length) local md5=$md5"
Write-Host "resourceUrl:"
Write-Output $target.resourceUrl
