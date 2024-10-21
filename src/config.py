import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
SECRET_KEY=os.getenv("SECRET_KEY")
REACT_IP_ADDR=os.getenv("REACT_IP_ADDR")
IP_ADDR_WORK=os.getenv("IP_ADDR_WORK")