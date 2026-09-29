$ErrorActionPreference = 'Stop'
$auditDir = $PSScriptRoot
$planPath = Join-Path $auditDir 'approved-cleanup-plan-2026-09-21.json'
$plan = Get-Content -LiteralPath $planPath -Raw | ConvertFrom-Json
$logPath = Join-Path $auditDir 'cleanup-results-2026-09-21.jsonl'
$prior = @()
if (Test-Path -LiteralPath $logPath) {
  $prior = @(Get-Content -LiteralPath $logPath | ForEach-Object { $_ | ConvertFrom-Json })
  if (@($prior | Where-Object { $_.event -eq 'finish' }).Count -gt 0) { throw 'Cleanup already finished.' }
}
Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
public static class ApprovedCleanup {
  public static List<string> Errors = new List<string>();
  public static long Files = 0;
  public static long Bytes = 0;
  public static string Normal(string p) { return Path.GetFullPath(p).TrimEnd('\\'); }
  public static bool Within(string p,string root) {
    p=Normal(p); root=Normal(root);
    return p.Equals(root,StringComparison.OrdinalIgnoreCase) || p.StartsWith(root+"\\",StringComparison.OrdinalIgnoreCase);
  }
  public static void Validate(string p,string[] roots,string[] excluded) {
    p=Normal(p);
    if (p.IndexOf("lucasrouter",StringComparison.OrdinalIgnoreCase)>=0 || p.IndexOf("52d78d4a92a2",StringComparison.OrdinalIgnoreCase)>=0) throw new Exception("Lucasrouter exclusion: "+p);
    bool valid=false;
    foreach(string root in roots) if(Within(p,root)) valid=true;
    if(!valid) throw new Exception("Outside allowed roots: "+p);
    foreach(string x in excluded) if(Within(p,x)||Within(x,p)) throw new Exception("Protected path overlap: "+p);
    for(string x=p; x!=null; x=Path.GetDirectoryName(x)) {
      if((File.Exists(x)||Directory.Exists(x)) && (File.GetAttributes(x)&FileAttributes.ReparsePoint)!=0) throw new Exception("Reparse ancestor: "+x);
    }
  }
  public static void RemoveTree(string path) {
    try {
      if (!path.StartsWith(@"\\?\")) path=@"\\?\"+path;
      FileAttributes a=File.GetAttributes(path);
      bool dir=(a&FileAttributes.Directory)!=0;
      if((a&FileAttributes.ReparsePoint)!=0) {
        // Delete the link itself only. Never enumerate or touch its target.
        if(dir) Directory.Delete(path,false); else File.Delete(path);
        return;
      }
      if(dir) {
        foreach(string entry in Directory.EnumerateFileSystemEntries(path)) RemoveTree(entry);
        Directory.Delete(path,false);
      } else {
        long length=new FileInfo(path).Length;
        if((a&FileAttributes.ReadOnly)!=0) File.SetAttributes(path,a&~FileAttributes.ReadOnly);
        File.Delete(path);Interlocked.Increment(ref Files);Interlocked.Add(ref Bytes,length);
      }
    } catch(Exception e) { lock(Errors) Errors.Add(path+" :: "+e.Message); }
  }
  public static void RemoveParallel(string path) {
    if (!path.StartsWith(@"\\?\")) path=@"\\?\"+path;
    var frontier=new List<string>();frontier.Add(path);
    try {
      for(int depth=0;depth<4 && frontier.Count<40000;depth++) {
        var next=new List<string>();bool expanded=false;
        foreach(string item in frontier) {
          var a=File.GetAttributes(item);
          if((a&FileAttributes.Directory)!=0 && (a&FileAttributes.ReparsePoint)==0) {
            string[] entries=Directory.GetFileSystemEntries(item);
            if(entries.Length>0) { next.AddRange(entries);expanded=true; }
            else next.Add(item);
          } else next.Add(item);
        }
        frontier=next;
        if(!expanded) break;
      }
      Parallel.ForEach(frontier,new ParallelOptions { MaxDegreeOfParallelism=8 },item=>RemoveTree(item));
      if(Directory.Exists(path)||File.Exists(path)) RemoveTree(path);
    } catch(Exception e) { lock(Errors) Errors.Add(path+" :: "+e.Message); }
  }
}
'@
$allowed = [string[]]$plan.allowedRoots
$protected = [string[]]$plan.protectedPaths
# Validate the whole allowlist before any mutation, then each target immediately before deletion.
foreach ($row in $plan.selected) { [ApprovedCleanup]::Validate($row.path,$allowed,$protected) }
$completedIds = @($prior | Where-Object { $_.event -eq 'target' } | ForEach-Object { $_.id })
if ($prior.Count -gt 0) {
  $freeBefore = ($prior | Where-Object { $_.event -eq 'start' } | Select-Object -First 1).freeBytes
  @{event='resume';at=(Get-Date).ToUniversalTime().ToString('o');reason='Switched owned cleanup to eight file-operation threads; an interrupted target may have unlogged prior deletions';completedTargets=$completedIds.Count} | ConvertTo-Json -Compress | Add-Content -LiteralPath $logPath -Encoding UTF8
} else {
  $freeBefore = [System.IO.DriveInfo]::new('C').AvailableFreeSpace
  @{event='start';at=(Get-Date).ToUniversalTime().ToString('o');freeBytes=$freeBefore;selected=$plan.selected.Count;protected=$protected} | ConvertTo-Json -Compress | Add-Content -LiteralPath $logPath -Encoding UTF8
}
$done=$completedIds.Count
foreach ($row in $plan.selected) {
  if ($completedIds -contains $row.id) { continue }
  [ApprovedCleanup]::Validate($row.path,$allowed,$protected)
  [ApprovedCleanup]::Errors.Clear()
  [ApprovedCleanup]::Files=0
  [ApprovedCleanup]::Bytes=0
  $present=[System.IO.Directory]::Exists($row.path) -or [System.IO.File]::Exists($row.path)
  if ($present) { [ApprovedCleanup]::RemoveParallel($row.path) }
  $remaining=[System.IO.Directory]::Exists($row.path) -or [System.IO.File]::Exists($row.path)
  $status=if(-not $present){'already absent'}elseif($remaining){'partial or failed'}else{'removed'}
  @{event='target';id=$row.id;path=$row.path;status=$status;deletedFiles=[ApprovedCleanup]::Files;deletedLogicalBytes=[ApprovedCleanup]::Bytes;errors=@([ApprovedCleanup]::Errors.ToArray());at=(Get-Date).ToUniversalTime().ToString('o')} | ConvertTo-Json -Compress -Depth 5 | Add-Content -LiteralPath $logPath -Encoding UTF8
  $done++
  Write-Output "$done / $($plan.selected.Count): $($row.id) $status"
}
$freeAfter=[System.IO.DriveInfo]::new('C').AvailableFreeSpace
@{event='finish';at=(Get-Date).ToUniversalTime().ToString('o');freeBytes=$freeAfter;freeBytesBefore=$freeBefore;observedFreeSpaceIncrease=$freeAfter-$freeBefore} | ConvertTo-Json -Compress | Add-Content -LiteralPath $logPath -Encoding UTF8
Write-Output "Finished. Observed free-space increase: $([math]::Round(($freeAfter-$freeBefore)/1GB,2)) GiB"
