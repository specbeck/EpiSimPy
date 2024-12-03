print("In module products __package__, __name__ ==", __package__, __name__)
from core.epidemic import Epidemic


epidemic = Epidemic(1000, days=100)


