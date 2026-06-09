# Test script for Space-Enabled Risk Engine
Write-Host "=== Testing Space-Enabled Risk Engine ===" -ForegroundColor Cyan

# Test 1: Simple risk analysis
Write-Host "`nTest 1: Basic Risk Analysis" -ForegroundColor Yellow

$body = @{
    area_of_interest = "Test Area"
    sensor_data = @{
        temperature = 30
        humidity = 40
        soil_moisture = 30
        smoke_level = 5
    }
} | ConvertTo-Json -Depth 5

try {
    $response = Invoke-RestMethod "http://127.0.0.1:8000/risk/analyze" -Method POST -ContentType "application/json" -Body $body
    Write-Host "Success: Risk Score: $($response.total_risk_score)" -ForegroundColor Green
    Write-Host "Success: Risk Level: $($response.risk_level)" -ForegroundColor Green
    Write-Host "Success: Recommendations: $($response.recommendations.Count) items" -ForegroundColor Green
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: High risk scenario
Write-Host "`nTest 2: High Risk Scenario" -ForegroundColor Yellow

$highRiskBody = @{
    area_of_interest = "Pantanal"
    sensor_data = @{
        temperature = 39
        humidity = 18
        soil_moisture = 15
        smoke_level = 35
    }
} | ConvertTo-Json -Depth 5

try {
    $response = Invoke-RestMethod "http://127.0.0.1:8000/risk/analyze" -Method POST -ContentType "application/json" -Body $highRiskBody
    Write-Host "Success: Risk Score: $($response.total_risk_score)" -ForegroundColor Green
    Write-Host "Success: Risk Level: $($response.risk_level)" -ForegroundColor Green
    
    if ($response.risk_level -eq "HIGH" -or $response.risk_level -eq "CRITICAL") {
        Write-Host "Success: Alert should be generated for HIGH/CRITICAL risk" -ForegroundColor Green
    }
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Check alerts
Write-Host "`nTest 3: Check Alerts" -ForegroundColor Yellow

try {
    $alerts = Invoke-RestMethod "http://127.0.0.1:8000/alerts"
    Write-Host "Success: Total alerts: $($alerts.total_alerts)" -ForegroundColor Green
    Write-Host "Success: Active alerts: $($alerts.active_alerts)" -ForegroundColor Green
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Tests Complete ===" -ForegroundColor Cyan

# Made with Bob
