import time
from datetime import datetime

from pywinauto import Desktop
from pywinauto.application import Application


DURATION_MINUTES = 5
INTERVAL_SECONDS = 5

TEXTS = [
    "Test automatisé en cours.",
    "Écriture périodique dans Bloc-notes.",
    "Validation de l'automatisation desktop.",
    "Nouvelle itération exécutée.",
]


def find_notepad_window():
    desktop = Desktop(backend="uia")

    windows = desktop.windows(
        control_type="Window",
        title_re=r".*(Notepad|Bloc-notes).*",
    )

    if not windows:
        raise RuntimeError(
            "Aucune fenêtre Bloc-notes trouvée."
        )

    print(
        f"{len(windows)} fenêtre(s) Bloc-notes trouvée(s)"
    )

    for index, win in enumerate(windows):
        print(
            f"[{index}] "
            f"title='{win.window_text()}' "
            f"pid={win.process_id()} "
            f"visible={win.is_visible()}"
        )

    visible_windows = [
        win
        for win in windows
        if win.is_visible()
    ]

    if not visible_windows:
        raise RuntimeError(
            "Aucune fenêtre Bloc-notes visible."
        )

    return visible_windows[-1]


def find_editor(window):
    editors = window.descendants(
        control_type="Document"
    )

    if editors:
        print(
            f"{len(editors)} contrôle(s) Document trouvé(s)"
        )
        return editors[0]

    editors = window.descendants(
        control_type="Edit"
    )

    if editors:
        print(
            f"{len(editors)} contrôle(s) Edit trouvé(s)"
        )
        return editors[0]

    raise RuntimeError(
        "Zone d'édition Bloc-notes introuvable."
    )


def main():
    print("Ouverture de Bloc-notes...")

    Application(
        backend="uia"
    ).start(
        "notepad.exe",
        wait_for_idle=False,
    )

    time.sleep(2)

    print("Recherche de la fenêtre...")

    window = find_notepad_window()

    print(
        f"Fenêtre sélectionnée : "
        f"'{window.window_text()}'"
    )

    window.set_focus()

    editor = find_editor(window)

    print("Zone d'édition trouvée.")

    duration_seconds = (
        DURATION_MINUTES * 60
    )

    start_time = time.time()

    end_time = (
        start_time
        + duration_seconds
    )

    iteration = 0

    print(
        f"Automatisation lancée pendant "
        f"{DURATION_MINUTES} minute(s)."
    )

    try:
        while time.time() < end_time:
            text = TEXTS[
                iteration % len(TEXTS)
            ]

            timestamp = (
                datetime.now()
                .strftime("%H:%M:%S")
            )

            line = (
                f"[{timestamp}] {text}"
            )

            print(
                f"Itération {iteration + 1}: "
                f"{line}"
            )

            window.set_focus()

            time.sleep(0.5)

            editor.type_keys(
                line + "{ENTER}",
                with_spaces=True,
            )

            iteration += 1

            remaining_seconds = int(
                end_time - time.time()
            )

            if remaining_seconds <= 0:
                break

            print(
                f"Prochaine saisie dans "
                f"{INTERVAL_SECONDS}s - "
                f"temps restant : "
                f"{remaining_seconds}s"
            )

            time.sleep(
                min(
                    INTERVAL_SECONDS,
                    remaining_seconds,
                )
            )

    except KeyboardInterrupt:
        print(
            "\nArrêt manuel demandé."
        )

    finally:
        elapsed = int(
            time.time() - start_time
        )

        print(
            "Fin de l'automatisation."
        )

        print(
            f"Durée réelle : "
            f"{elapsed} seconde(s)"
        )

        print(
            f"Nombre d'itérations : "
            f"{iteration}"
        )


if __name__ == "__main__":
    main()