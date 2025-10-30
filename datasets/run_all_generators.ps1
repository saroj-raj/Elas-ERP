# Elas ERP Dataset Generator Runner
# This script runs all dataset generators and creates sample data

Write-Host "`n╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          ELAS ERP DEMO DATASET GENERATOR                         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if Python is available
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check/install required packages
Write-Host "`n📦 Checking dependencies..." -ForegroundColor Yellow
$packages = @("pandas", "openpyxl", "fpdf")
foreach ($pkg in $packages) {
    Write-Host "   Checking $pkg..." -NoNewline
    $installed = pip show $pkg 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
    } else {
        Write-Host " Installing..." -ForegroundColor Yellow
        pip install $pkg --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   $pkg installed ✓" -ForegroundColor Green
        } else {
            Write-Host "   Failed to install $pkg" -ForegroundColor Red
            exit 1
        }
    }
}

# Run generators
Write-Host "`n🚀 Generating datasets..." -ForegroundColor Cyan

$generators = @(
    @{Name="Sales Retail"; File="generate_sales_retail.py"; Rows="1,200+"},
    @{Name="Finance AR"; File="generate_finance_ar.py"; Rows="600+"},
    @{Name="Operations Work Orders"; File="generate_operations_workorders.py"; Rows="500+"},
    @{Name="Education Enrollments"; File="generate_education_enrollments.py"; Rows="2,400+"},
    @{Name="Minimal Small"; File="generate_minimal_small.py"; Rows="70+"}
)

$total = $generators.Count
$current = 0

foreach ($gen in $generators) {
    $current++
    Write-Host "`n[$current/$total] Generating $($gen.Name) ($($gen.Rows) rows)..." -ForegroundColor Yellow
    
    $scriptPath = Join-Path "datasets" $gen.File
    
    if (Test-Path $scriptPath) {
        & python $scriptPath
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✓ $($gen.Name) completed successfully" -ForegroundColor Green
        } else {
            Write-Host "   ✗ $($gen.Name) failed" -ForegroundColor Red
        }
    } else {
        Write-Host "   ✗ Generator not found: $scriptPath" -ForegroundColor Red
    }
}

# Summary
Write-Host "`n╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                   GENERATION COMPLETE                            ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📂 Generated datasets in ./datasets/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Datasets created:" -ForegroundColor Yellow
Write-Host "  1. sales_retail/        - Retail transactions, products, reps" -ForegroundColor White
Write-Host "  2. finance_ar/          - Invoices, payments, AR aging + PDFs" -ForegroundColor White
Write-Host "  3. operations_workorders/ - Work orders, technicians, shifts" -ForegroundColor White
Write-Host "  4. education_enrollments/ - Student enrollments, courses" -ForegroundColor White
Write-Host "  5. minimal_small/       - Small test datasets with edge cases" -ForegroundColor White
Write-Host ""
Write-Host "Total files: ~20 CSV/XLSX + 2 PDFs + 5 README.md" -ForegroundColor Cyan
Write-Host "Total rows: ~5,000+ across all datasets" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Start your backend server" -ForegroundColor White
Write-Host "   2. Go to onboarding flow" -ForegroundColor White
Write-Host "   3. Upload files from datasets/ folders" -ForegroundColor White
Write-Host "   4. Test quick-viz and mapping features" -ForegroundColor White
Write-Host ""
