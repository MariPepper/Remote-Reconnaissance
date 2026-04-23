<?php
$results_dir = __DIR__ . '/audit_results';
$copies_dir  = __DIR__ . '/audit_copies';
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">

<style>
    html, body {
        height: 100%;
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
        background: #fff;
        color: #222;
        overflow: hidden; /* prevents scroll inside iframe */
    }

    .wrap {
        box-sizing: border-box;
        height: 100%;
        padding: 0; /* padding comes from the parent .card */
    }

    h3 {
        margin-top: 0;
        font-size: 18px;
        color: #2c3e50;
        font-weight: 700;
    }    

    .success {
        background: #e8fbe8;
        border-left: 6px solid #27ae60;
        padding: 14px 18px;
        margin-bottom: 20px;
        border-radius: 6px;
        font-weight: bold;
        color: #1e7d3a;
        font-size: 14px;
    }

    .error {
        background: #fdeaea;
        border-left: 6px solid #c0392b;
        padding: 14px 18px;
        margin-bottom: 20px;
        border-radius: 6px;
        font-weight: bold;
        color: #a5281e;
        font-size: 14px;
    }
</style>

</head>
<body>
<div class="wrap">

    <h3>Audit Results</h3>
    <?php
    $result_files = glob($results_dir . '/*');

    if ($result_files) {
        foreach ($result_files as $file) {
            echo "<div class='success'>✔ Created: " . htmlspecialchars(basename($file)) . "</div>";
        }
    } else {
        echo "<div class='error'>No files found in audit_results.</div>";
    }
    ?>

    <h3>Audit Copies</h3>
    <?php
    $copy_files = glob($copies_dir . '/*');

    if ($copy_files) {
        foreach ($copy_files as $file) {
            echo "<div class='success'>✔ Created: " . htmlspecialchars(basename($file)) . "</div>";
        }
    } else {
        echo "<div class='error'>No files found in audit_copies.</div>";
    }
    ?>

</div>
</body>
</html>
