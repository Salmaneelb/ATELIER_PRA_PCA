@app.route("/status", methods=["GET"])
def status():
    # Count en base
    conn = sqlite3.connect("/data/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]
    conn.close()

    backup_dir = "/backup"
    last_backup_file = None
    backup_age_seconds = None

    files = [
        os.path.join(backup_dir, f)
        for f in os.listdir(backup_dir)
        if os.path.isfile(os.path.join(backup_dir, f))
    ]

    if files:
        latest_file = max(files, key=os.path.getmtime)
        last_backup_file = os.path.basename(latest_file)
        backup_age_seconds = int(time.time() - os.path.getmtime(latest_file))

    return jsonify({
        "count": count,
        "last_backup_file": last_backup_file,
        "backup_age_seconds": backup_age_seconds
    })
