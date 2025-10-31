# Test Authentication Endpoint

Write-Host "`n🧪 Testing PostgreSQL Authentication" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

$body = @{
    email = 'admin@elas-erp.com'
    password = 'admin123'
} | ConvertTo-Json

try {
    Write-Host "📡 Sending login request to http://localhost:8000/api/auth/login..." -ForegroundColor Yellow
    
    $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/auth/login' -Method Post -Body $body -ContentType 'application/json'
    
    Write-Host "`n✅ LOGIN SUCCESSFUL!" -ForegroundColor Green
    Write-Host "================================`n" -ForegroundColor Green
    
    Write-Host "📧 Email:      $($response.user.email)" -ForegroundColor Cyan
    Write-Host "👤 Full Name:  $($response.user.full_name)" -ForegroundColor Cyan
    Write-Host "🎭 Role:       $($response.user.role)" -ForegroundColor Cyan
    Write-Host "✅ Active:     $($response.user.is_active)" -ForegroundColor Cyan
    Write-Host "🔐 Superuser:  $($response.user.is_superuser)" -ForegroundColor Cyan
    
    Write-Host "`n🔑 Access Token (first 50 chars):" -ForegroundColor Yellow
    Write-Host "   $($response.access_token.Substring(0, [Math]::Min(50, $response.access_token.Length)))..." -ForegroundColor White
    
    Write-Host "`n🔄 Refresh Token (first 50 chars):" -ForegroundColor Yellow
    Write-Host "   $($response.refresh_token.Substring(0, [Math]::Min(50, $response.refresh_token.Length)))..." -ForegroundColor White
    
    Write-Host "`n✅ PostgreSQL authentication is working perfectly!`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ ERROR" -ForegroundColor Red
    Write-Host "================================`n" -ForegroundColor Red
    Write-Host "Message: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nMake sure the backend server is running on port 8000`n" -ForegroundColor Yellow
}
