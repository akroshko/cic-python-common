# TODO: do appropriate shebang here?
# http://ipython.readthedocs.io/en/stable/config/details.html#keyboard-shortcuts

from IPython import get_ipython
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import HasFocus, HasSelection, ViInsertMode, EmacsInsertMode

from prompt_toolkit.key_binding.bindings.named_commands import get_by_name

ip = get_ipython()
insert_mode = ViInsertMode() | EmacsInsertMode()

def insert_unexpected(event):
    buf = event.current_buffer
    buf.insert_text('The Spanish Inquisition')

# TODO: error when rlipython is activated

# Register the shortcut if IPython is using prompt_toolkit
# TODO: warn when this is activatved
if hasattr(ip, 'pt_cli'):
    registry = ip.pt_cli.application.key_bindings_registry
    registry.add_binding(Keys.Escape,u'p',
                     filter=(HasFocus(DEFAULT_BUFFER)
                             & ~HasSelection()
                             & insert_mode))(get_by_name('previous-history'))
    registry.add_binding(Keys.Escape,u'n',
                         filter=(HasFocus(DEFAULT_BUFFER)
                                 & ~HasSelection()
                                 & insert_mode))(get_by_name('next-history'))
                         # & insert_mode))(insert_unexpected)
