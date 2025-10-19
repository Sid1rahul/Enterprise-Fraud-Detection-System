$headers = @{
    'Authorization' = 'Bearer demo_token_123'
    'Content-Type' = 'application/json'
}

Write-Host "Testing API endpoints..." -ForegroundColor Green

# Test health endpoint
try {
    $health = Invoke-RestMethod -Uri 'http://localhost:8000/health' -Method GET
    Write-Host "✅ Health Check: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "❌ Health Check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test model status
try {
    $models = Invoke-RestMethod -Uri 'http://localhost:8000/api/models/status' -Method GET -Headers $headers
    Write-Host "✅ Model Status: $($models.models_loaded.Count) models loaded" -ForegroundColor Green
} catch {
    Write-Host "❌ Model Status failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "API testing complete!" -ForegroundColor Cyan
