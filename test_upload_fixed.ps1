# Test file upload to the enhanced fraud detection API
$headers = @{
    'Authorization' = 'Bearer demo_token_123'
}

$filePath = 'C:\CFD\sample_transactions.csv'

Write-Host "Testing file upload API..." -ForegroundColor Green
Write-Host "File: $filePath" -ForegroundColor Yellow

try {
    # Test simple health check first
    Write-Host "Checking API health..." -ForegroundColor Cyan
    $healthResponse = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method GET
    Write-Host "API Status: $($healthResponse.status)" -ForegroundColor Green
    
    # Test file upload using curl (more reliable for multipart)
    Write-Host "Uploading file using curl..." -ForegroundColor Cyan
    $curlCommand = 'curl -X POST "http://localhost:8000/api/upload/file" -H "Authorization: Bearer demo_token_123" -F "file=@C:\CFD\sample_transactions.csv"'
    $uploadResult = Invoke-Expression $curlCommand
    
    Write-Host "Upload result:" -ForegroundColor Yellow
    Write-Host $uploadResult -ForegroundColor White
    
} catch {
    Write-Host "Error occurred: $($_.Exception.Message)" -ForegroundColor Red
}
