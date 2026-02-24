from studapp.models import Branch


def branches_context(request):
    """Make branches available in every template (for footer links)."""
    return {'branches': Branch.objects.all()}
