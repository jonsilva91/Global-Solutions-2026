# Test RAG Copilot Endpoint

Write-Host "Testing RAG Copilot Operational Report Generator" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Run risk analysis
Write-Host "Step 1: Running risk analysis..." -ForegroundColor Yellow
$riskBody = @{
    area_of_interest = "Pantanal"
    sensor_data = @{
        temperature = 39
        humidity = 18
        soil_moisture = 15
        smoke_level = 35
    }
} | ConvertTo-Json -Depth 5

try {
    $risk = Invoke-RestMethod "http://127.0.0.1:8000/risk/analyze" -Method POST -ContentType "application/json" -Body $riskBody
    Write-Host "Risk analysis completed" -ForegroundColor Green
    Write-Host "  Risk Level: $($risk.risk_level)" -ForegroundColor $(if ($risk.risk_level -eq "HIGH" -or $risk.risk_level -eq "CRITICAL") { "Red" } else { "Yellow" })
    Write-Host "  Risk Score: $($risk.risk_score)" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "Risk analysis failed: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Generate copilot report
Write-Host "Step 2: Generating copilot operational briefing..." -ForegroundColor Yellow
$copilotBody = @{
    risk_analysis = $risk
} | ConvertTo-Json -Depth 10

try {
    $report = Invoke-RestMethod "http://127.0.0.1:8000/copilot/report" -Method POST -ContentType "application/json" -Body $copilotBody
    Write-Host "Copilot report generated successfully" -ForegroundColor Green
    Write-Host ""
    
    # Display report summary
    Write-Host "OPERATIONAL BRIEFING SUMMARY" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Title: $($report.title)" -ForegroundColor White
    Write-Host "Area: $($report.area_of_interest)" -ForegroundColor White
    Write-Host "Risk Level: $($report.risk_level)" -ForegroundColor $(if ($report.risk_level -eq "HIGH" -or $report.risk_level -eq "CRITICAL") { "Red" } else { "Yellow" })
    Write-Host "Risk Score: $($report.risk_score)" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Executive Summary:" -ForegroundColor Cyan
    Write-Host $report.executive_summary -ForegroundColor White
    Write-Host ""
    
    Write-Host "Evidence Summary ($($report.evidence_summary.Count) items):" -ForegroundColor Cyan
    $report.evidence_summary | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    Write-Host ""
    
    Write-Host "Recommended Actions ($($report.recommended_actions.Count) items):" -ForegroundColor Cyan
    $report.recommended_actions | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    Write-Host ""
    
    Write-Host "Knowledge Base Files Used ($($report.source_provenance.knowledge_base.Count)):" -ForegroundColor Cyan
    $report.source_provenance.knowledge_base | ForEach-Object { 
        $filename = Split-Path $_ -Leaf
        Write-Host "  - $filename" -ForegroundColor Magenta 
    }
    Write-Host ""
    
    Write-Host "Limitations ($($report.limitations.Count) items):" -ForegroundColor Cyan
    $report.limitations | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
    Write-Host ""
    
    Write-Host "Generated At: $($report.generated_at)" -ForegroundColor White
    Write-Host ""
    
    Write-Host "All tests passed!" -ForegroundColor Green
    
} catch {
    Write-Host "Copilot report generation failed: $_" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Made with Bob
