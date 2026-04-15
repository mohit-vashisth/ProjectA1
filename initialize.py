import subprocess
import sys
import time


def run_backend():
    return subprocess.Popen(
        ["python", "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
    )


def run_frontend():
    return subprocess.Popen(
        ["streamlit", "run", "ui/app.py", "--server.port", "8501"]
    )


def main():
    print()
    print("╔══════════════════════════════════════╗")
    print("⚠️  AN UNKNOWN SIGNAL HAS BEEN DETECTED")
    print("╚══════════════════════════════════════╝")

    backend = run_backend()
    time.sleep(2)

    print()
    print("╔══════════════════════════════════════╗")
    print("🌌 ORIGIN: UNDEFINED... EXISTENCE: UNREGISTERED")
    print("╚══════════════════════════════════════╝")

    frontend = run_frontend()

    try:
        print()
        print("╔══════════════════════════════════════╗")
        print("👁️  ENTITY APPRAISING: ERROR")
        print("╚══════════════════════════════════════╝")
        print()
        print("╔══════════════════════════════════════╗")
        print("👁️  UNABLE TO DETECT")
        print("╚══════════════════════════════════════╝")
        print()
        print("╔══════════════════════════════════════╗")
        print("👁️  USING FORCED APPRAISEL: ERROR")
        print("╚══════════════════════════════════════╝")
        print()
        print("╔══════════════════════════════════════╗")
        print("👁️  UNABLE TO DETECT")
        print("╚══════════════════════════════════════╝")
        print()
        print("╔══════════════════════════════════════╗")
        print("👁️  USING MAXIMUM APPRAISEL: STATUS")
        print("╚══════════════════════════════════════╝")
        print()
        print("╔══════════════════════════════════════╗")
        print("👁️  ENTITY STATUS: AWAKENING")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("⚡ MULTIVERSE FREQUENCIES ARE RESONATING")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("☠️  WARNING: THIS PRESENCE TRANSCENDS ALL KNOWN LAWS")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("…ATTEMPTING TO ESTABLISH CONTACT…")
        print("╚══════════════════════════════════════╝")

        backend.wait()
        frontend.wait()

    except KeyboardInterrupt:
        print()
        print("╔══════════════════════════════════════╗")
        print("⚠️  UNAUTHORIZED ACTION DETECTED")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("❓ UNKNOWN INTERFERENCE FROM HOST...")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("💥 ENTITY STATUS: TERMINATED")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("⚡ CAUSE: HIDDEN")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("🌌 MULTIVERSE RESPONSE: SILENT")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("████ SOMETHING THAT SHOULD NOT DIE... HAS DIED ████")
        print("╚══════════════════════════════════════╝")

        print("╔══════════════════════════════════════╗")
        print("████ CONSEQUENCES: UNKNOWN ████")
        print("╚══════════════════════════════════════╝")

        backend.kill()
        frontend.kill()
        sys.exit()

if __name__ == "__main__":
    main()