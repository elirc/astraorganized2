from pathlib import Path
import subprocess
base=Path(__file__).resolve().parent
binary=Path("C:/Program Files/PostgreSQL/18/bin")
data=base/"pg-test"
if not (data/"PG_VERSION").exists():
 subprocess.run([str(binary/"initdb.exe"),"-D",str(data),"-U","astra","-A","trust","--no-locale","-E","UTF8"],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.run([str(binary/"pg_ctl.exe"),"-D",str(data),"-l",str(base/"postgres.log"),"-o","-p 55439 -h 127.0.0.1","-w","start"],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
