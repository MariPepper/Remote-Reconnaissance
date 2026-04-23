<?php
header("Content-Type: application/octet-stream");
header("Content-Disposition: attachment; filename=auditor.exe");
header("Content-Length: " . filesize(__DIR__ . "/auditor.exe"));
readfile(__DIR__ . "/auditor.exe");
exit;
