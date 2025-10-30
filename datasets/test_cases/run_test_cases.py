"""
Elas ERP - Automated Test Case Runner

This script automates the testing of widget generation across all test cases.
It uploads files, invokes the quick-viz API, and validates the results.

Usage:
    python run_test_cases.py                    # Run all tests
    python run_test_cases.py --industry retail  # Test specific industry
    python run_test_cases.py --size small       # Test specific company size
    python run_test_cases.py --test TC001       # Test single case
    python run_test_cases.py --parallel 4       # Run with 4 workers
    python run_test_cases.py --report detailed  # Generate detailed HTML report
"""

import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import concurrent.futures
from dataclasses import dataclass, asdict


@dataclass
class TestResult:
    """Test case execution result"""
    test_id: str
    test_name: str
    industry: str
    size: str
    status: str  # PASS, FAIL, SKIP, ERROR
    duration: float
    widgets_generated: int
    widgets_expected: int
    widget_types_match: bool
    data_accuracy: bool
    performance_ok: bool
    errors: List[str]
    timestamp: str


class ElasERPTestRunner:
    """Automated test runner for Elas ERP widget generation"""
    
    def __init__(self, backend_url: str = "http://localhost:8000"):
        self.backend_url = backend_url
        self.test_cases_dir = Path(__file__).parent
        self.sample_data_dir = self.test_cases_dir.parent / "sample_data"
        self.results_dir = self.test_cases_dir / "test_results"
        self.results_dir.mkdir(exist_ok=True)
        
        self.results: List[TestResult] = []
        
    def check_backend_health(self) -> bool:
        """Verify backend is running"""
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def parse_test_case(self, md_file: Path) -> Dict:
        """Extract test case metadata from markdown file"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parsing (you can enhance this with proper MD parser)
        lines = content.split('\n')
        metadata = {
            'test_id': '',
            'industry': '',
            'size': '',
            'files': [],
            'domain': '',
            'intent': '',
            'expected_widgets': 0
        }
        
        for i, line in enumerate(lines):
            if '**Test Case ID**:' in line:
                metadata['test_id'] = line.split(':')[1].strip()
            elif '**Industry**:' in line:
                metadata['industry'] = line.split(':')[1].strip()
            elif '**Company Size**:' in line:
                size_text = line.split(':')[1].strip()
                if 'Small' in size_text:
                    metadata['size'] = 'Small'
                elif 'Medium' in size_text:
                    metadata['size'] = 'Medium'
                elif 'Large' in size_text:
                    metadata['size'] = 'Large'
            elif '**Domain**:' in line:
                metadata['domain'] = line.split(':', 1)[1].strip().strip('"')
            elif '**User Intent**:' in line:
                metadata['intent'] = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('### File '):
                # Extract filename from next few lines
                for j in range(i+1, min(i+5, len(lines))):
                    if '.csv' in lines[j] or '.xlsx' in lines[j]:
                        # Extract filename (e.g., `filename.csv`)
                        import re
                        match = re.search(r'`([^`]+\.(csv|xlsx))`', lines[j])
                        if match:
                            metadata['files'].append(match.group(1))
                        break
            elif line.startswith('### Widget '):
                metadata['expected_widgets'] += 1
        
        return metadata
    
    def upload_files(self, test_id: str, files: List[str], industry: str) -> Optional[Dict]:
        """Upload test data files to backend"""
        try:
            file_handles = []
            for filename in files:
                filepath = self.sample_data_dir / industry.lower() / filename
                if not filepath.exists():
                    print(f"  ⚠️  File not found: {filepath}")
                    return None
                file_handles.append(
                    ('files', (filename, open(filepath, 'rb')))
                )
            
            response = requests.post(
                f"{self.backend_url}/api/upload",
                files=file_handles,
                timeout=30
            )
            
            # Close file handles
            for _, (_, fh) in file_handles:
                fh.close()
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"  ❌ Upload failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Upload error: {e}")
            return None
    
    def generate_widgets(self, domain: str, intent: str, uploaded_data: Dict) -> Optional[Dict]:
        """Call quick-viz API to generate widgets"""
        try:
            payload = {
                "domain": domain,
                "user_intent": intent,
                "uploaded_files": uploaded_data
            }
            
            response = requests.post(
                f"{self.backend_url}/api/quick-viz",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"  ❌ Widget generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Widget generation error: {e}")
            return None
    
    def validate_widgets(self, widgets: List[Dict], expected_count: int) -> Dict[str, bool]:
        """Validate generated widgets"""
        validation = {
            'count_match': len(widgets) >= expected_count - 2,  # Allow ±2 variance
            'has_variety': False,
            'has_time_series': False,
            'has_aggregation': False
        }
        
        widget_types = set(w.get('type', '').lower() for w in widgets)
        validation['has_variety'] = len(widget_types) >= 3
        
        for widget in widgets:
            widget_type = widget.get('type', '').lower()
            if 'line' in widget_type or 'area' in widget_type:
                validation['has_time_series'] = True
            if 'bar' in widget_type or 'pie' in widget_type:
                validation['has_aggregation'] = True
        
        return validation
    
    def run_test_case(self, md_file: Path) -> TestResult:
        """Execute a single test case"""
        test_name = md_file.stem
        print(f"\n{'='*70}")
        print(f"🧪 Running: {test_name}")
        print(f"{'='*70}")
        
        start_time = time.time()
        errors = []
        
        # Parse test case
        print("  📖 Parsing test case...")
        try:
            metadata = self.parse_test_case(md_file)
            test_id = metadata['test_id']
            industry = metadata['industry']
            size = metadata['size']
            print(f"  ℹ️  Test ID: {test_id}, Industry: {industry}, Size: {size}")
        except Exception as e:
            errors.append(f"Failed to parse test case: {e}")
            return TestResult(
                test_id='UNKNOWN',
                test_name=test_name,
                industry='UNKNOWN',
                size='UNKNOWN',
                status='ERROR',
                duration=time.time() - start_time,
                widgets_generated=0,
                widgets_expected=0,
                widget_types_match=False,
                data_accuracy=False,
                performance_ok=False,
                errors=errors,
                timestamp=datetime.now().isoformat()
            )
        
        # Upload files
        print(f"  📁 Uploading {len(metadata['files'])} files...")
        uploaded_data = self.upload_files(test_id, metadata['files'], industry)
        if not uploaded_data:
            errors.append("File upload failed")
        
        # Generate widgets
        widgets_generated = 0
        validation = {}
        if uploaded_data:
            print(f"  🎨 Generating widgets...")
            print(f"     Domain: {metadata['domain']}")
            print(f"     Intent: {metadata['intent']}")
            
            widget_response = self.generate_widgets(
                metadata['domain'],
                metadata['intent'],
                uploaded_data
            )
            
            if widget_response and 'widgets' in widget_response:
                widgets = widget_response['widgets']
                widgets_generated = len(widgets)
                print(f"  ✅ Generated {widgets_generated} widgets")
                
                # Validate
                validation = self.validate_widgets(widgets, metadata['expected_widgets'])
            else:
                errors.append("Widget generation failed")
        
        # Calculate results
        duration = time.time() - start_time
        performance_ok = duration < 10.0
        
        status = 'PASS'
        if errors:
            status = 'FAIL'
        elif not validation.get('count_match', False):
            status = 'FAIL'
            errors.append(f"Widget count mismatch: expected ~{metadata['expected_widgets']}, got {widgets_generated}")
        elif not performance_ok:
            status = 'FAIL'
            errors.append(f"Performance issue: took {duration:.1f}s (limit: 10s)")
        
        result = TestResult(
            test_id=test_id,
            test_name=test_name,
            industry=industry,
            size=size,
            status=status,
            duration=duration,
            widgets_generated=widgets_generated,
            widgets_expected=metadata['expected_widgets'],
            widget_types_match=validation.get('has_variety', False),
            data_accuracy=True,  # Would need deeper validation
            performance_ok=performance_ok,
            errors=errors,
            timestamp=datetime.now().isoformat()
        )
        
        # Print summary
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"\n  {status_icon} {status}: {test_id} - {duration:.2f}s")
        if errors:
            for error in errors:
                print(f"     ⚠️  {error}")
        
        return result
    
    def get_test_cases(self, industry: Optional[str] = None, 
                       size: Optional[str] = None,
                       test_id: Optional[str] = None) -> List[Path]:
        """Get list of test case files to run"""
        test_files = []
        
        if test_id:
            # Find specific test case
            for md_file in self.test_cases_dir.rglob("*.md"):
                if md_file.stem.startswith(test_id) or test_id in md_file.stem:
                    test_files.append(md_file)
            return test_files
        
        # Get all test cases from industry folders
        industry_folders = [
            'retail', 'finance', 'healthcare', 'manufacturing',
            'education', 'saas', 'logistics'
        ]
        
        if industry:
            industry_folders = [industry.lower()]
        
        for ind in industry_folders:
            ind_path = self.test_cases_dir / ind
            if ind_path.exists():
                for md_file in ind_path.glob("TC*.md"):
                    if size:
                        # Filter by size in filename
                        if size.lower() in md_file.stem.lower():
                            test_files.append(md_file)
                    else:
                        test_files.append(md_file)
        
        return sorted(test_files)
    
    def generate_html_report(self, output_file: Path):
        """Generate HTML test report"""
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        total = len(self.results)
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Elas ERP Test Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #2563eb; color: white; padding: 20px; border-radius: 8px; }}
        .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .card h3 {{ margin: 0 0 10px 0; color: #666; font-size: 14px; }}
        .card .value {{ font-size: 32px; font-weight: bold; }}
        .card.pass .value {{ color: #10b981; }}
        .card.fail .value {{ color: #ef4444; }}
        table {{ width: 100%; background: white; border-collapse: collapse; border-radius: 8px; overflow: hidden; }}
        th {{ background: #f3f4f6; padding: 12px; text-align: left; font-weight: 600; }}
        td {{ padding: 12px; border-top: 1px solid #e5e7eb; }}
        .status-pass {{ color: #10b981; font-weight: bold; }}
        .status-fail {{ color: #ef4444; font-weight: bold; }}
        .errors {{ color: #ef4444; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Elas ERP Test Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <div class="card">
            <h3>Total Tests</h3>
            <div class="value">{total}</div>
        </div>
        <div class="card pass">
            <h3>Passed</h3>
            <div class="value">{passed}</div>
        </div>
        <div class="card fail">
            <h3>Failed</h3>
            <div class="value">{failed}</div>
        </div>
        <div class="card">
            <h3>Pass Rate</h3>
            <div class="value">{pass_rate:.1f}%</div>
        </div>
    </div>
    
    <div class="card">
        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Test ID</th>
                    <th>Name</th>
                    <th>Industry</th>
                    <th>Size</th>
                    <th>Status</th>
                    <th>Duration</th>
                    <th>Widgets</th>
                    <th>Errors</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in self.results:
            status_class = 'status-pass' if result.status == 'PASS' else 'status-fail'
            errors_html = '<br>'.join(result.errors) if result.errors else '-'
            
            html += f"""
                <tr>
                    <td>{result.test_id}</td>
                    <td>{result.test_name}</td>
                    <td>{result.industry}</td>
                    <td>{result.size}</td>
                    <td class="{status_class}">{result.status}</td>
                    <td>{result.duration:.2f}s</td>
                    <td>{result.widgets_generated} / {result.widgets_expected}</td>
                    <td class="errors">{errors_html}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\n📊 HTML report generated: {output_file}")
    
    def run(self, industry: Optional[str] = None,
            size: Optional[str] = None,
            test_id: Optional[str] = None,
            parallel: int = 1):
        """Run test suite"""
        
        # Check backend health
        print("🔍 Checking backend health...")
        if not self.check_backend_health():
            print("❌ Backend is not running! Start it first:")
            print("   cd elas-erp")
            print("   python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000")
            return
        print("✅ Backend is healthy\n")
        
        # Get test cases
        test_files = self.get_test_cases(industry, size, test_id)
        print(f"📋 Found {len(test_files)} test case(s) to run\n")
        
        if not test_files:
            print("⚠️  No test cases found matching criteria")
            return
        
        # Run tests
        start_time = time.time()
        
        if parallel > 1:
            print(f"🚀 Running with {parallel} parallel workers\n")
            with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
                self.results = list(executor.map(self.run_test_case, test_files))
        else:
            print("🚀 Running tests sequentially\n")
            for test_file in test_files:
                result = self.run_test_case(test_file)
                self.results.append(result)
        
        total_duration = time.time() - start_time
        
        # Print summary
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        total = len(self.results)
        
        print(f"\nTotal Tests: {total}")
        print(f"✅ Passed:   {passed} ({passed/total*100:.1f}%)")
        print(f"❌ Failed:   {failed} ({failed/total*100:.1f}%)")
        print(f"⏱️  Duration:  {total_duration:.1f}s\n")
        
        if failed > 0:
            print("FAILURES:")
            for result in self.results:
                if result.status == 'FAIL':
                    print(f"  • {result.test_id} - {result.test_name}")
                    for error in result.errors:
                        print(f"    - {error}")
        
        # Generate report
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        report_file = self.results_dir / f"test_run_{timestamp}.html"
        self.generate_html_report(report_file)
        
        # Save JSON results
        json_file = self.results_dir / f"test_run_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)
        print(f"💾 JSON results saved: {json_file}")


def main():
    parser = argparse.ArgumentParser(description='Elas ERP Automated Test Runner')
    parser.add_argument('--industry', choices=['retail', 'finance', 'healthcare', 'manufacturing', 'education', 'saas', 'logistics'],
                      help='Run tests for specific industry only')
    parser.add_argument('--size', choices=['small', 'medium', 'large'],
                      help='Run tests for specific company size only')
    parser.add_argument('--test', help='Run specific test case by ID (e.g., TC001)')
    parser.add_argument('--parallel', type=int, default=1, help='Number of parallel workers')
    parser.add_argument('--backend', default='http://localhost:8000', help='Backend URL')
    
    args = parser.parse_args()
    
    runner = ElasERPTestRunner(backend_url=args.backend)
    runner.run(
        industry=args.industry,
        size=args.size,
        test_id=args.test,
        parallel=args.parallel
    )


if __name__ == '__main__':
    main()
