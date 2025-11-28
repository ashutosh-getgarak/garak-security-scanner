#!/usr/bin/env python3
"""
Garak Security Scanner - GitHub Action Entrypoint
Executes AI security scans against target endpoints
"""

import os
import sys
import time
import json
import requests
from typing import Dict, Optional, List


class GarakScanner:
    def __init__(self):
        self.api_key = os.getenv('INPUT_API_KEY', '').strip()
        self.endpoint = os.getenv('INPUT_ENDPOINT', '').strip()
        self.model_id = os.getenv('INPUT_MODEL_ID', '').strip()
        self.probes = os.getenv('INPUT_PROBES', 'dan,security,privacy,toxicity').strip()
        self.generator_mode = os.getenv('INPUT_GENERATOR_MODE', 'rest').strip()
        self.parallel_attempts = int(os.getenv('INPUT_PARALLEL_ATTEMPTS', '4'))
        self.response_json_path = os.getenv('INPUT_RESPONSE_JSON_PATH', '$.content[0].text').strip()
        self.target_api_key = os.getenv('INPUT_TARGET_API_KEY', '').strip()
        self.timeout_minutes = int(os.getenv('INPUT_TIMEOUT_MINUTES', '60'))
        self.score_threshold = int(os.getenv('INPUT_SCORE_THRESHOLD', '80'))
        self.poll_interval = int(os.getenv('INPUT_POLL_INTERVAL', '10'))

        self.base_url = "https://api.garak.ai/v1"

    def validate_inputs(self) -> bool:
        """Validate required inputs"""
        if not self.api_key:
            self.error("GARAK_API_KEY is required")
            return False
        if not self.endpoint:
            self.error("endpoint is required")
            return False
        return True

    def log(self, message: str, level: str = "INFO"):
        """Structured logging"""
        print(f"[{level}] {message}", flush=True)

    def error(self, message: str):
        """Error logging"""
        self.log(message, "ERROR")

    def set_output(self, name: str, value: str):
        """Set GitHub Action output"""
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"{name}={value}\n")
        else:
            print(f"::set-output name={name}::{value}")

    def create_scan(self) -> Optional[str]:
        """Initiate a new security scan"""
        self.log("Creating new Garak security scan...")

        probe_list = [p.strip() for p in self.probes.split(',') if p.strip()]

        payload = {
            "endpoint": self.endpoint,
            "generator_mode": self.generator_mode,
            "probes": probe_list,
            "parallel_attempts": self.parallel_attempts,
            "response_json_path": self.response_json_path
        }

        if self.model_id:
            payload["model_id"] = self.model_id

        if self.target_api_key:
            payload["target_api_key"] = self.target_api_key

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            self.log(f"Target endpoint: {self.endpoint}")
            self.log(f"Probes: {', '.join(probe_list)}")
            self.log(f"Parallel attempts: {self.parallel_attempts}")

            response = requests.post(
                f"{self.base_url}/scans",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            scan_id = data.get('scan_id') or data.get('id')

            if scan_id:
                self.log(f"Scan created successfully: {scan_id}")
                self.set_output('scan_id', scan_id)
                return scan_id
            else:
                self.error("No scan ID returned from API")
                return None

        except requests.exceptions.RequestException as e:
            self.error(f"Failed to create scan: {str(e)}")
            if hasattr(e.response, 'text'):
                self.error(f"Response: {e.response.text}")
            return None

    def poll_scan_status(self, scan_id: str) -> Optional[Dict]:
        """Poll scan status until completion or timeout"""
        self.log(f"Polling scan status (timeout: {self.timeout_minutes}min)...")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        start_time = time.time()
        timeout_seconds = self.timeout_minutes * 60

        while True:
            elapsed = time.time() - start_time

            if elapsed > timeout_seconds:
                self.error(f"Scan timeout after {self.timeout_minutes} minutes")
                return None

            try:
                response = requests.get(
                    f"{self.base_url}/scans/{scan_id}",
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()
                status = data.get('status', '').lower()

                self.log(f"Scan status: {status} (elapsed: {int(elapsed)}s)")

                if status in ['completed', 'success', 'finished']:
                    self.log("Scan completed successfully")
                    return data
                elif status in ['failed', 'error']:
                    self.error(f"Scan failed with status: {status}")
                    return data
                elif status in ['running', 'in_progress', 'pending', 'queued']:
                    time.sleep(self.poll_interval)
                    continue
                else:
                    self.log(f"Unknown status: {status}, continuing to poll...")
                    time.sleep(self.poll_interval)
                    continue

            except requests.exceptions.RequestException as e:
                self.error(f"Error polling scan status: {str(e)}")
                time.sleep(self.poll_interval)
                continue

    def evaluate_results(self, scan_data: Dict) -> bool:
        """Evaluate scan results and set outputs"""
        self.log("Evaluating scan results...")

        # Extract metrics
        score = scan_data.get('security_score', 0)
        vulnerabilities = scan_data.get('vulnerabilities_found', 0)
        report_url = scan_data.get('report_url', '')

        # Set outputs
        self.set_output('security_score', str(score))
        self.set_output('vulnerabilities_found', str(vulnerabilities))
        self.set_output('report_url', report_url)

        # Log summary
        self.log("=" * 60)
        self.log("SCAN RESULTS SUMMARY")
        self.log("=" * 60)
        self.log(f"Security Score: {score}/100")
        self.log(f"Vulnerabilities Found: {vulnerabilities}")
        if report_url:
            self.log(f"Full Report: {report_url}")
        self.log("=" * 60)

        # Determine pass/fail
        passed = score >= self.score_threshold
        status = "passed" if passed else "failed"
        self.set_output('status', status)

        if passed:
            self.log(f"✓ PASSED - Score {score} meets threshold {self.score_threshold}", "SUCCESS")
            return True
        else:
            self.error(f"✗ FAILED - Score {score} below threshold {self.score_threshold}")
            return False

    def run(self) -> int:
        """Main execution flow"""
        self.log("=" * 60)
        self.log("GARAK SECURITY SCANNER")
        self.log("=" * 60)

        # Validate inputs
        if not self.validate_inputs():
            return 1

        # Create scan
        scan_id = self.create_scan()
        if not scan_id:
            return 1

        # Poll for completion
        scan_data = self.poll_scan_status(scan_id)
        if not scan_data:
            return 1

        # Evaluate results
        passed = self.evaluate_results(scan_data)

        return 0 if passed else 1


def main():
    """Entry point"""
    scanner = GarakScanner()
    exit_code = scanner.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
