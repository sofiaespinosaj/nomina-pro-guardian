#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path


def main() -> None:
	base_dir = Path(__file__).resolve().parent.parent
	report_path = base_dir / ".report.json"

	command = [
		"docker",
		"run",
		"--rm",
		"-w",
		"/app",
		"-v",
		f"{base_dir}:/app",
		"guardian-sandbox",
		"pytest",
		"tests/",
		"--json-report",
		"--json-report-file=.report.json",
	]

	result = subprocess.run(
		command,
		capture_output=True,
		text=True,
	)

	stdout = result.stdout or ""
	stderr = result.stderr or ""

	total = 0
	passed = 0
	failed = 0
	error_detail = None

	try:
		report_data = json.loads(report_path.read_text(encoding="utf-8"))
		summary = report_data.get("summary", {}) if isinstance(report_data, dict) else {}
		total = int(summary.get("total", 0))
		passed = int(summary.get("passed", 0))
		failed = int(summary.get("failed", 0)) + int(summary.get("error", 0))
	except Exception as exc:
		failed = 1
		error_detail = f"No se pudo leer .report.json: {exc}"

	verdict = "APROBADO" if failed == 0 else "RECHAZADO"

	payload = {
		"veredicto": verdict,
		"total": total,
		"pasaron": passed,
		"fallaron": failed,
		"logs": {
			"stdout": stdout,
			"stderr": stderr,
		},
	}
	if error_detail:
		payload["error"] = error_detail

	print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
	main()
