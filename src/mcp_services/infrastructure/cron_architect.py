#!/usr/bin/env python3
"""
CRON Schedule Architect - Ultra-deep expertise in CRON jobs and scheduling systems
Includes macOS-specific knowledge and Python daemon alternatives
"""

from pathlib import Path
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import asyncio
from enum import Enum
import re

class ScheduleType(Enum):
    """Types of scheduling systems"""
    CRON = "cron"
    SYSTEMD = "systemd"
    LAUNCHD = "launchd"  # macOS
    PYTHON_DAEMON = "python_daemon"
    CELERY = "celery"
    APScheduler = "apscheduler"

class CronArchitect:
    """
    Ultra-specialized agent for CRON scheduling and job automation
    Expert in macOS limitations and Python alternatives
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "documentation" / "external_services" / "scheduling"
        self.research_output = self.base_path / "research_outputs" / "scheduling_solutions" 
        self.research_output.mkdir(parents=True, exist_ok=True)
        
        # Exhaustive CRON and scheduling knowledge
        self.knowledge_base = {
            "cron_syntax": {
                "fields": {
                    "minute": "0-59",
                    "hour": "0-23", 
                    "day_of_month": "1-31",
                    "month": "1-12",
                    "day_of_week": "0-7 (0 and 7 are Sunday)"
                },
                "special_characters": {
                    "*": "Any value",
                    ",": "Value list separator",
                    "-": "Range of values",
                    "/": "Step values",
                    "?": "No specific value (day fields)",
                    "L": "Last day (day fields)",
                    "W": "Weekday (day of month)",
                    "#": "Nth occurrence (day of week)"
                },
                "special_strings": {
                    "@reboot": "Run at startup",
                    "@yearly": "0 0 1 1 *",
                    "@annually": "0 0 1 1 *",
                    "@monthly": "0 0 1 * *",
                    "@weekly": "0 0 * * 0",
                    "@daily": "0 0 * * *",
                    "@midnight": "0 0 * * *",
                    "@hourly": "0 * * * *"
                },
                "examples": {
                    "*/5 * * * *": "Every 5 minutes",
                    "0 */2 * * *": "Every 2 hours",
                    "0 9-17 * * 1-5": "Every hour 9am-5pm weekdays",
                    "0 2 * * *": "Daily at 2am",
                    "0 0 * * 0": "Weekly on Sunday midnight",
                    "0 0 1 * *": "Monthly on the 1st",
                    "30 4 1,15 * *": "4:30am on 1st and 15th",
                    "0 0 * * 1#2": "Second Monday of month"
                }
            },
            
            "macos_issues": {
                "system_integrity_protection": {
                    "problem": "SIP blocks CRON from accessing many directories and Docker",
                    "symptoms": ["Operation not permitted", "Permission denied", "Docker commands fail"],
                    "solutions": [
                        "Use LaunchD instead of CRON",
                        "Run Python daemons with user permissions",
                        "Use Full Disk Access for critical paths"
                    ]
                },
                "sleep_behavior": {
                    "problem": "CRON jobs skip during sleep",
                    "solutions": [
                        "Use anacron for catch-up behavior",
                        "Implement Python daemon with schedule library",
                        "Use LaunchD with StartCalendarInterval"
                    ]
                },
                "path_issues": {
                    "problem": "Limited PATH in CRON environment",
                    "solution": "Always set PATH in crontab or script",
                    "example": "PATH=/usr/local/bin:/usr/bin:/bin"
                },
                "output_handling": {
                    "problem": "Mail system often not configured",
                    "solution": "Redirect output to log files",
                    "example": "* * * * * command >> /path/to/log 2>&1"
                }
            },
            
            "python_daemon_pattern": {
                "schedule_library": {
                    "installation": "pip install schedule",
                    "basic_usage": """
import schedule
import time

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
""",
                    "advantages": [
                        "Human-readable syntax",
                        "Handles sleep/wake",
                        "Full system permissions",
                        "Easy debugging"
                    ]
                },
                "daemon_template": """#!/usr/bin/env python3
import schedule
import time
import logging
import signal
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daemon.log'),
        logging.StreamHandler()
    ]
)

class ScheduleDaemon:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)
    
    def handle_signal(self, signum, frame):
        logging.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def job(self):
        logging.info("Executing scheduled job")
        # Job logic here
    
    def run(self):
        # Schedule jobs
        schedule.every(1).hours.do(self.job)
        schedule.every().day.at("02:00").do(self.job)
        
        logging.info("Daemon started")
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)
        
        logging.info("Daemon stopped")

if __name__ == "__main__":
    daemon = ScheduleDaemon()
    daemon.run()
""",
                "running_as_service": {
                    "screen": "screen -dmS daemon python3 daemon.py",
                    "nohup": "nohup python3 daemon.py &",
                    "systemd": "Create service file in /etc/systemd/system/",
                    "launchd": "Create plist in ~/Library/LaunchAgents/"
                }
            },
            
            "launchd_macos": {
                "advantages": [
                    "Native macOS scheduler",
                    "Survives reboots",
                    "Handles sleep/wake properly",
                    "Full user permissions"
                ],
                "plist_template": """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.fedjobadvisor.backup</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/script.py</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>2</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    
    <key>WorkingDirectory</key>
    <string>/path/to/project</string>
    
    <key>StandardOutPath</key>
    <string>/path/to/stdout.log</string>
    
    <key>StandardErrorPath</key>
    <string>/path/to/stderr.log</string>
    
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>""",
                "commands": {
                    "load": "launchctl load ~/Library/LaunchAgents/com.example.plist",
                    "unload": "launchctl unload ~/Library/LaunchAgents/com.example.plist",
                    "start": "launchctl start com.example",
                    "stop": "launchctl stop com.example",
                    "list": "launchctl list | grep com.example"
                }
            },
            
            "celery_pattern": {
                "installation": "pip install celery redis",
                "beat_schedule": """
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379')

app.conf.beat_schedule = {
    'backup-every-2-hours': {
        'task': 'tasks.backup',
        'schedule': crontab(minute=0, hour='*/2'),
    },
    'daily-report': {
        'task': 'tasks.daily_report',
        'schedule': crontab(hour=7, minute=30),
    },
}
""",
                "advantages": [
                    "Distributed task execution",
                    "Task retry mechanisms",
                    "Result backend",
                    "Web UI monitoring (Flower)",
                    "Horizontal scaling"
                ]
            },
            
            "error_recovery": {
                "missed_jobs": {
                    "anacron": "Runs missed jobs after system wake",
                    "custom_logic": "Track last run time and catch up",
                    "queuing": "Queue jobs and process when available"
                },
                "failure_handling": {
                    "retry_logic": "Implement exponential backoff",
                    "alerting": "Send notifications on failure",
                    "fallback": "Have backup execution method",
                    "logging": "Comprehensive error logging"
                },
                "monitoring": {
                    "healthchecks": "Use healthchecks.io for monitoring",
                    "custom_monitor": "Build monitoring daemon",
                    "metrics": "Track success/failure rates"
                }
            },
            
            "fed_job_advisor_schedules": {
                "data_collection": {
                    "frequency": "Every 10 minutes",
                    "cron": "*/10 * * * *",
                    "python": "schedule.every(10).minutes.do(collect_jobs)",
                    "critical": True
                },
                "backups": {
                    "incremental": "0 9,11,13,15,17,21,23 * * *",
                    "full": "0 2,19 * * *",
                    "python": """
schedule.every().day.at("02:00").do(full_backup)
schedule.every().day.at("19:00").do(full_backup)
for hour in [9,11,13,15,17,21,23]:
    schedule.every().day.at(f"{hour:02d}:00").do(incremental_backup)
"""
                },
                "reports": {
                    "daily": "0 7 * * *",
                    "weekly": "0 8 * * 1",
                    "monthly": "0 9 1 * *"
                },
                "maintenance": {
                    "cleanup": "0 3 * * 0",
                    "vacuum": "0 4 * * 0",
                    "reindex": "0 5 1 * *"
                }
            }
        }
    
    def parse_cron_expression(self, expression: str) -> Dict[str, Any]:
        """
        Parse and validate CRON expression
        """
        parts = expression.strip().split()
        
        # Handle special strings
        if expression.startswith("@"):
            special_map = self.knowledge_base["cron_syntax"]["special_strings"]
            if expression in special_map:
                return {
                    "valid": True,
                    "special": expression,
                    "expanded": special_map[expression],
                    "description": self._describe_special(expression)
                }
        
        # Validate standard cron (5 or 6 fields)
        if len(parts) not in [5, 6]:
            return {
                "valid": False,
                "error": f"Invalid number of fields: {len(parts)} (expected 5 or 6)"
            }
        
        field_names = ["minute", "hour", "day_of_month", "month", "day_of_week"]
        if len(parts) == 6:
            field_names.insert(0, "second")
        
        parsed = {
            "valid": True,
            "fields": {},
            "description": ""
        }
        
        for i, (field_name, value) in enumerate(zip(field_names, parts)):
            parsed["fields"][field_name] = value
        
        parsed["description"] = self._describe_cron(parsed["fields"])
        parsed["next_runs"] = self._calculate_next_runs(expression, 5)
        
        return parsed
    
    def _describe_special(self, special: str) -> str:
        """Describe special CRON string"""
        descriptions = {
            "@reboot": "Run at system startup",
            "@yearly": "Run once a year at midnight on January 1st",
            "@annually": "Run once a year at midnight on January 1st",
            "@monthly": "Run once a month at midnight on the 1st",
            "@weekly": "Run once a week at midnight on Sunday",
            "@daily": "Run once a day at midnight",
            "@midnight": "Run once a day at midnight",
            "@hourly": "Run once an hour at the beginning of the hour"
        }
        return descriptions.get(special, "Unknown special string")
    
    def _describe_cron(self, fields: Dict[str, str]) -> str:
        """Generate human-readable description of CRON expression"""
        minute = fields.get("minute", "*")
        hour = fields.get("hour", "*")
        day = fields.get("day_of_month", "*")
        month = fields.get("month", "*")
        dow = fields.get("day_of_week", "*")
        
        # Common patterns
        if minute == "0" and hour == "*":
            return "Every hour on the hour"
        elif minute == "*/5":
            return "Every 5 minutes"
        elif minute == "0" and hour == "0":
            return "Daily at midnight"
        elif minute == "0" and hour.isdigit():
            return f"Daily at {hour}:00"
        elif minute.isdigit() and hour.isdigit():
            return f"Daily at {hour}:{minute:0>2}"
        else:
            return f"At {minute} minutes past {hour} hours on day {day} of month {month}, day of week {dow}"
    
    def _calculate_next_runs(self, expression: str, count: int = 5) -> List[str]:
        """Calculate next run times (simplified)"""
        # This would use a proper CRON parser in production
        now = datetime.now()
        runs = []
        
        # Simple examples for common patterns
        if expression == "*/5 * * * *":
            for i in range(count):
                next_time = now + timedelta(minutes=5 * (i + 1))
                runs.append(next_time.strftime("%Y-%m-%d %H:%M"))
        elif expression == "0 * * * *":
            for i in range(count):
                next_time = now.replace(minute=0, second=0) + timedelta(hours=i+1)
                runs.append(next_time.strftime("%Y-%m-%d %H:%M"))
        else:
            runs = ["Use a CRON calculator for complex expressions"]
        
        return runs
    
    async def diagnose_cron_failure(self, error_log: str, system: str = "macos") -> Dict[str, Any]:
        """
        Diagnose CRON job failures with system-specific knowledge
        """
        timestamp = datetime.now().isoformat()
        
        diagnosis = {
            "timestamp": timestamp,
            "system": system,
            "issues_detected": [],
            "solutions": [],
            "alternative_approaches": []
        }
        
        error_lower = error_log.lower()
        
        # macOS specific issues
        if system == "macos":
            if "operation not permitted" in error_lower or "permission denied" in error_lower:
                diagnosis["issues_detected"].append("System Integrity Protection blocking CRON")
                diagnosis["solutions"].extend([
                    "Grant Full Disk Access to /usr/sbin/cron in System Preferences",
                    "Use LaunchD instead of CRON",
                    "Run Python daemon with user permissions"
                ])
                diagnosis["alternative_approaches"].append({
                    "method": "Python Daemon",
                    "reason": "Bypasses SIP restrictions",
                    "implementation": self.knowledge_base["python_daemon_pattern"]["daemon_template"]
                })
            
            if "docker" in error_lower:
                diagnosis["issues_detected"].append("CRON cannot access Docker on macOS")
                diagnosis["solutions"].extend([
                    "Docker Desktop must be running",
                    "Use Python daemon that checks Docker status",
                    "Add Docker to PATH in crontab"
                ])
        
        # Common issues
        if "command not found" in error_lower:
            diagnosis["issues_detected"].append("PATH not set in CRON environment")
            diagnosis["solutions"].append("Add PATH=/usr/local/bin:/usr/bin:/bin to crontab")
        
        if "no such file" in error_lower:
            diagnosis["issues_detected"].append("Script path may be relative or incorrect")
            diagnosis["solutions"].append("Use absolute paths in CRON jobs")
        
        if "mail" in error_lower:
            diagnosis["issues_detected"].append("Mail system not configured")
            diagnosis["solutions"].append("Redirect output: command >> /path/to/log 2>&1")
        
        # Save diagnosis
        output_file = self.research_output / f"{timestamp}_cron_diagnosis.json"
        with open(output_file, 'w') as f:
            json.dump(diagnosis, f, indent=2)
        
        return diagnosis
    
    async def convert_cron_to_python(self, crontab_content: str) -> str:
        """
        Convert crontab to Python daemon script
        """
        lines = crontab_content.strip().split('\n')
        jobs = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse CRON job
                parts = line.split(None, 5)
                if len(parts) >= 6:
                    schedule_parts = parts[:5]
                    command = parts[5]
                    
                    # Convert to Python schedule
                    python_schedule = self._cron_to_python_schedule(schedule_parts)
                    jobs.append({
                        "cron": ' '.join(schedule_parts),
                        "command": command,
                        "python": python_schedule
                    })
        
        # Generate Python daemon script
        script = """#!/usr/bin/env python3
\"\"\"
Auto-generated Python daemon to replace CRON jobs
Generated: {timestamp}
\"\"\"

import schedule
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('schedule_daemon.log'),
        logging.StreamHandler()
    ]
)

def run_command(command):
    \"\"\"Execute shell command\"\"\"
    try:
        logging.info(f"Executing: {{command}}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Success: {{command}}")
        else:
            logging.error(f"Failed: {{command}}\\n{{result.stderr}}")
    except Exception as e:
        logging.error(f"Error running {{command}}: {{e}}")

# Schedule jobs
""".format(timestamp=datetime.now().isoformat())
        
        for job in jobs:
            script += f"""
# Original CRON: {job['cron']}
{job['python']}
"""
        
        script += """
def main():
    logging.info("Schedule daemon started")
    logging.info(f"Scheduled jobs: {len(schedule.jobs)}")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Daemon stopped by user")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
"""
        
        return script
    
    def _cron_to_python_schedule(self, cron_parts: List[str]) -> str:
        """Convert CRON schedule to Python schedule syntax"""
        minute, hour, dom, month, dow = cron_parts
        
        # Common patterns
        if minute == "0" and hour == "*":
            return 'schedule.every().hour.at(":00").do(run_command, command)'
        elif minute == "*/5":
            return 'schedule.every(5).minutes.do(run_command, command)'
        elif minute == "0" and hour.isdigit():
            return f'schedule.every().day.at("{hour:0>2}:00").do(run_command, command)'
        elif minute.isdigit() and hour.isdigit():
            return f'schedule.every().day.at("{hour:0>2}:{minute:0>2}").do(run_command, command)'
        else:
            return f'# Complex schedule - needs manual conversion: {" ".join(cron_parts)}'
    
    async def generate_scheduling_guide(self, platform: str = "macos") -> str:
        """
        Generate comprehensive scheduling guide for specific platform
        """
        if platform == "macos":
            guide = """# macOS Scheduling Guide - CRON Alternatives

## Why CRON Fails on macOS

### System Integrity Protection (SIP)
- Blocks CRON from accessing protected directories
- Prevents Docker access
- Restricts file system operations

### Common Errors
```
Operation not permitted
Permission denied  
docker: command not found
```

## Solution 1: Python Daemon (RECOMMENDED)

### Installation
```bash
pip install schedule
```

### Basic Daemon Script
```python
#!/usr/bin/env python3
import schedule
import time
import subprocess
import os

def backup_job():
    os.system('./backup.sh')

# Schedule jobs
schedule.every(2).hours.do(backup_job)
schedule.every().day.at("02:00").do(backup_job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Run as Background Service
```bash
# Using nohup
nohup python3 daemon.py > daemon.log 2>&1 &

# Using screen
screen -dmS scheduler python3 daemon.py

# Check if running
ps aux | grep daemon.py
```

## Solution 2: LaunchD (Native macOS)

### Create Launch Agent
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourapp.scheduler</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/script.py</string>
    </array>
    
    <key>StartInterval</key>
    <integer>3600</integer> <!-- Every hour -->
    
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

### Install and Manage
```bash
# Save to ~/Library/LaunchAgents/com.yourapp.scheduler.plist

# Load agent
launchctl load ~/Library/LaunchAgents/com.yourapp.scheduler.plist

# Start immediately
launchctl start com.yourapp.scheduler

# Check status
launchctl list | grep yourapp

# Unload
launchctl unload ~/Library/LaunchAgents/com.yourapp.scheduler.plist
```

## Solution 3: Docker Cron Container

### Dockerfile
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron

COPY crontab /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron

RUN crontab /etc/cron.d/app-cron

CMD ["cron", "-f"]
```

### Docker Compose
```yaml
version: '3'
services:
  scheduler:
    build: .
    volumes:
      - ./scripts:/scripts
      - /var/run/docker.sock:/var/run/docker.sock
```

## Monitoring & Debugging

### Log Everything
```python
import logging

logging.basicConfig(
    filename='scheduler.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
```

### Health Checks
```python
def health_check():
    # Ping monitoring service
    requests.get('https://hc-ping.com/your-uuid')
```

### Error Recovery
```python
def safe_job():
    try:
        risky_operation()
    except Exception as e:
        logging.error(f"Job failed: {e}")
        send_alert(str(e))
        # Retry logic
```

## Fed Job Advisor Specific Schedule

### Data Collection (Every 10 minutes)
```python
schedule.every(10).minutes.do(collect_federal_jobs)
```

### Backups (Multiple times daily)
```python
# Incremental
for hour in [9, 11, 13, 15, 17, 21, 23]:
    schedule.every().day.at(f"{hour:02d}:00").do(incremental_backup)

# Full
schedule.every().day.at("02:00").do(full_backup)
schedule.every().day.at("19:00").do(full_backup)
```

### Reports (Daily/Weekly/Monthly)
```python
schedule.every().day.at("07:00").do(daily_report)
schedule.every().monday.at("08:00").do(weekly_report)
schedule.every().month.do(monthly_report)
```

## Troubleshooting

### CRON Not Working?
1. Check system logs: `log show --predicate 'process == "cron"' --last 1h`
2. Verify permissions: `ls -la /usr/sbin/cron`
3. Test in foreground first
4. Use absolute paths everywhere
5. Set PATH in script

### Python Daemon Issues?
1. Check if running: `ps aux | grep python`
2. Review logs: `tail -f daemon.log`
3. Test imports: `python3 -c "import schedule"`
4. Verify Python path: `which python3`

### LaunchD Problems?
1. Validate plist: `plutil -lint ~/Library/LaunchAgents/com.yourapp.plist`
2. Check logs: `log show --predicate 'process == "launchd"' --last 1h`
3. Verify paths are absolute
4. Check file permissions

---
*Generated by CRON Schedule Architect Agent*
"""
        else:
            guide = "Platform-specific guide not available"
        
        return guide

# CLI interface
if __name__ == "__main__":
    import sys
    
    architect = CronArchitect()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "parse":
            if len(sys.argv) > 2:
                expression = sys.argv[2]
                result = architect.parse_cron_expression(expression)
                print(json.dumps(result, indent=2))
        
        elif command == "diagnose":
            if len(sys.argv) > 2:
                error = sys.argv[2]
                result = asyncio.run(architect.diagnose_cron_failure(error))
                print(json.dumps(result, indent=2))
        
        elif command == "convert":
            if len(sys.argv) > 2:
                with open(sys.argv[2], 'r') as f:
                    crontab = f.read()
                script = asyncio.run(architect.convert_cron_to_python(crontab))
                print(script)
        
        elif command == "guide":
            platform = sys.argv[2] if len(sys.argv) > 2 else "macos"
            guide = asyncio.run(architect.generate_scheduling_guide(platform))
            print(guide)
    else:
        print("CRON Schedule Architect")
        print("Commands:")
        print("  parse <expression> - Parse CRON expression")
        print("  diagnose <error> - Diagnose CRON failure")
        print("  convert <crontab> - Convert to Python daemon")
        print("  guide [platform] - Generate scheduling guide")