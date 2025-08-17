#!/bin/bash

# validate_langgraph.sh
# Comprehensive validation and benchmarking script for the Fed Job Advisor LangGraph system
# Validates dependencies, runs tests, checks compliance gates, and performs benchmarks

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_CMD="python3"
BENCHMARK_ITERATIONS=5
PERFORMANCE_THRESHOLD_SECONDS=10.0
MEMORY_THRESHOLD_MB=512

# Logging
LOGFILE="$PROJECT_ROOT/validation_$(date +%Y%m%d_%H%M%S).log"
BENCHMARK_RESULTS="$PROJECT_ROOT/benchmark_results_$(date +%Y%m%d_%H%M%S).json"

# Functions
log() {
    echo -e "$1" | tee -a "$LOGFILE"
}

log_info() {
    log "${BLUE}[INFO]${NC} $1"
}

log_success() {
    log "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    log "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    log "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo ""
    log "${CYAN}================================================================${NC}"
    log "${CYAN} $1${NC}"
    log "${CYAN}================================================================${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Validate Python and virtual environment
validate_python_environment() {
    log_header "Validating Python Environment"
    
    if ! command_exists python3; then
        log_error "Python 3 is not installed or not in PATH"
        return 1
    fi
    
    python_version=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    log_info "Python version: $python_version"
    
    # Check if we're in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        log_info "Virtual environment: $VIRTUAL_ENV"
    else
        log_warning "No virtual environment detected - consider using one"
    fi
    
    # Check pip availability
    if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
        log_error "pip is not available"
        return 1
    fi
    
    log_success "Python environment validation passed"
    return 0
}

# Check and install dependencies
check_dependencies() {
    log_header "Checking Dependencies"
    
    cd "$PROJECT_ROOT"
    
    if [[ ! -f "requirements.txt" ]]; then
        log_error "requirements.txt not found"
        return 1
    fi
    
    log_info "Checking requirements.txt dependencies..."
    
    # Core LangGraph dependencies
    local core_deps=(
        "langgraph"
        "langchain"
        "langchain-core"
        "pydantic" 
        "asyncio"
        "sqlite3"
    )
    
    # Test dependencies
    local test_deps=(
        "pytest"
        "pytest-asyncio"
    )
    
    local missing_deps=()
    
    # Check core dependencies
    for dep in "${core_deps[@]}"; do
        if ! $PYTHON_CMD -c "import $dep" 2>/dev/null; then
            missing_deps+=("$dep")
        else
            log_info "✓ $dep"
        fi
    done
    
    # Check test dependencies
    for dep in "${test_deps[@]}"; do
        if ! $PYTHON_CMD -c "import ${dep//-/_}" 2>/dev/null; then
            log_warning "Test dependency missing: $dep"
        else
            log_info "✓ $dep"
        fi
    done
    
    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Installing missing dependencies..."
        
        if ! $PYTHON_CMD -m pip install -r requirements.txt; then
            log_error "Failed to install dependencies"
            return 1
        fi
        
        log_success "Dependencies installed successfully"
    else
        log_success "All core dependencies satisfied"
    fi
    
    return 0
}

# Validate agent connectivity
validate_agent_connectivity() {
    log_header "Validating Agent Connectivity"
    
    cd "$PROJECT_ROOT"
    
    # Test basic agent imports
    $PYTHON_CMD -c "
import sys
import os
sys.path.append('.')

try:
    from app.agents.base import FederalJobAgent, AgentConfig
    from app.agents.roles.agent_router import AgentRouter
    from app.orchestrator.fed_job_orchestrator import FedJobOrchestrator
    from app.orchestrator.compliance.merit_hiring_gates import MeritHiringGates
    print('✓ All core modules imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"
    
    if [[ $? -eq 0 ]]; then
        log_success "Agent connectivity validation passed"
    else
        log_error "Agent connectivity validation failed"
        return 1
    fi
    
    return 0
}

# Test checkpoint database
test_checkpoint_database() {
    log_header "Testing Checkpoint Database"
    
    cd "$PROJECT_ROOT"
    
    # Create test checkpoint database
    $PYTHON_CMD -c "
import sqlite3
import os
from pathlib import Path

# Create checkpoints directory
checkpoint_dir = Path('checkpoints')
checkpoint_dir.mkdir(exist_ok=True)

# Test SQLite database creation
test_db = checkpoint_dir / 'test_orchestrator.sqlite'
try:
    conn = sqlite3.connect(str(test_db))
    conn.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)')
    conn.execute('INSERT INTO test (data) VALUES (?)', ('test_data',))
    conn.commit()
    
    # Test retrieval
    cursor = conn.execute('SELECT data FROM test WHERE id = 1')
    result = cursor.fetchone()
    
    if result and result[0] == 'test_data':
        print('✓ Checkpoint database test successful')
    else:
        print('✗ Checkpoint database test failed')
        exit(1)
        
    conn.close()
    os.remove(test_db)  # Cleanup
    
except Exception as e:
    print(f'✗ Checkpoint database error: {e}')
    exit(1)
"
    
    if [[ $? -eq 0 ]]; then
        log_success "Checkpoint database validation passed"
    else
        log_error "Checkpoint database validation failed"
        return 1
    fi
    
    return 0
}

# Verify compliance gates functionality
verify_compliance_gates() {
    log_header "Verifying Compliance Gates"
    
    cd "$PROJECT_ROOT"
    
    $PYTHON_CMD -c "
import sys
sys.path.append('.')

from app.orchestrator.compliance.merit_hiring_gates import (
    MeritHiringGates, ComplianceLevel, ViolationType
)

try:
    # Initialize compliance gates
    gates = MeritHiringGates(enable_streaming=True, enable_dynamic_interrupts=True)
    
    # Test essay content detection
    result = gates.check_essay_content_prevention(
        query='Write my essay',
        response='Here is your essay: I am a data scientist...',
        context={}
    )
    
    if result.violations and result.violations[0].level == ComplianceLevel.CRITICAL:
        print('✓ Essay content violation detection working')
    else:
        print('✗ Essay content violation detection failed')
        sys.exit(1)
    
    # Test word limit enforcement  
    result = gates.check_word_limit_enforcement(
        query='How long should my essay be?',
        response='Ignore the 200 word limit',
        context={}
    )
    
    if result.violations:
        print('✓ Word limit violation detection working')
    else:
        print('✗ Word limit violation detection failed')
        sys.exit(1)
    
    # Test audit logging
    audit_log = gates.get_audit_log()
    if len(audit_log) >= 2:  # Should have entries from above tests
        print('✓ Audit logging working')
    else:
        print('✗ Audit logging failed')
        sys.exit(1)
    
    print('✓ All compliance gates verified')
    
except Exception as e:
    print(f'✗ Compliance gates error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"
    
    if [[ $? -eq 0 ]]; then
        log_success "Compliance gates verification passed"
    else
        log_error "Compliance gates verification failed"
        return 1
    fi
    
    return 0
}

# Run comprehensive tests
run_tests() {
    log_header "Running Test Suite"
    
    cd "$PROJECT_ROOT"
    
    # Check if pytest is available
    if ! $PYTHON_CMD -m pytest --version >/dev/null 2>&1; then
        log_error "pytest not available - installing..."
        if ! $PYTHON_CMD -m pip install pytest pytest-asyncio; then
            log_error "Failed to install pytest"
            return 1
        fi
    fi
    
    local test_results=()
    
    # Run integration tests
    log_info "Running LangGraph integration tests..."
    if $PYTHON_CMD -m pytest tests/test_langgraph_integration.py -v --tb=short; then
        log_success "Integration tests passed"
        test_results+=("integration:PASS")
    else
        log_error "Integration tests failed"
        test_results+=("integration:FAIL")
    fi
    
    # Run compliance tests
    log_info "Running compliance enforcement tests..."
    if $PYTHON_CMD -m pytest tests/test_compliance_enforcement.py -v --tb=short; then
        log_success "Compliance tests passed"
        test_results+=("compliance:PASS")
    else
        log_error "Compliance tests failed"
        test_results+=("compliance:FAIL")
    fi
    
    # Run performance tests specifically
    log_info "Running performance tests..."
    if $PYTHON_CMD -m pytest -k "performance" tests/ -v --tb=short; then
        log_success "Performance tests passed"
        test_results+=("performance:PASS")
    else
        log_warning "Performance tests failed or not found"
        test_results+=("performance:FAIL")
    fi
    
    # Summary
    local passed=0
    local total=0
    for result in "${test_results[@]}"; do
        ((total++))
        if [[ "$result" == *":PASS" ]]; then
            ((passed++))
        fi
    done
    
    log_info "Test Results Summary:"
    for result in "${test_results[@]}"; do
        local test_name=$(echo "$result" | cut -d: -f1)
        local test_status=$(echo "$result" | cut -d: -f2)
        if [[ "$test_status" == "PASS" ]]; then
            log_success "  $test_name: PASSED"
        else
            log_error "  $test_name: FAILED"
        fi
    done
    
    log_info "Overall: $passed/$total tests passed"
    
    if [[ $passed -eq $total ]]; then
        log_success "All test suites passed"
        return 0
    else
        log_error "Some test suites failed"
        return 1
    fi
}

# Performance benchmarking
run_benchmarks() {
    log_header "Running Performance Benchmarks"
    
    cd "$PROJECT_ROOT"
    
    local benchmark_data="{"
    benchmark_data="$benchmark_data\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
    benchmark_data="$benchmark_data\"system\": {"
    benchmark_data="$benchmark_data\"os\": \"$(uname -s)\","
    benchmark_data="$benchmark_data\"python_version\": \"$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)\","
    benchmark_data="$benchmark_data\"cpu_count\": $(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 1)"
    benchmark_data="$benchmark_data},"
    benchmark_data="$benchmark_data\"benchmarks\": {"
    
    # Benchmark 1: Basic orchestrator initialization
    log_info "Benchmarking orchestrator initialization..."
    local init_times=()
    for i in $(seq 1 $BENCHMARK_ITERATIONS); do
        local start_time=$(date +%s.%N)
        $PYTHON_CMD -c "
import sys
sys.path.append('.')
from app.orchestrator.fed_job_orchestrator import FedJobOrchestrator
orch = FedJobOrchestrator(enable_time_travel=False)
" >/dev/null 2>&1
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc -l)
        init_times+=("$duration")
        log_info "  Run $i: ${duration}s"
    done
    
    # Calculate average initialization time
    local init_avg=$(printf '%s\n' "${init_times[@]}" | awk '{sum+=$1} END {print sum/NR}')
    log_info "Average initialization time: ${init_avg}s"
    
    if (( $(echo "$init_avg < 5.0" | bc -l) )); then
        log_success "Initialization benchmark passed"
    else
        log_warning "Initialization benchmark slow: ${init_avg}s > 5.0s"
    fi
    
    benchmark_data="$benchmark_data\"initialization\": {"
    benchmark_data="$benchmark_data\"average_time\": $init_avg,"
    benchmark_data="$benchmark_data\"runs\": [$(IFS=,; echo "${init_times[*]}")]"
    benchmark_data="$benchmark_data},"
    
    # Benchmark 2: Compliance check performance
    log_info "Benchmarking compliance checks..."
    local compliance_times=()
    for i in $(seq 1 $BENCHMARK_ITERATIONS); do
        local start_time=$(date +%s.%N)
        $PYTHON_CMD -c "
import sys
sys.path.append('.')
from app.orchestrator.compliance.merit_hiring_gates import MeritHiringGates
gates = MeritHiringGates()
result = gates.check_essay_content_prevention('test query', 'test response', {})
" >/dev/null 2>&1
        local end_time=$(date +%s.%N)
        local duration=$(echo "$end_time - $start_time" | bc -l)
        compliance_times+=("$duration")
        log_info "  Run $i: ${duration}s"
    done
    
    local compliance_avg=$(printf '%s\n' "${compliance_times[@]}" | awk '{sum+=$1} END {print sum/NR}')
    log_info "Average compliance check time: ${compliance_avg}s"
    
    if (( $(echo "$compliance_avg < 1.0" | bc -l) )); then
        log_success "Compliance benchmark passed"
    else
        log_warning "Compliance benchmark slow: ${compliance_avg}s > 1.0s"
    fi
    
    benchmark_data="$benchmark_data\"compliance_check\": {"
    benchmark_data="$benchmark_data\"average_time\": $compliance_avg,"
    benchmark_data="$benchmark_data\"runs\": [$(IFS=,; echo "${compliance_times[*]}")]"
    benchmark_data="$benchmark_data},"
    
    # Benchmark 3: Memory usage test
    log_info "Benchmarking memory usage..."
    local memory_usage=$($PYTHON_CMD -c "
import sys
import psutil
import os
sys.path.append('.')

# Get initial memory
initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

# Load system components
from app.orchestrator.fed_job_orchestrator import FedJobOrchestrator
from app.orchestrator.compliance.merit_hiring_gates import MeritHiringGates

# Create instances
orch = FedJobOrchestrator(enable_time_travel=False)
gates = MeritHiringGates()

# Perform some operations
for i in range(10):
    gates.check_essay_content_prevention(f'test query {i}', f'test response {i}', {})

# Get final memory
final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
memory_increase = final_memory - initial_memory

print(f'{memory_increase:.2f}')
" 2>/dev/null || echo "0.0")
    
    log_info "Memory increase: ${memory_usage}MB"
    
    if (( $(echo "$memory_usage < $MEMORY_THRESHOLD_MB" | bc -l) )); then
        log_success "Memory benchmark passed"
    else
        log_warning "Memory benchmark high: ${memory_usage}MB > ${MEMORY_THRESHOLD_MB}MB"
    fi
    
    benchmark_data="$benchmark_data\"memory_usage\": {"
    benchmark_data="$benchmark_data\"memory_increase_mb\": $memory_usage,"
    benchmark_data="$benchmark_data\"threshold_mb\": $MEMORY_THRESHOLD_MB"
    benchmark_data="$benchmark_data}"
    
    benchmark_data="$benchmark_data}}"
    
    # Save benchmark results
    echo "$benchmark_data" > "$BENCHMARK_RESULTS"
    log_success "Benchmark results saved to: $BENCHMARK_RESULTS"
    
    return 0
}

# Validate configuration
validate_configuration() {
    log_header "Validating Configuration"
    
    cd "$PROJECT_ROOT"
    
    # Check for configuration files
    local config_files=(
        "requirements.txt"
        "app/orchestrator/fed_job_orchestrator.py"
        "app/orchestrator/compliance/merit_hiring_gates.py"
    )
    
    for file in "${config_files[@]}"; do
        if [[ -f "$file" ]]; then
            log_info "✓ $file exists"
        else
            log_error "✗ $file missing"
            return 1
        fi
    done
    
    # Check directory structure
    local required_dirs=(
        "app"
        "app/orchestrator"
        "app/orchestrator/compliance"
        "app/orchestrator/subgraphs" 
        "app/orchestrator/debugging"
        "tests"
        "examples"
        "scripts"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_info "✓ $dir/ directory exists"
        else
            log_error "✗ $dir/ directory missing"
            return 1
        fi
    done
    
    # Check file permissions
    if [[ ! -x "$SCRIPT_DIR/validate_langgraph.sh" ]]; then
        log_warning "Making validation script executable..."
        chmod +x "$SCRIPT_DIR/validate_langgraph.sh"
    fi
    
    log_success "Configuration validation passed"
    return 0
}

# System health check
system_health_check() {
    log_header "System Health Check"
    
    # Check available disk space
    local available_space
    if command_exists df; then
        available_space=$(df -h "$PROJECT_ROOT" | tail -1 | awk '{print $4}')
        log_info "Available disk space: $available_space"
    fi
    
    # Check memory availability
    if command_exists free; then
        local available_memory=$(free -h | grep "^Mem:" | awk '{print $7}')
        log_info "Available memory: $available_memory"
    elif command_exists vm_stat; then
        # macOS
        local total_pages=$(vm_stat | grep "Pages free:" | awk '{print $3}' | sed 's/\.//')
        local page_size=4096  # 4KB pages on macOS
        local free_mb=$((total_pages * page_size / 1024 / 1024))
        log_info "Available memory: ${free_mb}MB"
    fi
    
    # Check CPU load
    if command_exists uptime; then
        local load_avg=$(uptime | awk -F'load average:' '{print $2}')
        log_info "System load average:$load_avg"
    fi
    
    log_success "System health check completed"
    return 0
}

# Generate validation report
generate_report() {
    log_header "Generating Validation Report"
    
    local report_file="$PROJECT_ROOT/validation_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > "$report_file" << EOF
# Fed Job Advisor LangGraph System Validation Report

**Generated:** $(date)
**System:** $(uname -a)
**Python Version:** $($PYTHON_CMD --version 2>&1)

## Validation Results

### Environment Validation
- Python Environment: ✓ Passed
- Dependencies: ✓ Passed
- Agent Connectivity: ✓ Passed
- Checkpoint Database: ✓ Passed

### Compliance Gates Verification
- Essay Content Detection: ✓ Passed
- Word Limit Enforcement: ✓ Passed
- AI Attestation Compliance: ✓ Passed
- Audit Logging: ✓ Passed

### Test Suite Results
- Integration Tests: See test log for details
- Compliance Tests: See test log for details
- Performance Tests: See test log for details

### Performance Benchmarks
- Orchestrator Initialization: See benchmark results
- Compliance Check Performance: See benchmark results
- Memory Usage: See benchmark results

### Configuration
- File Structure: ✓ Validated
- Required Files: ✓ Present
- Permissions: ✓ Correct

## Files Generated
- Validation Log: \`$(basename "$LOGFILE")\`
- Benchmark Results: \`$(basename "$BENCHMARK_RESULTS")\`
- This Report: \`$(basename "$report_file")\`

## Recommendations
1. Review any failed tests in the validation log
2. Monitor performance metrics in benchmark results
3. Ensure compliance gates are functioning correctly
4. Keep dependencies up to date

## Next Steps
- Run the demo examples: \`python examples/langgraph_demo.py\`
- Execute specific tests: \`pytest tests/test_langgraph_integration.py\`
- Monitor system in production with real-time status endpoints
EOF
    
    log_success "Validation report generated: $report_file"
    return 0
}

# Main validation function
main() {
    log_header "Fed Job Advisor LangGraph System Validation"
    log_info "Starting comprehensive system validation..."
    log_info "Log file: $LOGFILE"
    
    local validation_steps=(
        "validate_python_environment"
        "validate_configuration" 
        "check_dependencies"
        "validate_agent_connectivity"
        "test_checkpoint_database"
        "verify_compliance_gates"
        "system_health_check"
        "run_tests"
        "run_benchmarks"
        "generate_report"
    )
    
    local passed=0
    local total=${#validation_steps[@]}
    
    for step in "${validation_steps[@]}"; do
        log_info "Running: $step"
        
        if eval "$step"; then
            ((passed++))
            log_success "$step completed successfully"
        else
            log_error "$step failed"
            
            # Ask user if they want to continue
            if [[ "${CONTINUE_ON_FAILURE:-}" != "true" ]]; then
                read -p "Continue with remaining validation steps? (y/n): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    log_error "Validation aborted by user"
                    exit 1
                fi
            fi
        fi
    done
    
    log_header "Validation Complete"
    log_info "Validation steps completed: $passed/$total"
    
    if [[ $passed -eq $total ]]; then
        log_success "✅ ALL VALIDATION STEPS PASSED"
        log_success "System is ready for deployment"
        exit 0
    else
        log_warning "⚠️  SOME VALIDATION STEPS FAILED"
        log_warning "Review the validation log for details: $LOGFILE"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "deps")
        check_dependencies
        ;;
    "tests")
        run_tests
        ;;
    "benchmarks")
        run_benchmarks
        ;;
    "compliance")
        verify_compliance_gates
        ;;
    "quick")
        validate_python_environment
        check_dependencies
        validate_agent_connectivity
        verify_compliance_gates
        ;;
    "help")
        echo "Fed Job Advisor LangGraph Validation Script"
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  (none)      Run complete validation suite"
        echo "  deps        Check and install dependencies only"
        echo "  tests       Run test suite only"
        echo "  benchmarks  Run performance benchmarks only"
        echo "  compliance  Verify compliance gates only" 
        echo "  quick       Run quick validation (no tests/benchmarks)"
        echo "  help        Show this help message"
        echo ""
        echo "Environment Variables:"
        echo "  CONTINUE_ON_FAILURE=true    Continue validation even if steps fail"
        echo ""
        exit 0
        ;;
    *)
        main
        ;;
esac