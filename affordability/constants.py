from pathlib import Path


ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = ROOT/'data'
REGIONS = {
	'auckland', 
	'canterbury', 
	'nelson', 
	'otago', 
	'waikato', 
  	'wellington',
}
MODES = ['walking', 'bicycling', 'driving', 'transit']
# NZD/km
COST_BY_MODE = {'walk': 0, 'bicycle': 0, 'car': 0.274, 
  'transit': 0.218}
