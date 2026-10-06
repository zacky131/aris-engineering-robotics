# install_skills.ps1 — Windows PowerShell Installer for ARIS Engineering Robotics
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity -Project C:\path\to\my_project
#   powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform codex -Project C:\path\to\my_project
#   powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform claude -Project C:\path\to\my_project
#   powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -Platform antigravity
#   powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -ListPlatforms
#   powershell -ExecutionPolicy Bypass -File tools\install_skills.ps1 -ListSkills

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("codex", "claude", "antigravity")]
    [string]$Platform,

    [Parameter(Mandatory=$false)]
    [string]$Project,

    [Parameter(Mandatory=$false)]
    [switch]$DryRun,

    [Parameter(Mandatory=$false)]
    [switch]$ListPlatforms,

    [Parameter(Mandatory=$false)]
    [switch]$ListSkills
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

if ($ListPlatforms) {
    Write-Host "codex"
    Write-Host "claude"
    Write-Host "antigravity"
    exit 0
}

if ($ListSkills) {
    Write-Host ""
    Write-Host "=== ARIS Research Skills ==="
    Write-Host "  research-lit, idea-discovery, idea-discovery-robot, novelty-check"
    Write-Host "  experiment-plan, research-implement-feature, run-experiment"
    Write-Host "  monitor-experiment, analyze-results, ablation-planner"
    Write-Host "  paper-claim-audit, research-review, rebuttal, paper-compile"
    Write-Host "  research-pipeline, dse-loop, claims-drafting, result-to-claim"
    Write-Host "  citation-audit, formula-derivation, paper-write"
    Write-Host ""
    Write-Host "=== Robotics / Control Skills ==="
    Write-Host "  anchor-paper-intake, robotics-research-router, robotics-experiment-plan"
    Write-Host "  run-robotics-experiment, robotics-watchdog"
    Write-Host "  robotics-result-analysis, controller-tuning"
    Write-Host "  robotics-experiment-audit, simulation-validation"
    Write-Host "  sil-hil-validation, robotics-result-to-claim"
    Write-Host "  vla-robotics, learning-control-eval, safety-filter-cbf"
    Write-Host "  research-pipeline-robotics"
    Write-Host ""
    Write-Host "=== Engineering Paper Skills ==="
    Write-Host "  engineering-writing, engineering-polishing, engineering-paper-auditor"
    Write-Host "  engineering-figure-table, engineering-response, engineering-validation"
    Write-Host "  engineering-paper-router, engineering-paper-coach"
    exit 0
}

if (-not $Platform) {
    Write-Error "Platform is required: -Platform antigravity | codex | claude"
    exit 1
}

# Resolve destination
$HomeDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)

if ($Platform -eq "codex") {
    if ($Project) { $Dest = Join-Path $Project ".codex\skills" } else { $Dest = Join-Path $HomeDir ".codex\skills" }
} elseif ($Platform -eq "claude") {
    if ($Project) { $Dest = Join-Path $Project ".claude\skills" } else { $Dest = Join-Path $HomeDir ".claude\skills" }
} elseif ($Platform -eq "antigravity") {
    if ($Project) { $Dest = Join-Path $Project ".agents\skills" } else { $Dest = Join-Path $HomeDir ".gemini\config\skills" }
}

Write-Host "=== ARIS Engineering Robotics — Skill Installer (Windows PowerShell) ==="
Write-Host "Platform   : $Platform"
Write-Host "Dry run    : $DryRun"
Write-Host "Destination: $Dest"
Write-Host ""

$InstalledSkills = @()
$InstalledShared = @()
$InstalledWorkflows = @()
$InstalledAgentsMd = $false

# 1. Install skills
Write-Host "--- Installing all skills (robotics, research, engineering paper) ---"
$SkillsDir = Join-Path $RepoRoot "skills"
$SkillItems = Get-ChildItem -Path $SkillsDir -Directory | Where-Object { $_.Name -notin @("_shared", "shared-references") }

foreach ($skill in $SkillItems) {
    $targetDir = Join-Path $Dest $skill.Name
    if ($DryRun) {
        Write-Host "  DRY-RUN: would install $($skill.Name) → $targetDir"
    } else {
        if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }
        if (Test-Path $targetDir) { Remove-Item -Path $targetDir -Recurse -Force }
        Copy-Item -Path $skill.FullName -Destination $targetDir -Recurse -Force
        Write-Host "  INSTALLED: $($skill.Name)"
        $InstalledSkills += $skill.Name
    }
}

# 2. Install shared dependencies
Write-Host ""
Write-Host "--- Installing shared dependencies ---"
$SharedDeps = @("shared-references", "_shared")
foreach ($dep in $SharedDeps) {
    $src = Join-Path $RepoRoot "shared\$dep"
    if (-not (Test-Path $src)) {
        $src = Join-Path $RepoRoot "skills\$dep"
    }
    if (Test-Path $src) {
        $targetDir = Join-Path $Dest $dep
        if ($DryRun) {
            Write-Host "  DRY-RUN: would install shared/$dep → $targetDir"
        } else {
            if (-not (Test-Path $Dest)) { New-Item -ItemType Directory -Path $Dest -Force | Out-Null }
            if (Test-Path $targetDir) { Remove-Item -Path $targetDir -Recurse -Force }
            Copy-Item -Path $src -Destination $targetDir -Recurse -Force
            Write-Host "  INSTALLED shared: $dep"
            $InstalledShared += $dep
        }
    }
}

# 3. Antigravity project-local setup
if ($Platform -eq "antigravity" -and $Project) {
    $AgentsDir = Join-Path $Project ".agents"
    $AgentsMd = Join-Path $AgentsDir "AGENTS.md"
    $AgentsTemplate = Join-Path $RepoRoot "templates\antigravity\AGENTS.md"
    $ManagedBegin = "<!-- BEGIN ARIS-ENGINEERING-ROBOTICS -->"
    $ManagedEnd = "<!-- END ARIS-ENGINEERING-ROBOTICS -->"

    if ($DryRun) {
        Write-Host ""
        Write-Host "DRY-RUN: would install .agents\AGENTS.md (safe patch)"
        Write-Host "DRY-RUN: would install .agents\workflows\ (workflow files)"
    } else {
        if (-not (Test-Path $AgentsDir)) { New-Item -ItemType Directory -Path $AgentsDir -Force | Out-Null }

        if (-not (Test-Path $AgentsMd)) {
            Copy-Item -Path $AgentsTemplate -Destination $AgentsMd -Force
            Write-Host ""
            Write-Host "INSTALLED: .agents\AGENTS.md"
            $InstalledAgentsMd = $true
        } else {
            $existing = Get-Content -Path $AgentsMd -Raw -Encoding UTF8
            $template = Get-Content -Path $AgentsTemplate -Raw -Encoding UTF8
            $startIdx = $template.IndexOf($ManagedBegin)
            $endIdx = $template.IndexOf($ManagedEnd) + $ManagedEnd.Length
            $managedBlock = $template.Substring($startIdx, $endIdx - $startIdx)

            if ($existing.Contains($ManagedBegin)) {
                $eStart = $existing.IndexOf($ManagedBegin)
                $eEnd = $existing.IndexOf($ManagedEnd) + $ManagedEnd.Length
                $updated = $existing.Substring(0, $eStart) + $managedBlock + $existing.Substring($eEnd)
                Set-Content -Path $AgentsMd -Value $updated -Encoding UTF8
                Write-Host "  UPDATED: .agents\AGENTS.md (managed block replaced)"
            } else {
                $updated = $existing + "`n`n---`n`n" + $managedBlock
                Set-Content -Path $AgentsMd -Value $updated -Encoding UTF8
                Write-Host "  APPENDED: .agents\AGENTS.md (managed block added)"
            }
            $InstalledAgentsMd = $true
        }

        # Workflows
        $WfDest = Join-Path $AgentsDir "workflows"
        if (-not (Test-Path $WfDest)) { New-Item -ItemType Directory -Path $WfDest -Force | Out-Null }
        $WfSrc = Join-Path $RepoRoot "templates\antigravity\workflows"
        Write-Host ""
        Write-Host "--- Installing Antigravity workflows ---"
        Get-ChildItem -Path $WfSrc -Filter "*.md" | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination (Join-Path $WfDest $_.Name) -Force
            Write-Host "  INSTALLED workflow: $($_.Name)"
            $InstalledWorkflows += $_.Name
        }
    }
}

# 4. Manifest
if (-not $DryRun) {
    $ManifestDir = Join-Path $RepoRoot ".aris-engineering-robotics"
    if (-not (Test-Path $ManifestDir)) { New-Item -ItemType Directory -Path $ManifestDir -Force | Out-Null }
    $ManifestYaml = Join-Path $ManifestDir "installed-manifest.yaml"
    $ManifestTxt = Join-Path $ManifestDir "installed-skills.txt"

    $now = (Get-Date).ToString("o")
    $content = @"
# ARIS Engineering Robotics — install manifest
# Generated: $now
platform: $Platform
destination: $Dest
"@
    if ($Project) { $content += "`nproject: $Project" }
    $content += "`n`nmanaged:`n  skills:"
    foreach ($s in $InstalledSkills) { $content += "`n    - $s" }
    $content += "`n  shared:"
    foreach ($s in $InstalledShared) { $content += "`n    - $s" }
    $content += "`n  agents_md: $InstalledAgentsMd`n  workflows:"
    foreach ($w in $InstalledWorkflows) { $content += "`n    - $w" }
    $content += "`n"

    Set-Content -Path $ManifestYaml -Value $content -Encoding UTF8

    $txtLines = @()
    foreach ($s in $InstalledSkills) { $txtLines += (Join-Path $Dest $s) }
    foreach ($s in $InstalledShared) { $txtLines += (Join-Path $Dest $s) }
    Set-Content -Path $ManifestTxt -Value ($txtLines -join "`n") -Encoding UTF8

    Write-Host ""
    Write-Host "Manifest written to: $ManifestYaml"
}

Write-Host ""
Write-Host "=== Install complete (platform=$Platform dry_run=$DryRun) ==="
Write-Host ""
Write-Host "Validate with:"
Write-Host "  python tools\validate_installation.py --platform $Platform --dest `"$Dest`""
