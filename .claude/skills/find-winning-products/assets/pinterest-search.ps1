<#
.SYNOPSIS
    Sweeps the WinningHunter Pinterest Ads API (GET /api/v1/pinterest-ads) across markets
    and/or a keyword, and prints gate-ready, dropship-filtered, video-only rows.

.DESCRIPTION
    Implements Step 0.5 of the find-winning-products skill (../SKILL.md):
      - Market sweep in priority order (DE first) when -Countries is not given.
      - Keyword search (no countries filter) when -Keyword is given.
      - Client-side filters: video-only (media_type), dropship-only (non-empty
        shopify_shopifydomain + brand blocklist), and price band (min/max), because the
        SKILL.md documents that the API's own media/price filters are unreliable or
        collapse the result set (most shopify_productprice values are null).

    ############################################################################
    # NOT YET VERIFIED AGAINST THE LIVE API.
    #
    # This script was written from ../SKILL.md's description of the API, not from
    # WinningHunter's own API docs (none were available when this was written). Two
    # things in particular are guesses and WILL likely need correcting on first run:
    #
    #   1. Authentication scheme — tries, in order: Authorization: Bearer <key>,
    #      then X-Api-Key: <key>, then ?api_key=<key> as a query param. Whichever
    #      succeeds first is reported and reused for the rest of the run. If all
    #      three fail, check WinningHunter's API docs for the real scheme and fix
    #      Invoke-WHRequest below.
    #   2. Response field names — id, save_count, repin_count, adscore, daysrunning,
    #      adscount, pin_url, link, domain, shopify_* fields, media_type/video, and
    #      any credit-balance field are read defensively (missing = printed as
    #      "n/a", never fabricated) but the exact names may differ from what's
    #      actually returned. Run once with -RawJsonOut to capture a real response
    #      and adjust the field names below to match. `id` in particular is load-bearing:
    #      it is the only source for winninghunter_link and pinterest_link (Get-PinterestAdId
    #      below) — confirm its real name against a raw response before trusting either link.
    #
    # Do not trust the "gate-ready" filtering to be correct until you've confirmed
    # the field names against a real response.
    ############################################################################

.PARAMETER Niches
    Comma-separated WinningHunter niche codes, e.g. "CG,JY,BG". Optional — omit for a
    keyword-only search, or to browse a market unfiltered by niche.

.PARAMETER Countries
    Comma-separated ISO2 country codes, e.g. "DE,AT". Omit to sweep the full default
    market ladder (DE first). Ignored (with a warning) if -Keyword is set, per SKILL.md's
    "pass no countries filter on keyword queries" rule.

.PARAMETER Keyword
    A single keyword/phrase to search. When set, the market sweep is skipped — one
    request (or -PagesPerMkt pages of it) is issued with no country filter.

.PARAMETER MinDays
    Passed as `mindays`. Default 21 (matches SKILL.md's Tier B/C days-running gate).

.PARAMETER AdScoreFilter
    Passed as `adscorefilter`. One of winning|scaling|testing. Default "winning".

.PARAMETER PagesPerMkt
    How many pages to pull per market (or per keyword). Default 1. SKILL.md suggests
    raising to 2-3 once the ledger has burned through shallow results.

.PARAMETER MinPrice / MaxPrice
    Client-side price band applied to shopify_productprice. Rows with a null price are
    kept and flagged "price unknown — verify on landing page" rather than dropped,
    per SKILL.md Step 0.5's price-null caveat.

.PARAMETER IncludeImages
    Skip the video-only filter. Off by default — SKILL.md rule 2 says never deliver a
    static ad.

.PARAMETER SkipDropshipFilter
    Skip the shopify_shopifydomain / blocklist filter. Off by default.

.PARAMETER ApiKeyPath
    Path to a plaintext file containing only the API key. Defaults to
    ~/.claude/.winninghunter-api-key (deliberately outside the skill folder — see
    SKILL.md — so the key never travels if the skill folder is copied/shared).

.PARAMETER BrandBlocklistPath
    Path to ../references/brand-blocklist.md. If present, any line containing a bare
    domain (word.tld) is treated as a blocked domain for the dropship filter. Missing
    file = no blocklist applied (a warning is printed, not an error).

.PARAMETER RawJsonOut
    Directory to dump the raw JSON response of each request into, named
    <market-or-keyword>-page<N>.json. Use this on the first real run to verify field
    names against ../SKILL.md's assumptions.

.PARAMETER DryRun
    Print the request URLs that would be called, without calling them or spending
    credits.

.EXAMPLE
    ./pinterest-search.ps1 -Niches "CG,JY,BG" -Countries "DE" -MinDays 21

.EXAMPLE
    ./pinterest-search.ps1 -Keyword "mens watch" -MinDays 21 -PagesPerMkt 1

.EXAMPLE
    ./pinterest-search.ps1 -DryRun
    # Full 14-market sweep, no niches/keyword filter, just to see the URL list.
#>

[CmdletBinding()]
param(
    [string]$Niches,
    [string]$Countries,
    [string]$Keyword,
    [int]$MinDays = 21,
    [ValidateSet('winning', 'scaling', 'testing')]
    [string]$AdScoreFilter = 'winning',
    [int]$PagesPerMkt = 1,
    [double]$MinPrice,
    [double]$MaxPrice,
    [switch]$IncludeImages,
    [switch]$SkipDropshipFilter,
    [string]$ApiKeyPath = (Join-Path $HOME '.claude/.winninghunter-api-key'),
    [string]$BrandBlocklistPath = (Join-Path $PSScriptRoot '../references/brand-blocklist.md'),
    [string]$RawJsonOut,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

# Priority order per SKILL.md Step 0.5 "THE MARKET SWEEP" — DE first, AT second (same
# language), US third (deepest pool), then by Pinterest commerce maturity.
$DefaultMarketSweep = @('DE', 'AT', 'US', 'GB', 'FR', 'NL', 'CA', 'AU', 'IT', 'ES', 'BR', 'SE', 'DK', 'PL')

$ApiBase = 'https://app.winninghunter.com/api/v1/pinterest-ads'

# ---------------------------------------------------------------------------
# API key
# ---------------------------------------------------------------------------
function Get-WHApiKey {
    if (-not (Test-Path $ApiKeyPath)) {
        throw "No API key found at '$ApiKeyPath'. Save your WinningHunter API key there " +
              "(plaintext, single line, no quotes) before running this script. " +
              "See SKILL.md Step 0.5 for why this file lives outside the skill folder."
    }
    $key = (Get-Content -Path $ApiKeyPath -Raw).Trim()
    if ([string]::IsNullOrWhiteSpace($key)) {
        throw "API key file at '$ApiKeyPath' is empty."
    }
    return $key
}

# ---------------------------------------------------------------------------
# Brand blocklist (optional — dropship filter)
# ---------------------------------------------------------------------------
function Get-BrandBlocklist {
    if (-not (Test-Path $BrandBlocklistPath)) {
        Write-Warning "Brand blocklist not found at '$BrandBlocklistPath' — dropship filter " +
                       "will only apply the 'must have shopify_shopifydomain' rule, not the " +
                       "named-brand exclusions. See SKILL.md's references/brand-blocklist.md."
        return @()
    }
    $domainPattern = '\b([a-z0-9-]+\.(?:com|de|fr|es|it|nl|co|shop|store|net))\b'
    $domains = Select-String -Path $BrandBlocklistPath -Pattern $domainPattern -AllMatches |
        ForEach-Object { $_.Matches } | ForEach-Object { $_.Groups[1].Value.ToLowerInvariant() } |
        Sort-Object -Unique
    return $domains
}

# ---------------------------------------------------------------------------
# HTTP call with auth-scheme auto-probe
# ---------------------------------------------------------------------------
$script:WorkingAuthScheme = $null  # cached once one succeeds, to avoid re-probing every call

function Invoke-WHRequest {
    param(
        [Parameter(Mandatory)] [hashtable]$QueryParams,
        [Parameter(Mandatory)] [string]$ApiKey,
        [Parameter(Mandatory)] [string]$LabelForOutput
    )

    $qs = ($QueryParams.GetEnumerator() | Where-Object { $null -ne $_.Value -and $_.Value -ne '' } |
        ForEach-Object { "$($_.Key)=$([uri]::EscapeDataString([string]$_.Value))" }) -join '&'
    $baseUrl = "$ApiBase?$qs"

    if ($DryRun) {
        Write-Host "[DRY RUN] $LabelForOutput -> $baseUrl"
        return $null
    }

    $attempts = if ($script:WorkingAuthScheme) {
        @($script:WorkingAuthScheme)
    } else {
        @('Bearer', 'ApiKeyHeader', 'QueryParam')
    }

    $lastError = $null
    foreach ($scheme in $attempts) {
        try {
            $url = $baseUrl
            $headers = @{}
            switch ($scheme) {
                'Bearer'      { $headers['Authorization'] = "Bearer $ApiKey" }
                'ApiKeyHeader' { $headers['X-Api-Key'] = $ApiKey }
                'QueryParam'  { $url = "$baseUrl&api_key=$([uri]::EscapeDataString($ApiKey))" }
            }

            $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get -ErrorAction Stop

            if (-not $script:WorkingAuthScheme) {
                $script:WorkingAuthScheme = $scheme
                Write-Host "  (auth scheme '$scheme' worked — reusing it for the rest of this run)" -ForegroundColor DarkGray
            }

            if ($RawJsonOut) {
                if (-not (Test-Path $RawJsonOut)) { New-Item -ItemType Directory -Path $RawJsonOut -Force | Out-Null }
                $safeLabel = ($LabelForOutput -replace '[^\w-]', '_')
                $response | ConvertTo-Json -Depth 10 | Out-File (Join-Path $RawJsonOut "$safeLabel.json")
            }

            return $response
        } catch {
            $lastError = $_
            continue
        }
    }

    Write-Warning "$LabelForOutput — all auth schemes failed. Last error: $($lastError.Exception.Message)"
    if ($lastError.Exception.Response) {
        Write-Warning "  HTTP status: $($lastError.Exception.Response.StatusCode.value__)"
    }
    return $null
}

# ---------------------------------------------------------------------------
# Row filtering — video-only, dropship-only, price band
# ---------------------------------------------------------------------------
function Get-Field {
    param($Row, [string[]]$Candidates)
    foreach ($name in $Candidates) {
        if ($Row.PSObject.Properties.Name -contains $name -and $null -ne $Row.$name -and $Row.$name -ne '') {
            return $Row.$name
        }
    }
    return $null
}

function Test-IsVideo {
    param($Row)
    $mediaType = Get-Field $Row @('media_type', 'mediatype')
    $videoUrl  = Get-Field $Row @('video', 'video_url')
    if ($videoUrl) { return $true }
    if ($mediaType -and $mediaType.ToString().ToLowerInvariant() -like '*video*') { return $true }
    return $false
}

function Test-IsDropship {
    param($Row, [string[]]$Blocklist)
    $shopDomain = Get-Field $Row @('shopify_shopifydomain', 'shopify_domain')
    if (-not $shopDomain) { return $false }
    $domainLower = $shopDomain.ToString().ToLowerInvariant()
    foreach ($blocked in $Blocklist) {
        if ($domainLower -like "*$blocked*") { return $false }
    }
    return $true
}

function Get-PriceStatus {
    param($Row)
    $price = Get-Field $Row @('shopify_productprice')
    if ($null -eq $price -or $price -eq $false) {
        return @{ Price = $null; Status = 'unknown — verify on landing page' }
    }
    $priceNum = [double]$price
    if ($MinPrice -and $priceNum -lt $MinPrice) { return @{ Price = $priceNum; Status = "below min ($MinPrice)" } }
    if ($MaxPrice -and $priceNum -gt $MaxPrice) { return @{ Price = $priceNum; Status = "above max ($MaxPrice)" } }
    return @{ Price = $priceNum; Status = 'in band' }
}

function Get-PinterestAdId {
    # The row's own numeric id — SAME id used for both the WinningHunter deep link
    # (.../ad/<id>?platform=pinterest) and the live pin (pinterest.com/pin/<id>). Read it
    # directly off the row first; only fall back to scraping it out of pin_url/link when the
    # field itself is missing, since either one alone can be null on a given row (see SKILL.md
    # "Pinterest ad links are mandatory too").
    param($Row)
    $id = Get-Field $Row @('id', 'ad_id', 'adid', 'pin_id', 'pinid')
    if ($id) { return $id.ToString() }
    foreach ($urlField in @('pin_url', 'link')) {
        $url = Get-Field $Row @($urlField)
        if ($url -and $url -match '/pin/(\d+)') { return $Matches[1] }
    }
    return $null
}

function ConvertTo-GateReadyRow {
    param($Row, [string]$Market, [string]$SourceLabel)

    $adId = Get-PinterestAdId $Row

    [pscustomobject]@{
        source              = 'Pinterest'
        market_queried      = $Market
        query_label         = $SourceLabel
        domain              = Get-Field $Row @('domain')
        shopify_domain      = Get-Field $Row @('shopify_shopifydomain', 'shopify_domain')
        shopify_productid   = Get-Field $Row @('shopify_productid')
        price               = (Get-PriceStatus $Row).Price
        price_status        = (Get-PriceStatus $Row).Status
        currency            = Get-Field $Row @('shopify_currency')
        media_type          = Get-Field $Row @('media_type', 'mediatype')
        is_video            = Test-IsVideo $Row
        daysrunning         = Get-Field $Row @('daysrunning', 'days_running')
        adscount            = Get-Field $Row @('adscount', 'ads_count')
        adscore             = Get-Field $Row @('adscore')
        save_count          = Get-Field $Row @('save_count')
        repin_count         = Get-Field $Row @('repin_count')
        pin_url             = Get-Field $Row @('pin_url')
        link                = Get-Field $Row @('link')
        niche_v2            = Get-Field $Row @('niche_v2', 'niche')
        language            = Get-Field $Row @('language')
        # Carried as first-class fields from the moment the row is read — never reconstructed
        # by hand later while writing the sheet, which is where 216/219 lost them (2026-08-25).
        pin_ad_id           = $adId
        winninghunter_link  = if ($adId) { "https://app.winninghunter.com/ad/${adId}?platform=pinterest" } else { $null }
        pinterest_link      = if ($adId) { "https://www.pinterest.com/pin/$adId" } else { $null }
        pin_link_status     = if ($adId) { 'ok' } else { 'n/a - pin id not returned by API for this row' }
    }
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
$apiKey = if ($DryRun) { '<dry-run-no-key-needed>' } else { Get-WHApiKey }
$blocklist = if ($SkipDropshipFilter) { @() } else { Get-BrandBlocklist }

$allRawRows = New-Object System.Collections.Generic.List[object]
$requestCount = 0

if ($Keyword) {
    if ($Countries) {
        Write-Warning "Both -Keyword and -Countries were given. Per SKILL.md, keyword queries " +
                       "pass no countries filter — ignoring -Countries."
    }
    Write-Host "Keyword sweep: '$Keyword' (no country filter, per SKILL.md)" -ForegroundColor Cyan

    for ($page = 1; $page -le $PagesPerMkt; $page++) {
        $label = "keyword-$($Keyword -replace '\s','_')-page$page"
        Write-Host "  -> $label"
        $resp = Invoke-WHRequest -ApiKey $apiKey -LabelForOutput $label -QueryParams @{
            page          = $page
            adscorefilter = $AdScoreFilter
            mindays       = $MinDays
            keyword       = $Keyword
            niches        = $Niches
        }
        $requestCount++
        if ($resp) {
            $rows = Get-Field $resp @('data', 'results', 'items')
            if ($rows) { foreach ($r in $rows) { $allRawRows.Add(@{ Row = $r; Market = 'n/a (keyword)'; Label = $label }) } }
        }
    }
} else {
    $markets = if ($Countries) { $Countries -split ',' | ForEach-Object { $_.Trim() } } else { $DefaultMarketSweep }
    Write-Host "Market sweep: $($markets -join ', ')" -ForegroundColor Cyan

    foreach ($market in $markets) {
        for ($page = 1; $page -le $PagesPerMkt; $page++) {
            $label = "$market-page$page"
            Write-Host "  -> $label"
            $resp = Invoke-WHRequest -ApiKey $apiKey -LabelForOutput $label -QueryParams @{
                page          = $page
                adscorefilter = $AdScoreFilter
                mindays       = $MinDays
                countries     = $market
                niches        = $Niches
            }
            $requestCount++
            if ($resp) {
                $rows = Get-Field $resp @('data', 'results', 'items')
                if ($rows) { foreach ($r in $rows) { $allRawRows.Add(@{ Row = $r; Market = $market; Label = $label }) } }
            }
        }
    }
}

if ($DryRun) {
    Write-Host "`nDry run complete. $requestCount request(s) would have been made. No credits spent."
    return
}

Write-Host "`n$requestCount request(s) made (~$requestCount credit(s), per SKILL.md's '1 credit per request')." -ForegroundColor Cyan
Write-Host "Raw rows returned: $($allRawRows.Count)"

$gateReady = $allRawRows | ForEach-Object { ConvertTo-GateReadyRow -Row $_.Row -Market $_.Market -SourceLabel $_.Label }

if (-not $IncludeImages) {
    $before = $gateReady.Count
    $gateReady = $gateReady | Where-Object { $_.is_video }
    Write-Host "Video-only filter: $before -> $($gateReady.Count) rows (SKILL.md rule 2 — no static ads)."
}

if (-not $SkipDropshipFilter) {
    $before = $gateReady.Count
    $gateReady = $gateReady | Where-Object { $_.shopify_domain }
    Write-Host "Dropship filter (must have shopify_shopifydomain): $before -> $($gateReady.Count) rows."
    if ($blocklist.Count -gt 0) {
        $before = $gateReady.Count
        $gateReady = $gateReady | Where-Object {
            $d = $_.shopify_domain.ToLowerInvariant()
            -not ($blocklist | Where-Object { $d -like "*$_*" })
        }
        Write-Host "Brand blocklist filter: $before -> $($gateReady.Count) rows."
    }
}

if ($gateReady.Count -eq 0) {
    Write-Warning "No rows survived filtering. If this is the first live run, check: (1) did an " +
                   "auth scheme succeed above? (2) run with -RawJsonOut to inspect the real response " +
                   "shape and fix field names in Get-Field calls if they don't match."
}

$gateReady | Sort-Object -Property @{Expression = 'daysrunning'; Descending = $true} |
    Format-Table -AutoSize -Property market_queried, domain, shopify_domain, price, price_status, `
        currency, is_video, daysrunning, adscount, adscore, save_count, niche_v2, link, `
        pin_ad_id, pinterest_link

$missingPinLink = ($gateReady | Where-Object { -not $_.pin_ad_id }).Count
if ($missingPinLink -gt 0) {
    Write-Warning "$missingPinLink row(s) have no pin_ad_id and therefore no winninghunter_link " +
                   "or pinterest_link — per SKILL.md, write 'n/a - pin id not returned by API " +
                   "for this row' for those, do not guess a URL, and prefer re-querying the ad " +
                   "before dropping it."
}

Write-Host "`nDone. $($gateReady.Count) gate-ready row(s) after client-side filtering. Open each " +
           "'link' and 'pinterest_link' to verify price/handle before delivering, per SKILL.md's " +
           "mandatory link check."

return $gateReady
