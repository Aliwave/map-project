# if __name__ == "__main__":
# 	from core import create_app
# 	app = create_app()
# 	app.run()

import os
from core import db, create_app
from core.models import UserTable

app = create_app()

@app.shell_context_processor
def shell():
	return {"db":db, "UserTable":UserTable}