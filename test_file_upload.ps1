# Test file upload to the enhanced fraud detection API
$headers = @{
    'Authorization' = 'Bearer demo_token_123'
}

$filePath = 'C:\CFD\sample_transactions.csv'

Write-Host "Testing file upload API..." -ForegroundColor Green
Write-Host "File: $filePath" -ForegroundColor Yellow

try {
    # Use Invoke-WebRequest for file upload
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/upload/file' `
        -Method POST `
        -Headers $headers `
        -InFile $filePath `
        -ContentType 'multipart/form-data'
    
    Write-Host "✅ File upload successful!" -ForegroundColor Green
    Write-Host "Response: $($response.Content)" -ForegroundColor Cyan
    
    # Parse the JSON response to get file_id
    $jsonResponse = $response.Content | ConvertFrom-Json
    $fileId = $jsonResponse.file_id
    Write-Host "📁 File ID: $fileId" -ForegroundColor Yellow
    Write-Host "📊 Total Transactions: $($jsonResponse.total_transactions)" -ForegroundColor Yellow
    
    # Now test starting monitoring
    Write-Host "`nStarting monitoring session..." -ForegroundColor Green
    
    $monitoringBody = @{
        file_id = $fileId
        processing_speed_ms = 500
    }
    
    $monitoringResponse = Invoke-WebRequest -Uri 'http://localhost:8000/api/monitoring/start' `
        -Method POST `
        -Headers $headers `
        -Body $monitoringBody
    
    Write-Host "✅ Monitoring started!" -ForegroundColor Green
    Write-Host "Response: $($monitoringResponse.Content)" -ForegroundColor Cyan
    
    $monitoringJson = $monitoringResponse.Content | ConvertFrom-Json
    $sessionId = $monitoringJson.session_id
    Write-Host "🔄 Session ID: $sessionId" -ForegroundColor Yellow
    
    # Wait a few seconds and check status
    Write-Host "`nWaiting 5 seconds for processing..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Check monitoring status
    $statusResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/monitoring/status/$sessionId" `
        -Method GET `
        -Headers $headers
    
    Write-Host "📈 Monitoring Status:" -ForegroundColor Green
    Write-Host "  Status: $($statusResponse.status)" -ForegroundColor White
    Write-Host "  Processed: $($statusResponse.processed_count)/$($statusResponse.total_transactions)" -ForegroundColor White
    Write-Host "  Fraud Detected: $($statusResponse.fraud_detected)" -ForegroundColor Red
    
    # Get fraud alerts
    Write-Host "`nChecking for fraud alerts..." -ForegroundColor Green
    $alertsResponse = Invoke-RestMethod -Uri 'http://localhost:8000/api/monitoring/alerts?limit=10' `
        -Method GET `
        -Headers $headers
    
    Write-Host "🚨 Fraud Alerts: $($alertsResponse.total_alerts) total" -ForegroundColor Red
    
    if ($alertsResponse.alerts.Count -gt 0) {
        Write-Host "Recent alerts:" -ForegroundColor Yellow
        foreach ($alert in $alertsResponse.alerts | Select-Object -First 3) {
            Write-Host "  - $($alert.amount) at $($alert.merchant) (Risk: $([math]::Round($alert.risk_score * 100, 1))%)" -ForegroundColor Red
        }
    }
    
} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Response: $($_.Exception.Response)" -ForegroundColor Yellow
}
