#!/usr/bin/env pwsh
# Test Upload with Multiple File Types

Write-Host "`n" -NoNewline
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  FILE UPLOAD TEST - ALL SUPPORTED TYPES" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Create test directory
$testDir = "C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\test_files"
if (-not (Test-Path $testDir)) {
    New-Item -ItemType Directory -Path $testDir -Force | Out-Null
}

# Test 1: CSV File
Write-Host "📄 Test 1: CSV File" -ForegroundColor Yellow
$csvPath = "$testDir\test_sales.csv"
@"
ProductID,ProductName,Category,Price,Quantity,Revenue
1,Widget A,Electronics,29.99,150,4498.50
2,Widget B,Electronics,49.99,100,4999.00
3,Widget C,Office,19.99,200,3998.00
4,Widget D,Home,39.99,75,2999.25
5,Widget E,Electronics,59.99,50,2999.50
"@ | Out-File -FilePath $csvPath -Encoding UTF8

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/upload-simple" `
        -Method Post `
        -Form @{
            file = Get-Item $csvPath
            domain = "Sales"
            intent = "Revenue Analysis"
        } `
        -TimeoutSec 30
    
    Write-Host "  ✅ CSV Upload SUCCESS" -ForegroundColor Green
    Write-Host "     Dataset: $($response.dataset_id)" -ForegroundColor Gray
    Write-Host "     Widgets: $($response.widgets.Count)" -ForegroundColor Gray
    Write-Host "     Preview Rows: $($response.preview.Count)`n" -ForegroundColor Gray
}
catch {
    Write-Host "  ❌ CSV Upload FAILED: $_`n" -ForegroundColor Red
}

# Test 2: XLSX File (Excel)
Write-Host "📊 Test 2: XLSX File" -ForegroundColor Yellow
Write-Host "  ⚠️  XLSX requires Excel library - testing if supported" -ForegroundColor Yellow

# Create a simple test by copying one of the user's existing files if available
$xlsxTestFile = "C:\Users\rajsa\Downloads\GitHub\Elas-ERP\Elas-ERP\test_files\test_sales.xlsx"
if (Test-Path $xlsxTestFile) {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/api/upload-simple" `
            -Method Post `
            -Form @{
                file = Get-Item $xlsxTestFile
                domain = "Sales"
                intent = "Analysis"
            } `
            -TimeoutSec 30
        
        Write-Host "  ✅ XLSX Upload SUCCESS" -ForegroundColor Green
        Write-Host "     Dataset: $($response.dataset_id)" -ForegroundColor Gray
        Write-Host "     Widgets: $($response.widgets.Count)" -ForegroundColor Gray
        Write-Host "     Preview Rows: $($response.preview.Count)`n" -ForegroundColor Gray
    }
    catch {
        Write-Host "  ❌ XLSX Upload FAILED: $_`n" -ForegroundColor Red
    }
} else {
    Write-Host "  ℹ️  XLSX test file not found, skipping`n" -ForegroundColor Cyan
}

# Test 3: TXT File
Write-Host "📝 Test 3: TXT File" -ForegroundColor Yellow
$txtPath = "$testDir\test_data.txt"
@"
Product Report
Date: 2025-10-31

Sales Summary:
- Total Products: 5
- Total Revenue: $19,494.25
- Top Category: Electronics
- Best Seller: Widget B

Notes:
All products showing strong performance.
Electronics category leading sales.
Inventory levels adequate.
"@ | Out-File -FilePath $txtPath -Encoding UTF8

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/upload-simple" `
        -Method Post `
        -Form @{
            file = Get-Item $txtPath
            domain = "Reports"
            intent = "Document Analysis"
        } `
        -TimeoutSec 30
    
    Write-Host "  ✅ TXT Upload SUCCESS" -ForegroundColor Green
    Write-Host "     Dataset: $($response.dataset_id)" -ForegroundColor Gray
    if ($response.widgets) {
        Write-Host "     Widgets: $($response.widgets.Count)" -ForegroundColor Gray
    }
    if ($response.message) {
        Write-Host "     Message: $($response.message)`n" -ForegroundColor Gray
    }
}
catch {
    Write-Host "  ❌ TXT Upload FAILED: $_`n" -ForegroundColor Red
}

# Test 4: Large CSV File
Write-Host "📈 Test 4: Large CSV File (100 rows)" -ForegroundColor Yellow
$largeCsvPath = "$testDir\test_large_sales.csv"
$csvData = "OrderID,CustomerName,Product,Quantity,Price,Total,Date`n"
for ($i = 1; $i -le 100; $i++) {
    $products = @("Widget A", "Widget B", "Widget C", "Widget D", "Widget E")
    $product = $products[$i % 5]
    $qty = Get-Random -Minimum 1 -Maximum 50
    $price = (Get-Random -Minimum 10 -Maximum 100) + 0.99
    $total = [math]::Round($qty * $price, 2)
    $date = "2025-10-" + (Get-Random -Minimum 1 -Maximum 31).ToString("00")
    $csvData += "$i,Customer$i,$product,$qty,$price,$total,$date`n"
}
$csvData | Out-File -FilePath $largeCsvPath -Encoding UTF8

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/upload-simple" `
        -Method Post `
        -Form @{
            file = Get-Item $largeCsvPath
            domain = "Sales"
            intent = "Trend Analysis"
        } `
        -TimeoutSec 30
    
    Write-Host "  ✅ Large CSV Upload SUCCESS" -ForegroundColor Green
    Write-Host "     Dataset: $($response.dataset_id)" -ForegroundColor Gray
    Write-Host "     Widgets: $($response.widgets.Count)" -ForegroundColor Gray
    Write-Host "     Preview Rows: $($response.preview.Count)`n" -ForegroundColor Gray
}
catch {
    Write-Host "  ❌ Large CSV Upload FAILED: $_`n" -ForegroundColor Red
}

# Summary
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  TEST COMPLETE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📁 Test files created in: $testDir" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Open your browser at http://localhost:4000/onboarding/upload" -ForegroundColor Cyan
Write-Host "   2. Press Ctrl+F5 to hard refresh (clear cache)" -ForegroundColor Cyan
Write-Host "   3. Upload your actual files (CSV, XLSX supported)" -ForegroundColor Cyan
Write-Host "   4. Upload should work without errors now!`n" -ForegroundColor Cyan
