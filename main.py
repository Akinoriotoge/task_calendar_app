from database import init_db
from ui_main import create_ui

init_db()

app = create_ui()
app.mainloop()
