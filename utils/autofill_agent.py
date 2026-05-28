import webbrowser


def open_application_page(apply_link):
    try:
        if not apply_link or apply_link == "N/A":
            return "No valid apply link found."

        webbrowser.open_new_tab(apply_link)

        return "Application page opened in your browser. Use your saved profile/application packet to review and fill."

    except Exception as e:
        return f"Autofill error: {repr(e)}"